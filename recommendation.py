from data import data
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse.linalg import svds

class recommendor:
    def __init__(self,user_id,article_data,user_data,merged):
        self.user_id = user_id
        self.article_data= article_data
        self.user_data= user_data
        self.merged= merged
        

    def content_based(self,num_recommendations=10):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        # Create a mapping from ArticleId to row index
        article_id_to_index = {article_id: idx for idx, article_id in enumerate(self.article_data['article_id'])}

        article_vectors = tfidf_vectorizer.fit_transform(self.article_data['Description'].values.astype('U'))
        user_profiles = {}
        # Generate user profiles
        for user_id, group in self.user_data.groupby('UserId'):
            article_ids = group.loc[group['Click'] == 'Yes', 'ArticleId_served']
            valid_indices = [article_id_to_index[article_id] for article_id in article_ids if article_id in article_id_to_index]
            if valid_indices:
                user_profile = article_vectors[valid_indices].mean(axis=0)
                user_profiles[user_id] = user_profile
        user_profile = user_profiles.get(self.user_id)
        if user_profile is None:
            print(f"User with ID {self.user_id} does not exist.")
            return
        
        user_profile = np.asarray(user_profile)
        similarity_scores = cosine_similarity(user_profile, article_vectors).flatten()
        top_indices = similarity_scores.argsort()[-num_recommendations:][::-1]
        recommended_articles = article_data.iloc[top_indices][['article_id', 'Title', 'Description','Link']]
        
        return recommended_articles

    def collaborative_filtering(self):
        user_item = self.merged.pivot_table(index  = 'UserId' , columns='ArticleId_served' , values='Time_Spent')
        user_item = user_item.fillna(0)
        user_item_matrix = user_item.values   # converting to matrix 
        U , sigma , V_T = svds(user_item_matrix , k  = 150) # applying svd
        sigma  = np.diag(sigma) # converting sigma to diagonal matrix 
        user_ratings = np.dot(np.dot(U , sigma ) , V_T) 
        scaler = MinMaxScaler()
        user_ratings_norm = scaler.fit_transform(user_ratings)
        items  = user_ratings_norm[self.user_id]
        item_idx=items.argsort()[::-1]
        title=[]
        des=[]
        link=[]
        id=[]
        count = 0
        for  i in item_idx:
            if count <10:
                id.append(self.merged['ArticleId_served'][i])
                title.append(self.merged['Title'][i])
                link.append(self.merged['Link'][i])
                des.append(self.merged['Description'][i])
                count+=1
            else:
                break
        df = pd.DataFrame()
        
        df['article_id']=id
        df['Title']= title
        df['Description']= des
        df['Link']= link
        return df    

        def random_recommendations(self, num_recommendations=10):
            return self.article_data.sample(num_recommendations)
            
    def news_recommender(self):
        if self.user_id in self.merged['UserId']:
            content_recommnendation = self.content_based()
            collaborative_recommendation =self.collaborative_filtering()
            lst1 = content_recommnendation.head(5)
            lst2= collaborative_recommendation.head(5)

            df1 = (pd.concat([lst1, lst2], axis=0)).reset_index()
            return df1     
                    
        else:
            random_recommendation = self.random_recommendations(10)
            return random_recommendation



d1= data()
article_data=d1.article
user_data = d1.user_data
merged = d1.merged_df

r1 = recommendor(111,article_data,user_data,merged)
recom=r1.news_recommender()
# print(recom)
