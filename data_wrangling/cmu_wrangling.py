import pandas as pd 
import numpy as np 
import ast
import re
import os
from analysis.actor_profile import ethnicity_dict
import json


# Paths
movie_metadata_path = './data/MovieSummaries/movie.metadata.tsv'
horror_movies_path = 'data/horror_movies.csv'
HorrorMovieSummaries_path = 'data/HorrorMovieSummaries.txt'
output_file_Summaries = 'data/Summaries.txt'
output_file_Taglines = 'data/Taglines.txt'
Horror_Movies_Clean_path = 'data/Horror_Movies_Clean.csv'
triggers_path = 'data/EVERY_trigger_movies.csv'

# Usefull variables
CMU_headers = ['Weekipedia_ID', 'Freebase_ID', 'Name', 'Release_date', 'Revenue', 
                'Runtime', 'Language', 'Countries', 'Genres']
cleaning_columns = ['Language', 'Genres', 'Countries']

# Usefull functions
def extract_words(column):
    return column.apply(ast.literal_eval).apply(lambda x: list(x.values()))

def clean_language(language_string):
    return re.sub(" Language", "", language_string)

def get_Horror_movies_quasi_final(CMU):

    isHorrorMovie = CMU['Genres_clean'].apply(lambda l: 'Horror' in l)
    horror_df = CMU[isHorrorMovie]

    CMU_horror_df = CMU[CMU['Genres_clean'].apply(lambda l: 'Horror' in l)]

    horror_df = pd.read_csv(horror_movies_path)

    horror_df['Release_year'] = horror_df['release_date'].astype(str).str.extract(r'(\d{4})')
    horror_df['Release_year'] = pd.to_numeric(horror_df['Release_year'])
    horror_df = horror_df.drop(['original_title', 'poster_path', 'status', 'adult', 'backdrop_path', 'collection', 'release_date'], axis=1)
    horror_df['genre_names'] = horror_df['genre_names'].str.split(',')

    Horror_movies = pd.merge(CMU_horror_df, horror_df, left_on='Name',right_on='title', how='outer')

    Horror_movies['Name'] = Horror_movies['Name'].combine_first(Horror_movies['title'])
    Horror_movies['Release_year'] = Horror_movies['Release_year_x'].combine_first(Horror_movies['Release_year_y'])
    Horror_movies['Runtime'] = Horror_movies['Runtime'].combine_first(Horror_movies['runtime'])
    Horror_movies['Revenue'] = Horror_movies['Revenue'].combine_first(Horror_movies['revenue'])
    Horror_movies['Genres'] = Horror_movies['Genres_clean'].combine_first(Horror_movies['genre_names'])

    Horror_movies = Horror_movies.drop(['title', 'Release_year_x', 'Release_year_y', 'runtime', 'revenue', 'Genres_clean', 'genre_names'], axis=1)

    Horror_movies['ID'] = Horror_movies.index + 1 
    Horror_movies_quasi = Horror_movies.drop('id', axis=1)

    return Horror_movies_quasi

def get_character_metadata():

    character_path = os.path.join(os.getcwd(), 'data/MovieSummaries', 'character.metadata.tsv')
    character_columns = [
    'Wikipedia movie ID', 'Freebase Movie ID', 'Movie release date','Character Name', 'Actor DOB', 'Actor gender', 'Actor height', 'Actor ethnicity', 
        'Actor Name', 'Actor age at movie release', 'Freebase character map1', 'Freebase character map2', 'Freebase character map3'
    ]
    character_metadata= pd.read_csv(character_path, sep='\t', names = character_columns)



    character_metadata['ethnicity_clean'] = character_metadata['Actor ethnicity'].map(ethnicity_dict)
    character_metadata['Release_year'] = character_metadata['Movie release date'].astype(str).str.extract(r'(\d{4})')
    character_metadata['Release_year'] = pd.to_numeric(character_metadata['Release_year'])
    character_metadata = character_metadata.drop(['Movie release date', 'Actor ethnicity'], axis=1)
    # replace all negative ages by nan
    character_metadata['Actor age at movie release'] = character_metadata['Actor age at movie release'].where(character_metadata['Actor age at movie release'] >= 0, np.nan)

    return character_metadata

def parse_json_column(description):
    # convert json into dict
    return json.loads(description)


