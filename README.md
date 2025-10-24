\# Analyse des Performances de la Premier League 2023/24



!\[Tableau de Bord Premier League](dashboard.png)



Ce projet présente une analyse complète des données de la saison 2023/2024 de la Premier League anglaise, depuis la collecte des données jusqu'à la création d'un tableau de bord interactif.



\## 🎯 Objectif



L'objectif était de créer un pipeline de données fonctionnel pour extraire, stocker, analyser et visualiser les performances des équipes de football.



\## 🛠️ Technologies Utilisées



\- \*\*Langage :\*\* Python 3.13

\- \*\*Bibliothèques Python :\*\* Pandas, mysql-connector-python

\- \*\*Base de Données :\*\* MySQL

\- \*\*Visualisation :\*\* Tableau Public

\- \*\*Versionnage :\*\* Git \& GitHub



\## 📁 Structure du Projet



```

Projet\_PremierLeague/

├── premier\_league\_2324.csv     # Données brutes

├── import\_data.py              # Script d'importation en base de données

├── analyse.py                  # Script d'analyse des données

├── analyse\_premier\_league\_2324.xlsx  # Fichier de résultats de l'analyse

└── README.md                   # Ce fichier

```



\## 🚀 Comment lancer le projet



1\.  \*\*Collecte des données :\*\* Télécharger le fichier `E0.csv` depuis \[football-data.co.uk](https://www.football-data.co.uk/englandm.php) et le renommer `premier\_league\_2324.csv`.

2\.  \*\*Base de données :\*\* Créer la base et les tables MySQL en exécutant le script SQL fourni.

3\.  \*\*Importation :\*\* Lancer le script `import\_data.py` après avoir configuré les identifiants de la base de données.

4\.  \*\*Analyse :\*\* Lancer le script `analyse.py` pour générer le fichier Excel.

5\.  \*\*Visualisation :\*\* Importer le fichier Excel dans Tableau pour recréer le tableau de bord.



\## 📊 Résultat



Le résultat final est un tableau de bord interactif disponible sur Tableau Public :

https://public.tableau.com/views/AnalysePremierLeague202324/Feuille1?:language=en-US\&publish=yes\&:sid=\&:redirect=auth\&:display\_count=n\&:origin=viz\_share\_link



\## 📈 Pistes d'amélioration



\- Intégrer une API pour obtenir des données en temps réel.

\- Développer un modèle de prédiction des résultats de matchs.

\- Analyser les statistiques de joueurs individuels (buteurs, passeurs).

