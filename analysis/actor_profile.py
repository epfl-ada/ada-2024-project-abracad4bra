import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
import re
import matplotlib as mpl
from scipy import stats
import matplotlib.cm as cm


# Usefull variables
custom_palette = ["#ff7100", "#fd9702", "#e102ff", "#ae03ff", "#000000"]
ethnicity_dict={
    # dict that maps each freebase id with the ethnicity (from freebase website)
    "/m/01kb9y": "Multiracial",
    "/m/05qb937": "Venezuelans",
    "/m/09v5bdn": "Puerto Ricans",
    "/m/02pfy17": "Syrian people",
    "/m/013xrm": "Germans",
    "/m/01n94b": "Slovaks",
    "/m/02w7gg": "English people",
    "/m/0x67": "African American",
    "/m/011bn6ys": None,
    "/m/0118b8ry": None,
    "/m/03bkbh": "Irish people",
    "/m/0318mh": "Finns",
    "/m/027hhf": "Arbëreshë people",
    "/m/04c28": "Kurds",
    "/m/0cx3p": "Berbers",
    "/m/032j30": "Native Hawaiians",
    "/m/0gcp7x": "Iranian Azerbaijanis",
    "/m/013xrm": "Germans",
    "/m/038723": "Greek American",
    "/m/0d2by": "Chinese American",
    "/m/09vc4s": "English American",
    "/m/0912ll": "Dominican American",
    "/m/07mqps": "Dutch-American",
    "/m/01qhm_": "German American",
    "/m/0dbxy": "Cherokee",
    "/m/013s41": "Bulgarians",
    "/m/01km_m": "Slovenes",
    "/m/02ctzb": "White people",
    "/m/033tf_": "Irish American",
    "/m/0222qb": "Italian people",
    "/m/0jt85pd": "Greeks",
    "/m/03w9xlf": "Filipino Italian",
    "/m/0j251_s": "Arabs in France",
    "/m/0bwhd5z": "Harari people",
    "/m/0k0t_dz": "Caucasian race",
    "/m/09743": "Pashtun",
    "/m/03lmx1": "Scottish people",
    "/m/0bpjh3": "Bengalis",
    "/m/0j63_pr": "French Canadian American",
    "/m/0jt8h6f": "Latin Americans",
    "/m/02gx2x": "Javanese people",
    "/m/048z7l": "Jewish American",
    "/m/03ts0c": "French people",
    "/m/013s3n": "Czechs",
    "/m/0268_k": "Danes",
    "/m/059_w": "Native Americans in the United States",
    "/m/09kr66": "Russian American",
    "/m/0f3v0": "Comanche",
    "/m/09743": "Pashtun",
    "/m/09vc4s": "English American",
    "/m/0bpjh3": "Bengalis",
    "/m/0x67": "African American",
    "/m/0j3c70b": "Jamaicans",
    "/m/0dryh9k": "Indian people",
    "/m/09vc4s": "English American",
    "/m/0dbxy": "Cherokee",
    "/m/03bkbh": "Irish people",
    "/m/02pfy17": "Syrian people",
    "/m/0cx3p": "Berbers",
    "/m/03bkbh": "Irish people",
    "/m/02ctzb": "White people",
    "/m/02w7gg": "English people",
    "/m/033tf_": "Irish American",
    "/m/09vc4s": "English American",
    "/m/0bwhd5z": "Harari people",
    "/m/0k0t_dz": "Caucasian race",
    "/m/013xrm": "Germans",
    "/m/09743": "Pashtun",
    "/m/03w9xlf": "Filipino Italian",
    "/m/0j251_s": "Arabs in France",
    "/m/04c28": "Kurds",
    "/m/0j63_pr": "French Canadian American",
    "/m/038723": "Greek American",
    "/m/0134vqyy": "Scottish American",
    "/m/0dbxy": "Cherokee",
    "/m/05qb937": "Venezuelans",
    "/m/033tf_": "Irish American",
    "/m/03bkbh": "Irish people",
    "/m/04c28": "Kurds",
    "/m/0j251_s": "Arabs in France",
    "/m/0bpjh3": "Bengalis",
    "/m/0dbxy": "Cherokee",
    "/m/038723": "Greek American"
}

