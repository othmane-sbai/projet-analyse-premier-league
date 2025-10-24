import pandas as pd
import mysql.connector
from mysql.connector import Error

# --- PARAMÈTRES DE CONNEXION ---
# MODIFIEZ CES VALEURS
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'otmane', # <-- Laissez les guillemets vides
    'database': 'premier_league'
}
csv_file_path = r"C:\Users\DELL\Desktop\Projects\Personnel\Projet_PremierLeague\premier_league_2324.csv"

# (Le reste du code est le même que dans la réponse précédente)
def create_db_connection(config):
    try:
        conn = mysql.connector.connect(**config)
        print("Connexion à MySQL réussie.")
        return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

def populate_teams_table(conn, df):
    cursor = conn.cursor()
    home_teams = df['HomeTeam'].unique()
    away_teams = df['AwayTeam'].unique()
    all_teams = pd.unique(pd.concat([pd.Series(home_teams), pd.Series(away_teams)]))
    
    for team in all_teams:
        try:
            cursor.execute("INSERT IGNORE INTO teams (name) VALUES (%s)", (team,))
        except Error as e:
            print(f"Erreur lors de l'insertion de l'équipe {team}: {e}")
    conn.commit()
    print("Table 'teams' peuplée avec succès.")

def get_team_mapping(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM teams")
    team_mapping = {name: id for id, name in cursor.fetchall()}
    return team_mapping

def import_match_data(conn, df, team_mapping):
    """Nettoie le DataFrame et insère les données dans la table 'matches'."""
    cursor = conn.cursor()
    
    # 1. Nettoyage et renommage des colonnes
    df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HS', 'AS', 'HST', 'AST', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']].copy()
    df.rename(columns={
        'Date': 'match_date',
        'HomeTeam': 'home_team_name',
        'AwayTeam': 'away_team_name',
        'FTHG': 'home_goals',
        'FTAG': 'away_goals',
        'FTR': 'result',
        'HS': 'home_shots',
        'AS': 'away_shots',
        'HST': 'home_shots_on_target',
        'AST': 'away_shots_on_target',
        'HC': 'home_corners',
        'AC': 'away_corners',
        'HY': 'home_yellow_cards',
        'AY': 'away_yellow_cards',
        'HR': 'home_red_cards',
        'AR': 'away_red_cards'
    }, inplace=True)

    # 2. Conversion des dates
    df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%Y').dt.date
    
    # 3. Mapping des noms d'équipes vers les IDs
    df['home_team_id'] = df['home_team_name'].map(team_mapping)
    df['away_team_id'] = df['away_team_name'].map(team_mapping)
    
    # 4. Suppression des colonnes temporaires
    df.drop(columns=['home_team_name', 'away_team_name'], inplace=True)
    
    # Remplacer les NaN potentiels par None pour SQL
    df = df.where(pd.notnull(df), None)

    # 5. Préparation pour l'insertion (MÉTHODE CORRIGÉE)
    tuples = [tuple(x) for x in df.to_numpy()]
    
    # On crée la chaîne de placeholders de manière plus sûre
    num_cols = len(df.columns)
    placeholders = ', '.join(['%s'] * num_cols)
    
    cols = ','.join(list(df.columns))
    sql = f"INSERT INTO matches ({cols}) VALUES ({placeholders})"
    
    # 6. Insertion des données avec executemany (plus efficace)
    try:
        cursor.executemany(sql, tuples)
        conn.commit()
        print(f"{cursor.rowcount} enregistrements insérés avec succès dans la table 'matches'.")
    except Error as e:
        print(f"Erreur lors de l'insertion des matchs: {e}")
        conn.rollback()

        
if __name__ == "__main__":
    try:
        df = pd.read_csv(csv_file_path)
        print("Fichier CSV chargé avec succès.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{csv_file_path}' n'a pas été trouvé.")
        exit()

    connection = create_db_connection(db_config)
    if connection:
        populate_teams_table(connection, df)
        team_map = get_team_mapping(connection)
        import_match_data(connection, df, team_map)
        connection.close()
        print("Connexion à MySQL fermée.")