import tweepy
import pytesseract
import requests

from PIL import Image
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import openai



client = tweepy.Client("TWITTER_KEY_V2")


# Get comments on a tweet
tweet_id = input("Tweet Id: ")

comments = []


    


def getComments(url):
 
 options = webdriver.ChromeOptions()
 options.add_argument('--disable-extensions')
 options.add_argument('--headless')
 user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
 options.add_argument(f'user-agent={user_agent}')





 browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

 # open tweet's page
 browser.get(url)
 time.sleep(3)
 SCROLL_PAUSE_TIME = 0.5
 scroll_threshold = 7
 scroll = 0 
# Get scroll height
 last_height = browser.execute_script("return document.body.scrollHeight")

 while True:
    if scroll>scroll_threshold:
        break    
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # find comments
    _comments = soup.find_all("div", {"class": "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"})

# print comments
    for comment in _comments:
     if comment not in comments:
      comments.append(comment.text)
      print(comment.text)
    #time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    
    last_height = new_height
    scroll = scroll+1
    
 


# parse HTML content with BeautifulSoup
 soup = BeautifulSoup(browser.page_source, "html.parser")

# find comments
 _comments = soup.find_all("div", {"class": "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"})

# print comments
 for comment in _comments:
    if comment not in comments:
     comments.append(comment.text)
     print(comment.text)

# close chromium browser
 browser.close()


getComments("https://twitter.com/Toprak_MCSG/status/"+tweet_id)






def preprocess_comment(comment):
    # Lowercase
    comment = comment.lower()
    # Remove URLs
    comment = re.sub(r'http\S+', '', comment)
    # Remove special characters
    comment = re.sub(r'[^\w\s]', '', comment)
    return comment

preprocessed_comments = [preprocess_comment(comment) for comment in comments]


tweet = client.get_tweet(tweet_id, expansions=None, media_fields=None, place_fields=None, poll_fields=None, tweet_fields=None, user_fields=None, user_auth=False).data
image_text = ""
# Check if the tweet has an image
#if "media" in status.entities:
#    media_url = status.entities["media"][0]["media_url_https"]
#    image = Image.open(requests.get(media_url, stream=True).raw)
#    image_text = pytesseract.image_to_string(image)


openai.api_key = "openai_key"
# Use the concatenated text as the prompt
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Analyse comments of the main tweet,make inferences and write a text that explains the general idea of all comments, step by step. If main tweet has a image,you will get 'image-to-text' converted string. If main tweet doesn't contains a image you will get blank string. Respond with main tweet's language. Text Of Main Tweet's Image : '{image_text}' Main Tweet: '{tweet}'.Comments are seperated with '' chracter. Comments: '{preprocessed_comments}'.",
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)
generated_response = response.choices[0].text
prompt=f"Analyse comments of the main tweet,make inferences and write a text that explains the general idea of all comments. If main tweet has a image,you will get 'image-to-text' converted string. If main tweet doesn't contains a image you will get blank string. Text Of Main Tweet's Image : '{image_text}' Main Tweet: '{tweet}'. Respond with main tweet's language. Comments are seperated with '' chracter. Comments: '{preprocessed_comments}'.",
print(prompt)
print(generated_response)




