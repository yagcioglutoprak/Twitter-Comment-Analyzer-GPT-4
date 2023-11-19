import tweepy
import re
import time
import openai
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import requests
import pytesseract
import cv2
import numpy as np 
from pyChatGPT import ChatGPT


load_dotenv()
use_unofficial_api = False


def analyze_image_with_vision_api(image_url):
    """
    Analyze an image using GPT-4 Vision API to understand what it contains.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",  # Assuming this is the model for the GPT-4 vision tasks
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0]['message']['content']

def get_comments(browser, url):
    scroll_threshold = 7
    scroll = 0 
    browser.get(url)
    time.sleep(3)
    comments = []
    media_url =""
    try:
     # Wait for the media container to load
     wait = WebDriverWait(browser, 5)
     target_divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.css-1dbjc4n.r-1niwhzg.r-vvn4in.r-u6sd8q.r-4gszlv.r-1p0dtai.r-1pi2tsx.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-13qz1uu.r-1wyyakw")))

     for target_div in target_divs:
    # Extract the style tag value
      style = target_div.get_attribute("style")

    # Extract the URL from the style value
      match = re.search(r'url\("(.*?)"\)', style)
      if match:
        media_url = match.group(1)

        # Check if the URL contains "media" text
        if "media" in media_url:
            media_url = analyze_image_with_vision_api(media_url)
            print(media_url)
            break
        else:
         print("No div with media URL found.")


    except:

     print("No media found.")
    token_size = 0 
    while True:
        if scroll>scroll_threshold:
            break  
        soup = BeautifulSoup(browser.page_source, "html.parser")
        new_comments = soup.find_all("div", {"class": "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"})
        if not new_comments:
            break
        for comment in new_comments:
         if comment.text not in comments:
          comment_size = len(comment.text.split(" "))
          print(token_size)
          if (token_size + comment_size) > 800:
            break      
          comments.append(comment.text)
          token_size += comment_size
          if (token_size + comment_size) > 800:
            break  
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll = scroll+1
        time.sleep(1)
    #print(comments)
    browser.close()    
    return comments,media_url

def preprocess_comment(comment):
    comment = comment.lower()
    comment = re.sub(r'http\S+', '', comment)
    comment = re.sub(r'[^\w\s]', '', comment)
    return comment

def main():
    tweet_id = input("Tweet Id: ")
    tweet_url = f"https://twitter.com/MonsterBudsNFT/status/{tweet_id}"
    options = webdriver.ChromeOptions()
    
    browser = webdriver.Chrome(ChromeDriverManager().install())

    comments,media_url = get_comments(browser, tweet_url)
    preprocessed_comments = [preprocess_comment(c) for c in comments]
    #print(preprocessed_comments)

    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    client = tweepy.Client(os.environ.get("TWITTER_KEY_V2"))
    tweet = client.get_tweet(tweet_id, expansions=None, media_fields=None, place_fields=None, poll_fields=None, tweet_fields=None, user_fields=None, user_auth=False).data

    openai.api_key = os.environ.get("OPENAI_KEY")
    if use_unofficial_api == False:
        # Create a list of messages for the conversation history
     conversation = [
        {"role": "system", "content": "You are a helpful assistant analyzing tweet comments."},
        {"role": "user", "content": f"Analyse comments of the main tweet, make inferences and write a text that explains the general idea of all comments. Emphasize the general emotion and rate it by percentage at the end. If the main tweet has an image, provide a text version. Answer in the tweet's language. Main Tweet's Image Text: '{media_url}'. Main Tweet: '{tweet}'. Comments: '{preprocessed_comments}'."}
     ]

     response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=conversation
     )
     generated_response = response['choices'][0]['message']['content']

     print(generated_response)
    
    else:
     session = os.environ.get("CHATGPT_SESSION")
     api = ChatGPT(session,moderation=False)
     prompt=f"Analyse comments of the main tweet,make inferences and write a text that explains the general idea of all comments, step by step. Also,write general emotion and the rate by '%' end of the line. If main tweet has a image,you will get 'image-to-text' converted string. If main tweet doesn't contains a image you will get blank string. Answer with main tweet's language. Text Of Main Tweet's Image : '{media_url}'. Main Tweet: '{tweet}'. Comments are seperated with '' chracter. Comments: '{preprocessed_comments}'.",
     resp = api.send_message(prompt)
     #print(prompt)
     print(resp['message'])

    

if __name__ == "__main__":
    main()






