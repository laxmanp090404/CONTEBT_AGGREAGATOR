import shutil
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from textblob import TextBlob
import nltk
nltk.download('punkt')
#Function to print hypens till reaching the end of line
def print_hyphens_dynamic_width():
    terminal_width, _ = shutil.get_terminal_size()
    line_length = terminal_width - 1  
    for _ in range(line_length):
        print("-", end="")
    print()  
#passing the homepage link
url = "https://timesofindia.indiatimes.com/?from=mdr"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
}
response = requests.get(url, headers=headers)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
#finding links using the parent elements class
appId = soup.find(class_ = 'atWBy Q6d5H grid_wrapper')
nonAppView = appId.find_all("a")
links = []
#appending each article by scraping on the basis of anchor tag
for anchor in nonAppView:
    link_href = anchor.get("href") 
    links.append(link_href)
count=1
#performing operations on the article
for link in links:
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()

    # Extracting the text of the article
    text = article.text
    summary=article.summary
    article_title=article.title
    # Performing sentiment analysis using TextBlob
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

  

    if(sentiment > 0):
      sentiment_category="Positive"
    elif(sentiment<0):
      sentiment_category="Negative"
    else:
      sentiment_category="Neutral"
    # Printing the sentiment score
    print(f"Article Number {count}'s title:")
    print(article_title)
    print(f"Article Number {count}'s  Summary:\n")
    print(summary)
    print(f"Article Number {count}'s  Sentiment Score:", sentiment_category)
    count+=1
    print_hyphens_dynamic_width()
