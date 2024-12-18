import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# Usefull variables
custom_palette = [
    "#ff6f00",  # Orange ajusté
    "#fc8c02",  # Orange différent
    "#e000ff",  # Magenta ajusté
    "#a302ff",  # Violet ajusté
    "#1a1a1a",  # Noir adouci (gris foncé)
    "#00b3ff",  # Cyan vif
    "#f5e942",  # Jaune éclatant
    "#4cff00",  # Vert néon
    "#ff0073",  # Rose vif
    "#6a0dad",  # Violet profond
    "#ff4500",  # Rouge-orangé éclatant
    "#00ff7f",  # Vert printemps
    "#8b00ff",  # Violet
    "#ffd700",  # Or
    "#1e90ff",  # Bleu dodger
    "#ff1493",  # Rose foncé
    "#32cd32",  # Vert lime
    "#ff6347",  # Tomate
    "#40e0d0",  # Turquoise
    "#ffcccb"   # Corail clair
]

triggers_list = ['someone dies', 'the ending is sad', 'religion is discussed', 'a kid dies',
                "there's torture", 'there are jump scares', "there's flashing lights or images",
                'shaky cam is used', "there's screaming"]

# Usefull functions
def df_movies_after_1950(df):
    df = df.dropna(subset=['Date'])
    df = df.replace(0, np.nan)
    df = df[df['Date'] > 1950]

    return df

def get_triggers_counts(df):
    trigger_counts = df.groupby('Date').sum()

    return trigger_counts

def get_content_correlation_matrix(df):

    df = pd.DataFrame({
    'Possession': df["someone is possessed"],
    'Ghosts':df["there's ghosts"] ,
    'Shower': df["there are shower scenes"] ,
    'Religion': df['religion is discussed'],
    'Stroke': df['someone has a stroke'],
    'Kid dies': df['a kid dies'] ,
    'Someone dies': df['someone dies'],
    'Abusive parents': df["there's abusive parents"],
    'Someone is restrained': df["someone is restrained"],
    'Torture': df["there's torture"] ,
    'Hell': df["there's demons or Hell"] 
    })

    return df.corr()

def get_correlation_matrix_trigger_counts(df, trigger_counts):

    compte = df.groupby('Date').size().reset_index(name='count')

    df = pd.DataFrame({
    'Possession': trigger_counts["someone is possessed"].values / compte['count'],
    'Ghosts': trigger_counts["there's ghosts"].values / compte['count'],
    'Shower': trigger_counts["there are shower scenes"].values / compte['count'],
    'Religion': trigger_counts['religion is discussed'].values / compte['count'],
    'Stroke': trigger_counts['someone has a stroke'].values / compte['count'],
    'Kid dies': trigger_counts['a kid dies'].values / compte['count'],
    'Someone dies': trigger_counts['someone dies'].values / compte['count'],
    'Abusive parents': trigger_counts["there's abusive parents"].values / compte['count'],
    'Someone is restrained': trigger_counts["someone is restrained"].values / compte['count'],
    'Torture': trigger_counts["there's torture"].values / compte['count'],
    'Hell': trigger_counts["there's demons or Hell"].values / compte['count']
    })

    return df.corr()


# Plot functions
def plot_movies_per_year(df, trigger_counts):

    compte = df.groupby('Date').size().reset_index(name='count')
    plt.figure(figsize=(10, 6))
    plt.bar(compte['Date'], compte['count'], color=custom_palette[3])
    plt.xlabel('Year')
    plt.style.use('dark_background')
    plt.ylabel('Number of movies')
    plt.title('Number of movies per year')
    plt.xticks(rotation=45)  
    plt.show()

