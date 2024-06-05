# News Recommender System
This repository contains a News Recommender System project. It aims to provide personalized news recommendations to users based on their reading preferences and behavior. 

# Features
1. Content-Based Filtering: Recommends articles similar to those the user has interacted with based on the content of the articles.
2. Collaborative Filtering: Recommends articles based on the interactions of similar users (user-based) or similar articles (item-based).

# Data Preparation

**Article Data**: articles.csv has following columns:
- article_id: Unique identifier for the article
- Title: Title of the article
- Description: Description or content of the article
- Category: Category of the article
- Link: url of the article
- PublicationDate: Date the article was published

**Clickstream Data**: clickstream_data.csv has following columns:
- UserId: Unique identifier for the user
- SessionId: Unique identifier for the session
- ArticleId_served: The ID of the article served to the user
- Click: Whether the article was clicked ("Yes" or "No")
- Time_Spent: Time spent on the article in seconds

# Data Loading and Preprocessing
Load article data and preprocess it.
Load clickstream data and merge with article data for user interactions.

# Vectorization
TF-IDF and Word2Vec are used to create vectors for article descriptions.

# Content-Based Filtering
Calculate cosine similarity between the user profile (average of vectors of interacted articles) and all articles to recommend similar articles.

# Collaborative Filtering
Create a user-item matrix based on time spent on articles.
Calculate similarity between users or items to generate recommendations.

# User Interaction Logging
User interactions (clicks and time spent) are updated in interaction.csv for future recommendations.

**GUI** is made using Tkinter
