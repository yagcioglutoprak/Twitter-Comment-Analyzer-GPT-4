import tweepy
import re
import time
import openai
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv

load_dotenv()




def get_comments(browser, url):
    scroll_threshold = 7
    scroll = 0 
    browser.get(url)
    time.sleep(3)
    comments = []
    while True:
        if scroll>scroll_threshold:
            break  
        soup = BeautifulSoup(browser.page_source, "html.parser")
        new_comments = soup.find_all("div", {"class": "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"})
        if not new_comments:
            break
        for comment in new_comments:
         if comment.text not in comments:
          comments.append(comment.text)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll = scroll+1
        time.sleep(1)
    #print(comments)
    browser.close()    
    return comments

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

    comments = get_comments(browser, tweet_url)
    preprocessed_comments = [preprocess_comment(c) for c in comments]
    print(preprocessed_comments)

    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    client = tweepy.Client(os.environ.get("TWITTER_KEY_V2"))
    tweet = client.get_tweet(tweet_id, expansions=None, media_fields=None, place_fields=None, poll_fields=None, tweet_fields=None, user_fields=None, user_auth=False).data
    openai.api_key = os.environ.get("OPENAI_KEY")
    image_text = ""
    # Use the concatenated text as the prompt
    response = openai.Completion.create(
     engine="text-davinci-003",
     prompt=f"Analyse comments of the main tweet,make inferences and write a text that explains the general idea of all comments, step by step. Also,write general emotion and the rate by '%' end of the line. If main tweet has a image,you will get 'image-to-text' converted string. If main tweet doesn't contains a image you will get blank string. Respond with main tweet's language. Text Of Main Tweet's Image : '{image_text}' Main Tweet: '{tweet}'.Comments are seperated with '' chracter. Comments: '{preprocessed_comments}'.",
     max_tokens=1024,
     n=1,
     stop=None,
     temperature=0.5,
 )
    generated_response = response.choices[0].text
    prompt=f"Analyse comments of the main tweet,make inferences and write a text that explains the general idea of all comments, step by step. Also,write general emotion and the rate by '%' end of the line. If main tweet has a image,you will get 'image-to-text' converted string. If main tweet doesn't contains a image you will get blank string. Respond with main tweet's language. Text Of Main Tweet's Image : '{image_text}' Main Tweet: '{tweet}'.Comments are seperated with '' chracter. Comments: '{preprocessed_comments}'.",    print(prompt)
    print(generated_response)
    # Image recognition code here

    

if __name__ == "__main__":
    main()