def plot_movies_contents_number(df, trigger_counts):

    fig, axs = plt.subplots(7, 3, figsize=(20, 30))  

    triggers_to_plot1 = ["a child is abandoned by a parent or guardian", "an animal is abandoned"]
    for i, trigger in enumerate(triggers_to_plot1):
        axs[0, 0].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[0, 0].set_ylabel("Number of movies with this element")
    axs[0, 0].set_title("Abandonment")
    axs[0, 0].legend()

    triggers_to_plot2 = ["there's abusive parents"]
    for i, trigger in enumerate(triggers_to_plot2):
        axs[0, 1].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[0, 1].set_title("Familial violences")
    axs[0, 1].legend()

    triggers_to_plot3 = ["there's addiction", "someone uses drugs", "someone overdoses"]
    for i, trigger in enumerate(triggers_to_plot3):
        axs[0, 2].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[0, 2].set_title("Addiction")
    axs[0, 2].legend()

    triggers_to_plot4 = ["rape is mentioned", "sexual assault on men is a joke", "someone is restrained", "someone is held under water", "someone is beaten up by a bully", "someone's mouth is covered"]
    for i, trigger in enumerate(triggers_to_plot4):
        axs[1, 0].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 0].set_ylabel("Number of movies with this element")
    axs[1, 0].set_title("Violences")
    axs[1, 0].legend()

    triggers_to_plot5 = ["there's excessive gore", "there's genital trauma/mutilation", "there's torture", "heads get squashed", "teeth are damaged", "there's finger/toe mutilation", "there's body horror", "someone is burned alive", "there's cannibalism", "someone's throat is mutilated", "someone is crushed to death"]
    for i, trigger in enumerate(triggers_to_plot5):
        axs[1, 1].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 1].set_title("Bloody Violences")
    axs[1, 1].legend()

    triggers_to_plot6 = ["a kid dies", "an infant is abducted"]
    for i, trigger in enumerate(triggers_to_plot6):
        axs[1, 2].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 2].set_title("Children")
    axs[1, 2].legend()

    triggers_to_plot7 = ["a non-human character dies", "a major character dies", "someone dies", "someone sacrifices themselves"]
    for i, trigger in enumerate(triggers_to_plot7):
        axs[2, 0].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[2, 0].set_title("Death")
    axs[2, 0].legend()

    triggers_to_plot8 = ["a kid dies", "someone dies"]
    for i, trigger in enumerate(triggers_to_plot8):
        axs[2, 1].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[2, 1].set_title("Total death & child death")
    axs[2, 1].legend()

    triggers_to_plot9 = ["someone disabled played by able-bodied", "the r-slur is used"]
    for i, trigger in enumerate(triggers_to_plot9):
        axs[2, 2].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[2, 2].set_title("Disabiltiy")
    axs[2, 2].legend()

    triggers_to_plot10 = ["there are jump scares", "someone is possessed", "there are clowns", "there are shower scenes", "there's ghosts", "there are mannequins", "there's natural bodies of water"]
    for i, trigger in enumerate(triggers_to_plot10):
        axs[3, 0].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[3, 0].set_ylabel("Number of movies with this element")
    axs[3, 0].set_title("Fears")
    axs[3, 0].legend()

    triggers_to_plot11 = ["There's audio gore", "someone is eaten", "someone wets/soils themselves", "there's farting", "there's spitting", "someone poops on-screen", "someone vomits"]
    for i, trigger in enumerate(triggers_to_plot11):
        axs[3, 1].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[3, 1].set_title("Disgust")
    axs[3, 1].legend()

    triggers_to_plot12 = ["there are 9/11 depictions", "there's incarceration"]
    for i, trigger in enumerate(triggers_to_plot12):
        axs[3, 2].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[3, 2].set_title("Crimes")
    axs[3, 2].legend()

    colonnes_interval13 = trigger_counts.loc[:, 'a trans person is depicted predatorily': "there's bisexual cheating"]
    triggers_to_plot13 = colonnes_interval13.columns.tolist()
    for i, trigger in enumerate(triggers_to_plot13):
        axs[4, 0].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 0].set_ylabel("Number of movies with this element")
    axs[4, 0].set_title("LGBTQ+")
    axs[4, 0].legend()

    triggers_to_plot14 = ["needles/syringes are used", "someone has an eating disorder", "a mentally ill person is violent", "there's misophonia", "autism is misrepresented", "there's body dysmorphia", "someone has an anxiety attack", "reality is unstable or unhinged", "there's dissociation, depersonalization, or derealization", "D.I.D. Misrepresentation", "there's a claustrophobic scene", "someone has a mental illness", "someone self harms", "Someone attempts suicide", "someone dies by suicide"]
    for i, trigger in enumerate(triggers_to_plot14):
        axs[4, 1].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[4, 1].set_title("Medical")
    axs[4, 1].legend()

    triggers_to_plot15 = ["there's flashing lights or images", "shaky cam is used", "there are sudden loud noises", "there's screaming", "there is obscene language/gestures"]
    for i, trigger in enumerate(triggers_to_plot15):
        axs[4, 2].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[4, 2].set_title("Distressing systems")
    axs[4, 2].legend()

    triggers_to_plot16 = ["someone has an abortion", "a pregnant person dies", "there's childbirth", "someone miscarries", "there is a baby or unborn child", "a baby is stillborn"]
    for i, trigger in enumerate(triggers_to_plot16):
        axs[5, 0].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[5, 0].set_ylabel("Number of movies with this element")
    axs[5, 0].set_title("Pregnancy")
    axs[5, 0].legend()

    triggers_to_plot17 = ["there's fat jokes", "there's ableist language or behavior", "someone says the n-word", "an LGBT person dies", "there's antisemitism", "a minority is misrepresented", "the black guy dies first", "someone speaks hate speech", "there are homophobic slurs", "there's blackface","someone is misgendered"]
    for i, trigger in enumerate(triggers_to_plot17):
        axs[5, 1].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[5, 1].set_title("Discrimination")
    axs[5, 1].legend()

    triggers_to_plot18 = ["there's demons or Hell", "religion is discussed"]
    for i, trigger in enumerate(triggers_to_plot18):
        axs[5, 2].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[5, 2].set_title("Religion")
    axs[5, 2].legend()

    triggers_to_plot19 = ["someone has dementia/Alzheimer's", "someone is terminally ill", "someone has a stroke", "someone has a chronic illness"]
    for i, trigger in enumerate(triggers_to_plot19):
        axs[6, 0].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[6, 0].set_ylabel("Number of movies with this element")
    axs[6, 0].set_title("Disease")
    axs[6, 0].legend()

    triggers_to_plot20 = ["the ending is sad"]
    for i, trigger in enumerate(triggers_to_plot20):
        axs[6, 1].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[6, 1].set_title("Sad end")
    axs[6, 1].legend()

    triggers_to_plot21 = ["a person is hit by a car", "a car crashes", "a car honks or tires screech", "a plane crashes"]
    for i, trigger in enumerate(triggers_to_plot21):
        axs[6, 2].plot(trigger_counts.index, trigger_counts[trigger], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[6, 2].set_title("Transport")
    axs[6, 2].legend()

    plt.tight_layout()
    plt.show()

def plot_movies_contents_proportion(df, trigger_counts):

    compte = df.groupby('Date').size().reset_index(name='count')
    fig, axs = plt.subplots(7, 3, figsize=(20, 30))  
    plt.style.use('dark_background')

    triggers_to_plot1 = ["a child is abandoned by a parent or guardian", "an animal is abandoned"]
    for i, trigger in enumerate(triggers_to_plot1):
        axs[0, 0].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[0, 0].set_ylabel("Fraction of movies with this element")
    axs[0, 0].set_title("Abandonment")
    axs[0, 0].legend()

    triggers_to_plot2 = ["there's abusive parents"]
    for i, trigger in enumerate(triggers_to_plot2):
        axs[0, 1].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[0, 1].set_title("Familial violences")
    axs[0, 1].legend()

    triggers_to_plot3 = ["there's addiction", "someone uses drugs", "someone overdoses"]
    for i, trigger in enumerate(triggers_to_plot3):
        axs[0, 2].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[0, 2].set_title("Addiction")
    axs[0, 2].legend()

    triggers_to_plot4 = ["rape is mentioned", "sexual assault on men is a joke", "someone is restrained", "someone is held under water", "someone is beaten up by a bully", "someone's mouth is covered"]
    for i, trigger in enumerate(triggers_to_plot4):
        axs[1, 0].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 0].set_ylabel("Fraction of movies with this element")
    axs[1, 0].set_title("Violences")
    axs[1, 0].legend()

    triggers_to_plot5 = ["there's excessive gore", "there's genital trauma/mutilation", "there's torture", "heads get squashed", "teeth are damaged", "there's finger/toe mutilation", "there's body horror", "someone is burned alive", "there's cannibalism", "someone's throat is mutilated", "someone is crushed to death"]
    for i, trigger in enumerate(triggers_to_plot5):
        axs[1, 1].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 1].set_title("Bloody Violences")
    axs[1, 1].legend()

    triggers_to_plot6 = ["a kid dies", "an infant is abducted"]
    for i, trigger in enumerate(triggers_to_plot6):
        axs[1, 2].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 2].set_title("Children")
    axs[1, 2].legend()

    triggers_to_plot7 = ["a non-human character dies", "a major character dies", "someone dies", "someone sacrifices themselves"]
    for i, trigger in enumerate(triggers_to_plot7):
        axs[2, 0].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[2, 0].set_title("Death")
    axs[2, 0].legend()

    triggers_to_plot8 = ["a kid dies", "someone dies"]
    for i, trigger in enumerate(triggers_to_plot8):
        axs[2, 1].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[2, 1].set_title("Total death & child death")
    axs[2, 1].legend()

    triggers_to_plot9 = ["someone disabled played by able-bodied", "the r-slur is used"]
    for i, trigger in enumerate(triggers_to_plot9):
        axs[2, 2].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[2, 2].set_title("Disabiltiy")
    axs[2, 2].legend()

    triggers_to_plot10 = ["there are jump scares", "someone is possessed", "there are clowns", "there are shower scenes", "there's ghosts", "there are mannequins", "there's natural bodies of water"]
    for i, trigger in enumerate(triggers_to_plot10):
        axs[3, 0].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[3, 0].set_ylabel("Fraction of movies with this element")
    axs[3, 0].set_title("Fears")
    axs[3, 0].legend()

    triggers_to_plot11 = ["There's audio gore", "someone is eaten", "someone wets/soils themselves", "there's farting", "there's spitting", "someone poops on-screen", "someone vomits"]
    for i, trigger in enumerate(triggers_to_plot11):
        axs[3, 1].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[3, 1].set_title("Disgust")
    axs[3, 1].legend()

    triggers_to_plot12 = ["there are 9/11 depictions", "there's incarceration"]
    for i, trigger in enumerate(triggers_to_plot12):
        axs[3, 2].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[3, 2].set_title("Crimes")
    axs[3, 2].legend()

    colonnes_interval13 = trigger_counts.loc[:, 'a trans person is depicted predatorily': "there's bisexual cheating"]
    triggers_to_plot13 = colonnes_interval13.columns.tolist()
    for i, trigger in enumerate(triggers_to_plot13):
        axs[4, 0].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[1, 0].set_ylabel("Fraction of movies with this element")
    axs[4, 0].set_title("LGBTQ+")
    axs[4, 0].legend()

    triggers_to_plot14 = ["needles/syringes are used", "someone has an eating disorder", "a mentally ill person is violent", "there's misophonia", "autism is misrepresented", "there's body dysmorphia", "someone has an anxiety attack", "reality is unstable or unhinged", "there's dissociation, depersonalization, or derealization", "D.I.D. Misrepresentation", "there's a claustrophobic scene", "someone has a mental illness", "someone self harms", "Someone attempts suicide", "someone dies by suicide"]
    for i, trigger in enumerate(triggers_to_plot14):
        axs[4, 1].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[4, 1].set_title("Medical")
    axs[4, 1].legend()

    triggers_to_plot15 = ["there's flashing lights or images", "shaky cam is used", "there are sudden loud noises", "there's screaming", "there is obscene language/gestures"]
    for i, trigger in enumerate(triggers_to_plot15):
        axs[4, 2].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[4, 2].set_title("Distressing systems")
    axs[4, 2].legend()

    triggers_to_plot16 = ["someone has an abortion", "a pregnant person dies", "there's childbirth", "someone miscarries", "there is a baby or unborn child", "a baby is stillborn"]
    for i, trigger in enumerate(triggers_to_plot16):
        axs[5, 0].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[5, 0].set_ylabel("Fraction of movies with this element")
    axs[5, 0].set_title("Pregnancy")
    axs[5, 0].legend()

    triggers_to_plot17 = ["there's fat jokes", "there's ableist language or behavior", "someone says the n-word", "an LGBT person dies", "there's antisemitism", "a minority is misrepresented", "the black guy dies first", "someone speaks hate speech", "there are homophobic slurs", "there's blackface","someone is misgendered"]
    for i, trigger in enumerate(triggers_to_plot17):
        axs[5, 1].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[5, 1].set_title("Discrimination")
    axs[5, 1].legend()

    triggers_to_plot18 = ["there's demons or Hell", "religion is discussed"]
    for i, trigger in enumerate(triggers_to_plot18):
        axs[5, 2].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[5, 2].set_title("Religion")
    axs[5, 2].legend()

    triggers_to_plot19 = ["someone has dementia/Alzheimer's", "someone is terminally ill", "someone has a stroke", "someone has a chronic illness"]
    for i, trigger in enumerate(triggers_to_plot19):
        axs[6, 0].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[6, 0].set_ylabel("Fraction of movies with this element")
    axs[6, 0].set_title("Disease")
    axs[6, 0].legend()

    triggers_to_plot20 = ["the ending is sad"]
    for i, trigger in enumerate(triggers_to_plot20):
        axs[6, 1].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[6, 1].set_title("Sad end")
    axs[6, 1].legend()

    triggers_to_plot21 = ["a person is hit by a car", "a car crashes", "a car honks or tires screech", "a plane crashes"]
    for i, trigger in enumerate(triggers_to_plot21):
        axs[6, 2].plot(trigger_counts.index, trigger_counts[trigger].values /compte['count'], label=trigger, linewidth = 1, color = custom_palette[i]) 
    axs[6, 2].set_title("Transport")
    axs[6, 2].legend()

    plt.tight_layout()
    plt.show()

