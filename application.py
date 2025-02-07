"""
📝 **Instructions** :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :
conda create -n projet python pandas numpy streamlit plotly seaborn matplotlib plotly plotly_express matplotlib.pyplot

conda activate projet
streamlit run application.py
- Complétez les sections en écrivant votre code où c’est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Utilisez des emoji avec windows + ;
- Interprétez les résultats de vos visualisations (quelques phrases).
"""

### 1. Importation des librairies et chargement des données
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

st.markdown("Compte GITHUB : LONPCLT/SAE601")
st.markdown("Picault Elowen Legendre Clémence")

# Chargement des données
df = pd.read_csv("ds_salaries.csv")

### 2. Exploration visuelle des données
st.title("📊 Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")

# Aperçu des données
if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head())

#Statistique générales avec describe pandas 
st.subheader("📌 Statistiques générales")
st.write(df.describe())

### 3. Distribution des salaires en France par rôle et niveau d'expérience, uilisant px.box et st.plotly_chart
st.subheader("📈 Distribution des salaires en France")
df_france = df[df['company_location'] == 'FR']
fig = px.box(df_france, x='experience_level', y='salary_in_usd', color='job_title', title="Distribution des salaires en France")
st.plotly_chart(fig)
st.markdown("Ce graphique en boîte montre la distribution des salaires en France en fonction du niveau d'expérience et du rôle. On observe que les salaires augmentent généralement avec l'expérience et que certains rôles ont une dispersion salariale plus élevée.")

### 4. Analyse des tendances de salaires :
st.subheader("📊 Salaire moyen par catégorie")
categorie = st.selectbox("Choisissez une catégorie", ['experience_level', 'employment_type', 'job_title', 'company_location'])
salaire_moyen = df.groupby(categorie)['salary_in_usd'].mean().reset_index()
fig = px.bar(salaire_moyen, x=categorie, y='salary_in_usd', title=f"Salaire moyen par {categorie}")
st.plotly_chart(fig)
st.markdown("Ce graphique en barres illustre le salaire moyen par catégorie choisie. Il permet d'identifier les tendances salariales en fonction de l'expérience, du type d'emploi, du rôle ou de l'emplacement de l'entreprise.")

### 5. Corrélation entre variables
# Calcul de la matrice de corrélation
# Affichage du heatmap avec sns.heatmap
st.subheader("🔗 Corrélations entre variables numériques")
num_df = df.select_dtypes(include=[np.number])
corr_matrix = num_df.corr()
plt.figure(figsize=(10,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
st.pyplot(plt)
st.markdown("Ce heatmap permet de visualiser les corrélations entre les variables numériques. Une corrélation élevée entre deux variables signifie qu'elles évoluent souvent ensemble. On peut ainsi identifier quels facteurs influencent le plus le salaire.")

### 6. Analyse interactive des variations de salaire
# Une évolution des salaires pour les 10 postes les plus courants
# count of job titles pour selectionner les postes
# calcule du salaire moyen par an
#utilisez px.line
st.subheader("📈 Évolution des salaires pour les 10 postes les plus courants")
job_counts = df['job_title'].value_counts().nlargest(10).index
df_top_jobs = df[df['job_title'].isin(job_counts)]
salary_trends = df_top_jobs.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
fig = px.line(salary_trends, x='work_year', y='salary_in_usd', color='job_title', title="Évolution des salaires")
st.plotly_chart(fig)
st.markdown("Cette courbe montre l'évolution des salaires pour les postes les plus courants au fil des années. Elle permet d'identifier les tendances et d'observer quelles professions connaissent une hausse ou une stagnation salariale.")

### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
st.subheader("📊 Salaire médian par expérience et taille d'entreprise")
df_median = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()
fig = px.bar(df_median, x='experience_level', y='salary_in_usd', color='company_size', title="Salaire médian")
st.plotly_chart(fig)
st.markdown("Ce graphique en barres présente le salaire médian en fonction du niveau d'expérience et de la taille de l'entreprise. On observe que les grandes entreprises offrent généralement des salaires plus élevés, surtout pour les profils expérimentés.")

### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages 
st.subheader("🎚️ Filtrer les salaires")
salaire_min, salaire_max = st.slider("Sélectionnez une plage de salaire", int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max()), (50000, 150000))
df_filtered = df[(df['salary_in_usd'] >= salaire_min) & (df['salary_in_usd'] <= salaire_max)]
st.write(df_filtered)
st.markdown("Utilisez ce filtre pour afficher uniquement les salaires dans une plage donnée et observer la répartition des salaires en fonction des autres critères.")

### 9.  Impact du télétravail sur le salaire selon le pays
st.subheader("🏠 Impact du télétravail sur le salaire")
fig = px.box(df, x='remote_ratio', y='salary_in_usd', color='company_location', title="Impact du télétravail")
st.plotly_chart(fig)
st.markdown("Ce graphique met en évidence l'impact du télétravail sur le salaire en fonction du pays. On peut observer si les employés en télétravail total ou partiel bénéficient de rémunérations différentes par rapport aux employés sur site.")

### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
st.subheader("🔍 Filtrage avancé")
exp_levels = st.multiselect("Sélectionnez le niveau d'expérience", df['experience_level'].unique())
company_sizes = st.multiselect("Sélectionnez la taille d'entreprise", df['company_size'].unique())
if exp_levels:
    df = df[df['experience_level'].isin(exp_levels)]
if company_sizes:
    df = df[df['company_size'].isin(company_sizes)]
st.write(df)
st.markdown("Ce filtre avancé permet de sélectionner des critères spécifiques pour affiner l'analyse des salaires selon l'expérience et la taille d'entreprise.")