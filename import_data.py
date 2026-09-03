import argparse
import os
import sys

import pandas as pd
import mysql.connector
from mysql.connector import Error


db_config = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DATABASE', 'premier_league')
}
DEFAULT_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'premier_league_2324.csv')


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
   
    cursor = conn.cursor()
    
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

    
    df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%Y').dt.date
    
    
    df['home_team_id'] = df['home_team_name'].map(team_mapping)
    df['away_team_id'] = df['away_team_name'].map(team_mapping)
    
   
    df.drop(columns=['home_team_name', 'away_team_name'], inplace=True)
    
    
    df = df.where(pd.notnull(df), None)

    
    tuples = [tuple(x) for x in df.to_numpy()]
    
   
    num_cols = len(df.columns)
    placeholders = ', '.join(['%s'] * num_cols)
    
    cols = ','.join(list(df.columns))
    sql = f"INSERT INTO matches ({cols}) VALUES ({placeholders})"
    
   
    try:
        cursor.executemany(sql, tuples)
        conn.commit()
        print(f"{cursor.rowcount} enregistrements insérés avec succès dans la table 'matches'.")
    except Error as e:
        print(f"Erreur lors de l'insertion des matchs: {e}")
        conn.rollback()

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Importe le fichier CSV de la Premier League 2023/24 dans MySQL."
    )
    parser.add_argument(
        'csv_path',
        nargs='?',
        default=DEFAULT_CSV_PATH,
        help=f"Chemin du fichier CSV à importer (défaut : {DEFAULT_CSV_PATH})",
    )
    args = parser.parse_args(argv)

    try:
        df = pd.read_csv(args.csv_path)
    except FileNotFoundError:
        print(f"Erreur : le fichier '{args.csv_path}' est introuvable.", file=sys.stderr)
        print("Téléchargez E0.csv et indiquez son chemin : python import_data.py <chemin_du_fichier>", file=sys.stderr)
        return 1

    print("Fichier CSV chargé avec succès.")

    connection = create_db_connection(db_config)
    if connection is None:
        print("Importation annulée : impossible de se connecter à MySQL.", file=sys.stderr)
        return 1

    try:
        populate_teams_table(connection, df)
        team_map = get_team_mapping(connection)
        import_match_data(connection, df, team_map)
    finally:
        connection.close()
    print("Connexion à MySQL fermée.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