def plot_correlation_matrix(df):
    
    correlation_matrix = get_content_correlation_matrix(df)

    colors = ["#ff6f00", "#fc8c02", "#e000ff", "#6a0dad"]
    custom_cmap = mpl.colors.LinearSegmentedColormap.from_list("orange_to_violet", colors)

    plt.figure(figsize=(8, 6))  # Taille de la figure
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap=custom_cmap,
                cbar=True, square=True, linewidths=0.5, annot_kws={"size": 10})
    plt.title("Content correlation matrix in term of number of movies with same triggers over time", fontsize=14)
    plt.xticks(rotation=90)  # Rotation des labels des axes x
    plt.yticks(rotation=0)   # Rotation des labels des axes y
    plt.show()

def plot_correlation_matrix_counts(df, trigger_counts):
    
    correlation_matrix = get_correlation_matrix_trigger_counts(df, trigger_counts)
    colors = ["#ff6f00", "#fc8c02", "#e000ff", "#6a0dad"]
    custom_cmap = mpl.colors.LinearSegmentedColormap.from_list("orange_to_violet", colors)

    plt.figure(figsize=(8, 6))  # Taille de la figure
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap=custom_cmap,
                cbar=True, square=True, linewidths=0.5, annot_kws={"size": 10})
    plt.title("Content correlation matrix in term of number of movies with same triggers over time", fontsize=14)
    plt.xticks(rotation=90)  # Rotation des labels des axes x
    plt.yticks(rotation=0)   # Rotation des labels des axes y
    plt.show()

