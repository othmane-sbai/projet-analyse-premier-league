import pandas as pd
import mysql.connector
from mysql.connector import Error


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'otmane', 
    'database': 'premier_league'
}

def create_db_connection(config):
    
    try:
        conn = mysql.connector.connect(**config)
        print("Connexion à MySQL réussie pour l'analyse.")
        return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

def calculate_points(row):
    
    if row['result'] == 'H':
        return 3 if row['is_home'] else 0
    elif row['result'] == 'A':
        return 0 if row['is_home'] else 3
    else: # Match nul
        return 1

def analyze_season_data(conn):
    
    
    
    SELECT 
        m.match_date, t1.name AS home_team, t2.name AS away_team,
        m.home_goals, m.away_goals, m.result
    FROM matches m
    JOIN teams t1 ON m.home_team_id = t1.id
    JOIN teams t2 ON m.away_team_id = t2.id
    ORDER BY m.match_date;
    """
    df = pd.read_sql(query, conn)
    print("Données récupérées depuis MySQL.")


    home_df = df[['home_team', 'home_goals', 'away_goals', 'result']].copy()
    home_df.rename(columns={'home_team': 'team', 'home_goals': 'goals_for', 'away_goals': 'goals_against'}, inplace=True)
    home_df['is_home'] = True
    
    away_df = df[['away_team', 'away_goals', 'home_goals', 'result']].copy()
    away_df.rename(columns={'away_team': 'team', 'away_goals': 'goals_for', 'home_goals': 'goals_against'}, inplace=True)
    away_df['is_home'] = False
    
    all_matches = pd.concat([home_df, away_df])
    
    all_matches['won'] = all_matches.apply(lambda r: (r['is_home'] and r['result'] == 'H') or (not r['is_home'] and r['result'] == 'A'), axis=1)
    all_matches['drawn'] = all_matches['result'] == 'D'
    all_matches['lost'] = all_matches.apply(lambda r: (r['is_home'] and r['result'] == 'A') or (not r['is_home'] and r['result'] == 'H'), axis=1)
    all_matches['points'] = all_matches.apply(calculate_points, axis=1)

    ranking = all_matches.groupby('team').agg(
        played=('team', 'count'),
        won=('won', 'sum'),
        drawn=('drawn', 'sum'),
        lost=('lost', 'sum'),
        goals_for=('goals_for', 'sum'),
        goals_against=('goals_against', 'sum'),
        points=('points', 'sum')
    ).reset_index()
    
    ranking['goal_difference'] = ranking['goals_for'] - ranking['goals_against']
    ranking = ranking.sort_values(by=['points', 'goal_difference', 'goals_for'], ascending=False).reset_index(drop=True)
    ranking.index += 1
    ranking.rename(columns={'team': 'Équipe', 'played': 'Joués', 'won': 'Gagnés', 'drawn': 'Nuls', 'lost': 'Perdus', 'goals_for': 'Buts Marqués', 'goals_against': 'Buts Encaissés', 'points': 'Points', 'goal_difference': 'Diff. Buts'}, inplace=True)

    
    avg_goals = (df['home_goals'] + df['away_goals']).mean()

   
    home_df['home_points'] = home_df['result'].map({'H': 3, 'D': 1, 'A': 0})
    away_df['away_points'] = away_df['result'].map({'A': 3, 'D': 1, 'H': 0})

    home_perf = home_df.groupby('team').agg(
        home_played=('team', 'count'),
        home_won=('result', lambda x: (x == 'H').sum()),
        home_points=('home_points', 'sum')
    ).reset_index()

    away_perf = away_df.groupby('team').agg(
        away_played=('team', 'count'),
        away_won=('result', lambda x: (x == 'A').sum()),
        away_points=('away_points', 'sum')
    ).reset_index()
    
    performances = pd.merge(home_perf, away_perf, on='team')
    performances.rename(columns={'team': 'Équipe'}, inplace=True)

    return ranking, avg_goals, performances

if __name__ == "__main__":
    connection = create_db_connection(db_config)
    if connection:
        ranking_df, avg_goals_score, performances_df = analyze_season_data(connection)
        connection.close()

        output_file = "analyse_premier_league_2324.xlsx"
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            ranking_df.to_excel(writer, sheet_name='Classement', index=True)
            performances_df.to_excel(writer, sheet_name='Performances Domicile-Ext', index=False)
            
            stats_df = pd.DataFrame({'Statistique': ['Moyenne de buts par match'], 'Valeur': [f"{avg_goals_score:.2f}"]})
            stats_df.to_excel(writer, sheet_name='Statistiques Générales', index=False)
        
        print(f"\nAnalyse terminée. Fichier Excel '{output_file}' créé avec succès.")
        print("\nAperçu du classement :")
        print(ranking_df.head(10))