# Usefull functions
def compute_gender_proportions(df):
    # function to compute the mean proportion of men and women in movies over the year
    df_women = df[df['Actor gender'] == 'F']
    df_men = df[df['Actor gender'] == 'M']

    men_per_movie = df_men.groupby(['Release_year', 'Name'])['Actor Name'].count().reset_index(name='Men Count')
    women_per_movie = df_women.groupby(['Release_year', 'Name'])['Actor Name'].count().reset_index(name='Women Count')

    all_actors_per_movie = women_per_movie.merge(men_per_movie, on=['Release_year', 'Name'])

    all_actors_per_movie['Total Count'] = all_actors_per_movie['Women Count'] + all_actors_per_movie['Men Count']

    all_actors_per_movie['Women proportion'] = all_actors_per_movie['Women Count'] / all_actors_per_movie['Total Count']
    all_actors_per_movie['Men proportion'] = all_actors_per_movie['Men Count'] / all_actors_per_movie['Total Count']

    mean_women_proportion = all_actors_per_movie.groupby('Release_year')['Women proportion'].mean().reset_index()
    mean_men_proportion = all_actors_per_movie.groupby('Release_year')['Men proportion'].mean().reset_index()

    return mean_women_proportion, mean_men_proportion


# Plot functions
def plot_men_women_proportions(CMU_mean_women_proportion, CMU_mean_men_proportion, Horror_mean_women_proportion, Horror_mean_men_proportion):

    plt.figure(figsize=(10, 6))

    plt.plot(CMU_mean_women_proportion['Release_year'], CMU_mean_women_proportion['Women proportion'], color=custom_palette[0], linestyle='-', markersize=5, label='Women - All genres')
    plt.plot(Horror_mean_women_proportion['Release_year'], Horror_mean_women_proportion['Women proportion'], color=custom_palette[1], linestyle='-', markersize=5, label='Women - Horro')
    plt.plot(CMU_mean_men_proportion['Release_year'], CMU_mean_men_proportion['Men proportion'], color=custom_palette[2], linestyle='-', markersize=5, label='Men - All genres')
    plt.plot(Horror_mean_men_proportion['Release_year'], Horror_mean_men_proportion['Men proportion'], color=custom_palette[3], linestyle='-', markersize=5, label='Men - Horror')

    plt.title("Comparison of the Evolution of Male and Female Proportions per Film: All Genres vs. Horror", fontsize=14)
    plt.xlabel("Année", fontsize=12)
    plt.ylabel("Proportion d'acteurs/trices", fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_age_differences_women_men(Horror_movies_with_actors, CMU_with_actors):

    Horror_movies_with_actors['Movie Type'] = 'Horror'
    CMU_with_actors['Movie Type'] = 'All genres'

    # concat both dfs
    all_movies_with_actors = pd.concat([Horror_movies_with_actors[['Actor age at movie release', 'Actor gender', 'Movie Type']], 
                                CMU_with_actors[['Actor age at movie release', 'Actor gender', 'Movie Type']]])

    all_movies_with_actors.reset_index(drop=True, inplace=True)

    # boxplot
    plt.figure(figsize=(10,6))
    sns.boxplot(x='Movie Type', y='Actor age at movie release', hue='Actor gender', data=all_movies_with_actors, palette={'M': custom_palette[3], 'F': custom_palette[0]})

    plt.title('Actor Age Distribution depending on Gender: Horror vs All Genres')
    plt.xlabel('Movie Genre')
    plt.ylabel('Age at Movie Release')
    plt.show()

def plot_ethnicity_actors(Horror_movies_with_actors, CMU_with_actors):
    
    top_ethnicities_CMU = CMU_with_actors['ethnicity_clean'].value_counts().head(30)
    top_ethnicities_horror = Horror_movies_with_actors['ethnicity_clean'].value_counts().head(30)

    # normalization
    total_CMU = CMU_with_actors.shape[0]
    total_horror = Horror_movies_with_actors.shape[0]

    # proportions
    proportions_non_horror = top_ethnicities_CMU / total_CMU
    proportions_horror = top_ethnicities_horror / total_horror

    proportions_horror = proportions_horror.reindex(proportions_non_horror.index, fill_value=0)

    # df for visualisation
    ethnicities_comparison = pd.DataFrame({
        'ethnicity_clean': proportions_non_horror.index,
        'All genres': proportions_non_horror.values,
        'Horror': proportions_horror.values
    })

    ethnicities_comparison = ethnicities_comparison.melt(id_vars="ethnicity_clean", 
                                                        value_vars=["All genres", "Horror"],
                                                        var_name="Movie Type", 
                                                        value_name="Proportion")

    # barplot
    plt.figure(figsize=(10, 6))
    sns.barplot(x="ethnicity_clean", y="Proportion", hue="Movie Type", data=ethnicities_comparison, palette=[custom_palette[2], custom_palette[0]])
    plt.title("Comparison of Actor Ethnicity Distribution: \n Horror vs All Genres")
    plt.xlabel("Ethnicity")
    plt.ylabel("Proportion of Actors")
    plt.xticks(rotation=90, ha="right")
    plt.tight_layout()
    plt.show()

