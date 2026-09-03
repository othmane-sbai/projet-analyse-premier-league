\# Analyse des Performances de la Premier League 2023/24



!\[Tableau de Bord Premier League](dashboard.png)



Ce projet présente une analyse complète des données de la saison 2023/2024 de la Premier League anglaise, depuis la collecte des données jusqu'à la création d'un tableau de bord interactif.



\## 🎯 Objectif



L'objectif était de créer un pipeline de données fonctionnel pour extraire, stocker, analyser et visualiser les performances des équipes de football.



\## 🛠️ Technologies Utilisées



\- \*\*Langage :\*\* Python 3.13

\- \*\*Bibliothèques Python :\*\* Pandas, mysql-connector-python, openpyxl

\- \*\*Base de Données :\*\* MySQL

\- \*\*Visualisation :\*\* Tableau Public

\- \*\*Versionnage :\*\* Git \& GitHub



\## 📁 Structure du Projet



```

Projet\_PremierLeague/

├── premier\_league\_2324.csv     # Données brutes

├── schema.sql                  # Création de la base et des tables MySQL

├── requirements.txt            # Dépendances Python

├── import\_data.py              # Script d'importation en base de données

├── analyse.py                  # Script d'analyse des données

├── analyse\_premier\_league\_2324.xlsx  # Fichier de résultats de l'analyse

└── README.md                   # Ce fichier

```



\## 🚀 Comment lancer le projet



1\.  \*\*Dépendances :\*\* Installer les bibliothèques Python : `pip install -r requirements.txt`.

2\.  \*\*Collecte des données :\*\* Télécharger le fichier `E0.csv` depuis \[football-data.co.uk](https://www.football-data.co.uk/englandm.php), le renommer `premier\_league\_2324.csv` et le placer dans le dossier du projet.

3\.  \*\*Base de données :\*\* Créer la base et les tables MySQL en exécutant le script `schema.sql` : `mysql -u root -p < schema.sql`.

4\.  \*\*Importation :\*\* Configurer les identifiants MySQL via les variables d'environnement `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD` et `MYSQL_DATABASE` (valeurs par défaut : `localhost`, `root`, vide, `premier_league`), puis lancer `python import_data.py`. Pour importer un autre fichier, passer son chemin en argument : `python import_data.py chemin/vers/premier\_league\_2324.csv`.

5\.  \*\*Analyse :\*\* Lancer le script `analyse.py` pour générer le fichier Excel.

6\.  \*\*Visualisation :\*\* Importer le fichier Excel dans Tableau pour recréer le tableau de bord.



\## 📊 Résultat



Le résultat final est un tableau de bord interactif disponible sur Tableau Public :

https://public.tableau.com/views/AnalysePremierLeague202324/Feuille1?:language=en-US\&publish=yes\&:sid=\&:redirect=auth\&:display\_count=n\&:origin=viz\_share\_link



\## 📈 Pistes d'amélioration



\- Intégrer une API pour obtenir des données en temps réel.

\- Développer un modèle de prédiction des résultats de matchs.

\- Analyser les statistiques de joueurs individuels (buteurs, passeurs).

