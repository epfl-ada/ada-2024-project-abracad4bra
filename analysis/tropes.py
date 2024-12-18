import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl

# Usefull variables
custom_palette = ["#ff7100", "#fd9702", "#e102ff", "#ae03ff", "#000000"]
colors = [custom_palette[0], custom_palette[1], custom_palette[2], custom_palette[3]]

# Plot functions
def get_character_count(df, on_what, what, nb, title=None, plot=False):
    # count the character types and plot if wanted
    df = df[df[on_what]==what]
    count = df['Character type'].value_counts().nlargest(nb)

    if plot==True:
        plt.pie(count, labels=[f"{label} ({value})" for label, value in zip(count.index, count)], autopct='%1.1f%%', startangle=90)
        plt.title(title)

        plt.show()
    return count

def plot_top4_types(Horror_movies_with_actors_tropes, CMU_with_actors_tropes):

    horror_female_counts=get_character_count(Horror_movies_with_actors_tropes, 'Actor gender', 'F', 4)
    horror_male_counts=get_character_count(Horror_movies_with_actors_tropes, 'Actor gender', 'M', 4)
    non_horror_female_counts=get_character_count(CMU_with_actors_tropes, 'Actor gender', 'F', 4)
    non_horror_male_counts=get_character_count(CMU_with_actors_tropes, 'Actor gender', 'M', 4)
    fig, axs = plt.subplots(2, 2, figsize=(14, 12))

    axs[0, 0].pie(horror_female_counts, labels=[f"{label} ({value})" for label, value in zip(horror_female_counts.index, horror_female_counts)], autopct='%1.1f%%', startangle=90, colors=colors)
    axs[0, 0].set_title("Top 4 Character Types for Female Actors in Horror Movies")

    axs[0, 1].pie(horror_male_counts, labels=[f"{label} ({value})" for label, value in zip(horror_male_counts.index, horror_male_counts)], autopct='%1.1f%%', startangle=90, colors=colors)
    axs[0, 1].set_title("Top 4 Character Types for Male Actors in Horror Movies")

    axs[1, 0].pie(non_horror_female_counts, labels=[f"{label} ({value})" for label, value in zip(non_horror_female_counts.index, non_horror_female_counts)], autopct='%1.1f%%', startangle=90, colors=colors)
    axs[1, 0].set_title("Top 4 Character Types for Female Actors in Non-Horror Movies")

    axs[1, 1].pie(non_horror_male_counts, labels=[f"{label} ({value})" for label, value in zip(non_horror_male_counts.index, non_horror_male_counts)], autopct='%1.1f%%', startangle=90, colors=colors)
    axs[1, 1].set_title("Top 4 Character Types for Male Actors in Non-Horror Movies")

    plt.tight_layout()
    plt.show()