def plot_content_repartition(df):

    colors = ["#ff6f00", "#e000ff"]

    fix, axs = plt.subplots(3,3, figsize = (10,5))

    df['someone dies'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[0, 0], ylabel = '')
    axs[0,0].set_title('Movies with someone that dies')

    df['the ending is sad'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[0,1], ylabel = '')
    axs[0,1].set_title('Movies with a sad ending')

    df['religion is discussed'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[0,2], ylabel = '')
    axs[0,2].set_title('Movies with religion')

    df['a kid dies'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[1,0], ylabel = '')
    axs[1,0].set_title('Movies with a kid that dies')

    df["there's torture"].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[1,1], ylabel = '')
    axs[1,1].set_title('Movies with torture')

    df["there are jump scares"].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[1,2], ylabel = '')
    axs[1,2].set_title('Movies with jump scares')

    df["there's flashing lights or images"].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[2,0], ylabel = '')
    axs[2,0].set_title('Movies with flashing lights')

    df["shaky cam is used"].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[2,1], ylabel = '')
    axs[2,1].set_title('Movies with shaky cam')

    df["there's screaming"].value_counts().plot(kind='pie', autopct='%1.1f%%', colors = colors, ax = axs[2,2], ylabel = '')
    axs[2,2].set_title('Movies with screaming')

    plt.suptitle('Fraction of movies with specific triggers in HORROR movies')
    plt.tight_layout()
    plt.show()

def plot_trigger_apparition(df, triggers):

    fig, axs = plt.subplots(3, 3, figsize=(10, 6))
    colors = ["#ff6f00", "#e000ff"] 

    for i, trigger in enumerate(triggers_list):
        row, col = divmod(i, 3)
        percent_true_merged = (df[trigger].value_counts(normalize=True).get(True, 0) * 100)
        percent_true_triggers = (triggers[trigger].value_counts(normalize=True).get(True, 0) * 100)
        
        axs[row, col].bar(['Horror Movies', 'All movies'], [percent_true_merged, percent_true_triggers], color=colors)
        axs[row, col].set_title(trigger)
        axs[row, col].set_ylabel("Percentage (%)")

    plt.suptitle('Comparison of fraction of apparition of each trigger Between Horror dataset and whole dataset', fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

