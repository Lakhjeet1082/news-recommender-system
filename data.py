import pandas as pd
class data:
    def __init__(self):
        self.article=pd.read_csv('D:/news.tsv/Feed parser/Article.csv')
        self.user_data=pd.read_csv('D:/news.tsv/Feed parser/clickstream_data.csv')
        self.merged_df = pd.merge(self.user_data[['UserId', 'ArticleId_served', 'Time_Spent']], 
                            self.article[['Title','Description','article_id', 'Category','Link']], 
                            left_on='ArticleId_served', 
                            right_on='article_id', 
                            how='left')

        self.merged_df.drop(columns=['article_id'], inplace=True)
d1=data()

# print(d1.user_data.head(20))

# print(d1.merged_df)