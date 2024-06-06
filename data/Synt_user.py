import numpy as np
import pandas as pd

# Load the article data without null descriptions
article_data = pd.read_csv('article_data_no_null.csv')

# Extract the valid ArticleId values
valid_article_ids = article_data['article_id'].unique()

num_users = 1000  
num_articles = len(valid_article_ids)  # Update the number of articles based on the valid article IDs
max_session_length = 10 
max_time_spent = 300  

clickstream_data = []
for user_id in range(1, num_users + 1):
    num_sessions = np.random.randint(1, 6)  
    for session_id in range(1, num_sessions + 1):
        session_length = np.random.randint(1, max_session_length + 1)
        interactions = np.random.choice(valid_article_ids, size=session_length, replace=False)
        for idx, article_id in enumerate(interactions, start=1):
            click = np.random.choice(['Yes', 'No'], p=[0.8, 0.2])  
            time_spent = np.random.randint(1, max_time_spent + 1) if click == 'Yes' else 0
            clickstream_data.append({
                'UserId': user_id,
                'SessionId': f"{user_id}_{session_id}",
                'ArticleId_served': article_id,
                'Click': click,
                'Time_Spent': time_spent
            })

clickstream_df = pd.DataFrame(clickstream_data)

# Save the clickstream data to a CSV file
clickstream_df.to_csv('D:/news.tsv/Feed parser/clickstream_data.csv', index=False)

print("Clickstream data generated and saved.")
