import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
import re
import geopandas as gpd
import matplotlib as mpl
from scipy import stats

# Usefull variables
custom_palette = ["#ff7100", "#fd9702", "#e102ff", "#ae03ff", "#000000"]
topN = 10
useless = 1
country_coords = {
    "United States of America": (37.0902, -95.7129),
    "United Kingdom": (51.5074, -0.1278),
    "Canada": (56.1304, -106.3468),
    "Japan": (35.6762, 139.6503),
    "Italy": (41.9028, 12.4964),
    "Germany": (51.1657, 10.4515),
    "France": (48.8566, 2.3522),
    "India": (20.5937, 78.9629),
    "Spain": (40.4637, -3.7492),
    "South Korea": (36.5773, 127.0000),
    "Australia": (-25.2744, 133.7751),
    "Hong Kong": (22.3193, 114.1694),
    "Mexico": (23.6345, -102.5528),
    "New Zealand": (-40.9006, 174.8860),
    "Thailand": (15.8700, 100.9925),
    "Philippines": (12.8797, 121.7740),
    "West Germany": (51.1657, 10.4515), 
    "Sweden": (60.1282, 18.6435),
    "Netherlands": (52.3676, 4.9041),
    "Romania": (45.9432, 24.9668),
    "Cambodia": (12.5657, 104.9910),
    "Czech Republic": (49.8175, 15.4730),
    "Ireland": (53.1424, -7.6921),
    "South Africa": (-30.5595, 22.9375),
    "Argentina": (-38.4161, -63.6167),
    "Brazil": (-14.2350, -51.9253),
    "Belgium": (50.8503, 4.3517),
    "Norway": (60.4720, 8.4689),
    "China": (35.8617, 104.1954),
    "Denmark": (56.2639, 9.5018),
    "England": (51.5074, -0.1278),
    "Indonesia": (-0.7893, 113.9213),
    "Russia": (55.7558, 37.6173),
    "Yugoslavia": (44.0165, 21.0059),
    "Austria": (47.1625, 19.5033),
    "Malaysia": (4.2105, 101.9758),
    "Czechoslovakia": (49.8175, 15.4730),
    "Weimar Republic": (51.1657, 10.4515),
    "Finland": (61.9241, 25.7482),
    "Luxembourg": (49.6117, 6.13),
    "Turkey": (38.9637, 35.2433),
    "Poland": (51.9194, 19.1451),
    "Switzerland": (46.8182, 8.2275),
    "Hungary": (47.1625, 19.5033),
    "Singapore": (1.3521, 103.8198),
    "Greece": (39.0742, 21.8243),
    "Soviet Union": (56.2639, 9.5018), 
    "Bulgaria": (42.7339, 25.4858),
    "Taiwan": (23.6978, 120.9605),
    "Portugal": (38.7169, -9.1395),
    "Serbia": (44.8176, 20.4633),
    "Scotland": (56.4907, -4.2026),
    "Egypt": (26.8206, 30.8025),
    "Pakistan": (30.3753, 69.3451),
    "Croatia": (45.1, 15.2),
    "Wales": (52.1307, -3.7837),
    "Israel": (31.7680, 35.2137),
    "Chile": (-35.6751, -71.5430),
    "United Arab Emirates": (23.4241, 53.8478),
    "Cuba": (21.5218, -77.7812),
    "Peru": (-9.19, -75.0152),
    "Puerto Rico": (18.2208, -66.5901),
    "Iceland": (64.9631, -19.0208),
    "Slovakia": (48.6690, 19.6990),
    "Cameroon": (3.8480, 11.5021),
    "Azerbaijan": (40.1431, 47.5769),
    "Nepal": (28.3949, 84.1240),
    "Georgia": (42.3154, 43.3569),
    "Lithuania": (55.1694, 23.8813),
    "Colombia": (4.5709, -74.2973),
    "Ukraine": (48.3794, 31.1656),
    "Monaco": (43.7333, 7.4167),
    "Iran": (32.4279, 53.6880),
    "Uruguay": (-32.5228, -55.7658),
    "Bosnia and Herzegovina": (43.8486, 18.3564),
    "Slovak Republic": (48.6690, 19.6990),
    "Malta": (35.9375, 14.3754),
    "Morocco": (31.7917, -7.0926)
}
occidental_countries = [
    "United States of America", "United Kingdom", "Canada", "Italy", "Germany",
    "France", "Spain", "Australia", "New Zealand", "Sweden", "Netherlands",
    "Ireland", "Belgium", "Norway", "Denmark", "England", "Austria", "Luxembourg",
    "Finland", "Switzerland", "Portugal", "Scotland", "Wales", "Iceland", 
    "Malta", "Monaco"]

# Usefull functions
def count_countries(df):
    # flatten the list of countries in 'Countries_clean' and count the frequency for each country
    countries = [
        country 
        for sublist in df['Countries_clean'].dropna()
        for country in sublist if isinstance(sublist, list)
    ]
    return Counter(countries), len(df)


