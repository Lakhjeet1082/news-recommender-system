from recommendation import recommendor
from data import data 
import pandas as pd
import webbrowser
import datetime
import time
import os
from tkinter import *

start_time = None
current_article_id = None
current_link = None

def every_100(text):
    final_text = ""
    for i in range(len(text)):
        final_text += text[i]
        if (i + 1) % 100 == 0:
            final_text += "\n"
    return final_text

def open_article(user_id, article_id, link):
    global start_time, current_article_id, current_link
    start_time = time.time()  
    current_article_id = article_id
    current_link = link
    log_clickstream(user_id, article_id, link, "Yes", 0)  # Log the click with 0 time spent initially
    webbrowser.open(link)

# Function to stop the timer and log the time spent
def return_from_article(user_id):
    global start_time, current_article_id, current_link
    if start_time is not None:
        end_time = time.time()
        time_spent = int(end_time - start_time)  # Calculate the time spent
        update_clickstream(user_id, current_article_id, current_link, time_spent)  # Update the clickstream with the time spent
        start_time = None  # Reset the timer

# Function to log clickstream data
def log_clickstream(user_id, article_id, link, click, time_spent):
    timestamp = datetime.datetime.now()
    clickstream_entry = {
        'UserId': user_id,
        'ArticleId_served': article_id,
        'Click': click,
        'Time_Spent': time_spent,
        'Timestamp': timestamp
    }
    clickstream_df = pd.DataFrame([clickstream_entry])
    
    # Write header only if the file does not exist
    file_exists = os.path.isfile('D:/news.tsv/Feed parser/interaction.csv')
    clickstream_df.to_csv('D:/news.tsv/Feed parser/interaction.csv', mode='a', header=not file_exists, index=False)

# Function to update clickstream data with time spent
def update_clickstream(user_id, article_id, link, time_spent):
    try:
        clickstream_df = pd.read_csv('D:/news.tsv/Feed parser/interaction.csv')
        mask = (clickstream_df['UserId'] == user_id) & (clickstream_df['ArticleId_served'] == article_id)
        clickstream_df.loc[mask, 'Time_Spent'] = time_spent
        clickstream_df.to_csv('D:/news.tsv/Feed parser/interaction.csv', index=False)
    except pd.errors.ParserError as e:
        print(f"Error reading the CSV file: {e}")

# Create the Tkinter root window
root = Tk()
root.title("Recommended Articles")
root.geometry("1000x800")
root.configure(bg='#f0f0f0')  

user_id = 23
d1= data()
article_data=d1.article
user_data = d1.user_data
merged = d1.merged_df

r1 = recommendor(user_id,article_data,user_data,merged)
recommended_articles = r1.news_recommender()

if recommended_articles is not None:
    # Create a scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Create a canvas and connect it to the scrollbar
    canvas = Canvas(root, yscrollcommand=scrollbar.set, bg='#f0f0f0')
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=canvas.yview)

    # Create a frame within the canvas
    frame = Frame(canvas, bg='#f0f0f0')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Function to update the scroll region
    def on_configure(event):
        canvas.config(scrollregion=canvas.bbox('all'))

    # Bind the configure event to update the scroll region
    frame.bind('<Configure>', on_configure)

    # Create frames and labels to display the recommendations
    for idx, row in recommended_articles.iterrows():
        article_frame = Frame(frame, width=900, height=200, pady=10, padx=10, bg='white', bd=2, relief='groove')
        
        # Create a clickable title label
        title_label = Label(article_frame, text=row['Title'], font=("Helvetica", 16, "bold"), fg="#337833", bg='white', wraplength=850, justify=LEFT, padx=10, pady=5, cursor="hand2")
        title_label.pack(anchor="w")
        title_label.bind("<Button-1>", lambda e, user_id=user_id, article_id=row['article_id'], link=row['Link']: open_article(user_id, article_id, link))
        
        description_label = Label(article_frame, text=every_100(row['Description']), font=("Helvetica", 12), fg="#532555", bg='white', wraplength=850, justify=LEFT, padx=10, pady=5)
        description_label.pack(anchor="w")
        
        article_frame.pack(anchor="w", pady=5, padx=10)
    
    # Add a return button to log the time spent when returning
    return_button = Button(root, text="Return from Article", font=("Helvetica", 14), bg="#337833", fg="white",
                           command=lambda: return_from_article(user_id))
    return_button.pack(side=BOTTOM, pady=20)

root.mainloop()