# Functions to get data
def get_CMU():

    CMU = pd.read_csv(movie_metadata_path, sep='\t', names=CMU_headers)

    CMU['Release_year'] = CMU['Release_date'].astype(str).str.extract(r'(\d{4})')
    CMU['Release_year'] = pd.to_numeric(CMU['Release_year'])

    
    for column_name in cleaning_columns:
        CMU[column_name+"_clean"] = extract_words(CMU[column_name])

    CMU.Language_clean = CMU.Language_clean.apply(lambda lang_list: list(map(clean_language, lang_list)))

    CMU = CMU.drop(['Release_date', 'Language', 'Countries', 'Genres'], axis=1)

    CMU.loc[CMU['Release_year'] == CMU['Release_year'].min(), 'Release_year'] = 2010

    return CMU

def get_Horror_movies_and_merged_df(CMU):

    Horror_movies = get_Horror_movies_quasi_final(CMU)
    CMU_plot_summaries = pd.read_csv(HorrorMovieSummaries_path, sep='\t', header=None, names=['Weekipedia_ID', 'summary'])

    merged_df = Horror_movies.copy()
    # Ensure that both 'wiki_id' columns are of the same type
    CMU_plot_summaries['Weekipedia_ID'] = CMU_plot_summaries['Weekipedia_ID'].astype(str)
    merged_df['Weekipedia_ID'] = merged_df['Weekipedia_ID'].astype(str)

    # Merge on 'wiki_id' to get the summaries in merged_df
    merged_df = pd.merge(merged_df, CMU_plot_summaries, on='Weekipedia_ID', how='left')
    merged_df['Summary'] = merged_df['overview'].combine_first(merged_df['summary'])

    # Write summaries to the output file
    with open(output_file_Summaries, 'w', encoding='utf-8') as f:
        for _, row in merged_df.iterrows():
            # Write each line in the format: new ID followed by the summary
            f.write(f"{row['ID']}\t{row['Summary']}\n")

    # Write taglines to the output file, checking for non-NaN values
    with open(output_file_Taglines, 'w', encoding='utf-8') as f:
        for _, row in merged_df.iterrows():
            # Check if 'tagline' is not NaN
            if pd.notna(row['tagline']):
                # Write each line in the format: new ID followed by the tagline
                f.write(f"{row['ID']}\t{row['tagline']}\n")

    Horror_movies = Horror_movies.drop(['overview', 'tagline'], axis=1)

    Horror_movies.to_csv(Horror_Movies_Clean_path)

    return Horror_movies, merged_df

def get_df_hist(merged_df):

    # preparing data for historical analysis 
    df_hist=merged_df.copy()
    df_hist['Summary'] = df_hist['Summary'].fillna('') # replace NaN by empty string
    df_hist['Release_year'] = df_hist['Release_year'].fillna(0).astype(int) 
    df_hist['Release_year'] = pd.to_datetime(df_hist['Release_year'], format='%Y', errors='coerce')
    df_hist = df_hist[df_hist['Release_year'] >= pd.to_datetime('1950', format='%Y')]

    return df_hist

def get_merged_and_triggers(Horror_movies):

    triggers = pd.read_csv(triggers_path)
    triggers.fillna(0, inplace = True)
    triggers = triggers.apply(lambda col: col.astype(int) if col.dtype in ['float64', 'float32'] else col)
    triggers = triggers.replace({1: True, 0: False})

    merged = pd.merge(Horror_movies, triggers, left_on = 'Name', right_on = 'Movie')
    merged = merged.dropna(subset=['Date'])

    merged['Date'] = merged['Date'].astype(int)

    return merged, triggers

def get_df_with_actors(df):

    character_metadata = get_character_metadata()
    df_with_actors = pd.merge(df, character_metadata, on=['Wikipedia movie ID', 'Release_year'], how='left')

    return df_with_actors

def get_tv_tropes():
    tvtropes_tsv = os.path.join(os.getcwd(), 'data', 'MovieSummaries', 'tvtropes.clusters.txt')
    tv_tropes_columns = ['Character type', 'Description']
    tv_tropes= pd.read_csv(tvtropes_tsv, sep='\t', names=tv_tropes_columns)

    # transfrom the 'Description' column
    parsed_data = tv_tropes['Description'].apply(parse_json_column)

    # create new columns
    tv_tropes = pd.concat([tv_tropes, parsed_data.apply(pd.Series)], axis=1)

    tv_tropes = tv_tropes.rename(columns={
        'char': 'Character Name',
        'movie': 'Movie title',
        'id': 'ID',
        'actor': 'Actor'
    })

    return tv_tropes

def get_df_with_tv_tropes(df, tv_tropes):

    df_with_tv_tropes = pd.merge(df, 
                                tv_tropes[['Movie title', 'Actor', 'Character type']], 
                                left_on=['Name', 'Actor Name'], 
                                right_on=['Movie title', 'Actor'], 
                                how='left')
    return df_with_tv_tropes