# Plot functions
def plot_nan_proportion(df, df_name, columns=None):

    # keep only specified columns, if provided
    if columns:
        nan_proportions = df[columns].isna().mean() * 100
    else:
        nan_proportions = df.isna().mean() * 100

    plt.figure(figsize=(10, 6))
    nan_proportions.plot(kind='barh', color='skyblue', edgecolor='black')
    plt.title(f'Proportion of NaN values per column in the {df_name} DF')
    plt.xlabel('Percentage of NaN values')
    plt.ylabel('Columns')
    plt.xlim(0, 100)
    
    # add percentage
    for index, value in enumerate(nan_proportions):
        plt.text(value + 1, index, f'{value:.1f}%', va='center', color='white')
        
    # to have the first row at the top
    plt.gca().invert_yaxis()
    plt.show()

def plot_movies_distribution_hist(CMU, Horror_movies):
    
    plt.figure(figsize=(10, 6))

    # plot release year distribution for all genres
    sns.histplot(CMU['Release_year'].dropna(), bins=150, kde=True, color=custom_palette[0], label="All genres", stat='density', linewidth=2, edgecolor=None)

    # plot release year distribution for horror
    sns.histplot(Horror_movies['Release_year'].dropna(), bins=150, kde=True, color=custom_palette[2], label="Horror", stat='density', linewidth=2, edgecolor=None)

    # manually add color to highlight horror 'peaks'
    plt.axvspan(1985, 1993, color='grey', alpha=0.3)  
    plt.axvspan(1970, 1975, color='grey', alpha=0.3)  
    plt.axvspan(2002, 2019, color='grey', alpha=0.3)  


    plt.title('Histogram of Movie Release Year Distribution: Horror vs All Genres', color='white')
    plt.xlabel('Release Year', color='white')
    plt.ylabel('Proportion', color='white')

    plt.legend()
    plt.show()

def plot_movies_countries_distribution(CMU, Horror_movies):

    # country counts and total movie counts for both dataframes
    cmu_country_counts, cmu_total_movies = count_countries(CMU)
    horror_country_counts, horror_total_movies = count_countries(Horror_movies)

    # select the top 20
    top_cmu_countries = [country for country, count in cmu_country_counts.most_common(20)]

    # calculate proportions for each dataset
    cmu_proportions = [
        cmu_country_counts.get(country, 0) / cmu_total_movies for country in top_cmu_countries
    ]
    horror_proportions = [
        horror_country_counts.get(country, 0) / horror_total_movies for country in top_cmu_countries
    ]


    plt.figure(figsize=(14, 8))
    bar_width = 0.35
    x = range(len(top_cmu_countries))
    plt.bar(x, cmu_proportions, width=bar_width, label='All genres', color=custom_palette[2])
    plt.bar([pos + bar_width for pos in x], horror_proportions, width=bar_width, label='Horror', color=custom_palette[0])

    plt.xlabel('Country')
    plt.ylabel('Proportion of Movies')
    plt.title('Top 20 Most Frequent Countries (Proportion): All Genres vs Horror')
    plt.xticks([pos + bar_width / 2 for pos in x], top_cmu_countries, rotation=90)
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_most_represented_associated_genres(df):

    subgenres_counts = df\
                        .Genres\
                        .explode()\
                        .apply(lambda str: re.sub(" ", "", str))\
                        .value_counts()

    most_represented_subgenres = subgenres_counts[useless:topN+useless]
    palette = sns.color_palette("viridis", len(most_represented_subgenres))

    ax = sns.barplot(most_represented_subgenres, estimator="sum", errorbar=None, orient='h', palette=custom_palette[:-1])
    plt.xlabel("Number of associations")
    plt.ylabel("Genres")
    plt.title(f"Top {topN} genres appearances in horror movies")

def plot_movies_world_map(df):

    countries_counts = df\
                        .Countries_clean\
                        .explode()\
                        .value_counts()

    world_map_file = gpd.datasets.get_path('naturalearth_lowres')
    world_map = gpd.read_file(world_map_file)

    fig, axis = plt.subplots(figsize=(10, 10))
    world_map.plot(ax=axis, color='lightgray', edgecolor='darkgray')

    norm = mpl.colors.Normalize(vmin=np.min(countries_counts), vmax=np.max(countries_counts)/100)
    cmap = mpl.colors.LinearSegmentedColormap.from_list('custom_cmap', custom_palette[:-1])

    for country, count in countries_counts.items():
        lat, lon = country_coords[country]
        axis.scatter(lon, lat, s=count*6, label=country, alpha=0.5, c=count, cmap=cmap, norm=norm)
    

def testing_occidental_countries(df):

    countries_counts = df\
                        .Countries_clean\
                        .explode()\
                        .value_counts()

    isOccidental = countries_counts.index.isin(occidental_countries)
    occidental_counts = countries_counts[isOccidental]
    non_occidental_counts = countries_counts[~isOccidental]

    stat, pvalue = stats.mannwhitneyu(occidental_counts, non_occidental_counts)

    return stat, pvalue
