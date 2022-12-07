# Recommendation System For TVSeries
Our goal was to build a knowledge graph of television series. Using this knowledge graph, we built graph embeddings that helped us cluster similar series. This was used to build our recommendation system based on its similarity metric with other entities. We included cast, genre, release date, end date, producers, network, production company, plot, number of seasons, languages, rating, awards, and country of origin for each series. 
This project provides two features that recommend similar television series to users and allows them to query series as per their selection of genre and actors. 

To run imdb crawler-
1. cd Crawler/imdb
2. scrapy crawl tvseries

To run rotten tomatoes crawler-
1. cd Crawler/rotten
2. scrapy crawl rotten

Entity Linking code in EntityLinking folder

Recommender folder has the code for embedding generation and Recommendation App

FilesForAuraDB folder includes the files that were used to create the KG in AuraDB
