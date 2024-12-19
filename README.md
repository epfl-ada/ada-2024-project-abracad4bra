# Horror movies, the collective nightmares of society 

Welcome to the Horror Movie Museum!


## Final Website : https://valentinedelevaux.github.io/ada.github.io/

## Contributions :
Valentine Delevaux : Trigger Analysis, Graphisms of the characters and backgrounds of the website, Layout of the website, Texts of the website
Valentine Casalta : Content and World Analysis, Layout of the website, Texts of the website, Conversion of the plots in plotly
Julie Le Tallec : Titles and Diversity Analysis, Texts of the website, Graphisms of the portraits of the team
Elie Roth : Global events Analysis, Texts of the website
Marco Lourenço Leitao : World Analysis, Layout of the Notebook

## Abstract: 
Our project aims to explore the evolution of  horror movies as a reflection of societal fears and transformations. We believe that horror films are acting as the nightmares of society, allowing the audience to confront what scares them in a controlled, metaphorical space, and therefore offer a unique lens to examine collective fears. 
By analyzing horror themes across decades, we are looking at how shifting societal dynamics, such as technological advancements, cultural fears and moral concerns, manifest within this genre. Recent trends, like the rise of movies focused on AI, illustrate how horror adapts to contemporary issues, much as past horror movies reelected anxieties around religion, societal violence. 
This analysis aims to show how horror movies both respond to and shape societal fears and evolutions, ultimately offering insight into society's subconscious and its evolving concerns over time. 

The final project takes the form of an immersive story, where the reader becomes a visitor exploring Dracula's Museum of Horror Movies, guided by Dracula's loyal butler. The visitor journeys through various themed rooms, each dedicated to a unique subject of analysis within the horror genre.


## Research questions 
1- Do horror movies reflect societal evolution on diversity ? 
- How does the representation of diversity in horror movies compare to other film genres, and does this reveal the role of horror in reflecting societal changes?
- Within the horror genre, how have portrayals of diversity evolved over time in terms of actor representation, character tropes, and the descriptions provided in movie summaries ?

2- How did horror movies' scenarios evolve over time ? 
- General evolution of themes addressed 
- Analysis of different tropes and content 

3- Are there cultural specificities in horror ? 
- Are the themes addressed different around the world ? 
- Are horror movies as popular a genre everywhere ? 

4- Do historical events have an impact on horror movies scenarios ? 

## Methods 
1- To analyze how diversity in horror movies compares to other genres, we will collect data on gender and ethnicity of actors. We will use descriptive statistics (e.g., proportions) to summarize representation, and inferential tests like chi-square and ANOVA to determine if differences are statistically significant.
To analyze stereotypes in horror movie tropes and their evolution over time, we will examine character descriptions in movie summaries. We will try to extract patterns in words associated with characters' gender and ethnicity.

2- One of the axis of the content analysis is through the analysis of the triggering content that the movies possess. Using the trigger dataset from Doesthedogdie, we analyse the apparition of certain content in horror movies (like the apparition of ghosts, deaths, violence...). We visualize them over the year, and work on the correlation between each using a correlation matrix. Then, we analyse their frequency of apparition, and compare that to their frequency in other genres of movies to see if those kind of content are specific to horror movies.

3- In order to analyze the differences in the genre over the world we use a dictionary to map countries to different world regions and we define different list of keywords related to common themes. Using the keywords we're able to search through movie summaries and tag them with corresponding themes. 
When analyzing the popularity and recurrence of themes by region we're careful to normalize the data to take into account the size and production diffence of different regions.

4- For various topics (terrorism, flu epidemics, nuclear disaster, petrol, communism…), we are going to perform a similarity calculation between a vectorized list of keywords related to the topic and the vectorized summary of each horror movie. The vectorization is done through building and training a word embedding model. Some historically dependent events are retrieved through chat-GPT and statistical analysis (Mann-Whitney U test) is done to estimate the significance of the change in time of the topic-related horror movies during the period of historical events.

## Additional datasets
**Kaggle Horror movies dataset:**
This dataset contains information on 32k movies released between 1950 and 2022. We chose this dataset to complete the original data with more recent movies (fill the gap between 2016 and 2022) and have more movie plots to analyze as we previously only had ~5k horror movies. 

**Trigger warning dataset:**
This dataset comes from the website ‘Doesthedogdie.com’ that regroups a variety of triggering content for thousands of movies, series, books… The developers provided us with a csv file of the list of 50k movies between 1900 and today, and the kind of triggering content they have. 
The concept of studying triggering content (ex : blood, violence, clowns…) is closely related to horror movies, as these films often feature disturbing and frightening themes that may not be suitable for all audiences.
This dataset is then crossed with the other datasets we use for assuring we only keep horror movies.

## Proposed Timeline 
Beginning of the project: Repartition of the different subjects of the project & looking for new datasets (Julie : Introduction and metadata analysis + actor/trope repartition, Elie : Impact of important events on movie industry, Marco : Analysis of tropes and introduction, Valentine C: Analysis of the summaries/cultural specificities, Valentine D: movie content and triggers analysis)

14/11: Sharing of new datasets and beginning of the analysis for each 

21/11: Homework 2. All principal figures need to be chosen, qualitative analysis

28/11: Quantitative analysis and significance tests

05/12: Written analysis of each graph, website development

12/12: Redaction of the final project and aesthetic of the graphs/website

19/12: Proofreading + Final touch
