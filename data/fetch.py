import requests
from bs4 import BeautifulSoup
import csv

# URL of the RSS feed
rss_url = 'https://www.thehindu.com/sci-tech/science/feeder/default.rss'

# Fetch the RSS feed content
response = requests.get(rss_url)
rss_content = response.content

# Parse the XML content using Beautiful Soup
soup = BeautifulSoup(rss_content, 'xml')

# Open the India.csv file for writing
with open('The_Hindu/Science.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Description', 'Link', 'Category', 'Publication Date'])

    # Iterate over the items in the feed
    for item in soup.find_all('item'):
        # Extract data from the item
        title = item.title.text.strip()
        description = item.description.text.strip()
        link = item.link.text.strip()
        category = item.category.text.strip()
        pub_date = item.pubDate.text.strip()

        # Write data to CSV file
        writer.writerow([title, description, link, category, pub_date])
