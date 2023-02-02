# Twitter Comment Analyzer
Are you tired of reading through endless comments on Twitter to find out what people are saying? Look no further! Our Twitter Comment Analyzer uses cutting-edge AI technology to analyze comments on a specific tweet and generate a comprehensive summary.


https://user-images.githubusercontent.com/40343443/215698367-8aae6a0c-eaec-4b62-8de0-1c6dc8638495.mp4


Here's how it works:

1. First, enter the tweet ID of the tweet you want to analyze.
2. Our script then uses Selenium and BeautifulSoup to extract all the comments on the tweet.
3. The comments are then preprocessed to remove any URLs, punctuations, and converted to lowercase.
4. The preprocessed comments are then fed into OpenAI's language model, where it generates a text that explains the general idea of all the comments.
5. And voila! You now have a summarized version of all the comments on the tweet.

*Note: If the main tweet has an image, our script also uses image recognition to generate a text representation of the image. The text representation is then included in the prompt to OpenAI, providing additional context for the summary.

*Exciting update: Script now has the option to use ChatGPT via "use_unofficial_api" variable. Set to true for NLP analysis with ChatGPT, false for analysis with GPT-3 (text-davinci-003). More versatility and enhanced capabilities with this added feature.


## Prerequisites
- Install the required packages by running `pip install tweepy re time openai bs4 selenium webdriver_manager dotenv`
- Create a .env file in the root directory and add the following keys:
  - TWITTER_KEY_V2
  - OPENAI_KEY

## Running the script
1. Open the terminal/command prompt
2. Navigate to the directory containing the script
3. Run `python3 filename.py`
4. Enter the tweet ID when prompted.

## Conclusion
With the Twitter Comment Analyzer, you'll never miss out on what people are saying on Twitter again! Try it out today and see for yourself.
