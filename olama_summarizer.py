import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# Load environment variables
# load_dotenv(override=True)
# api_key = os.getenv("OPENAI_API_KEY")

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.title = soup.title.string if soup.title else 'no title found'
            for irrelevant in soup.body(['style', 'script', 'img', 'input']):
                irrelevant.decompose()
            self.content = soup.body.get_text(separator='\n', strip=True)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            self.title = 'Error Loading Page'
            self.content = 'Could not load page content.'


def user_prompt(website):
    user_promt = f"You are looing at a website titled {website.title}"
    user_promt += f"\n\nHere is the content of the website:\n{website.content}]\
        Please provide short summary of the website\n\n"
    # user_promt += "Please provide a summary of the website in markdown format."
    return user_promt

def message_for(website):
    return[
        {
            "role": "user",
            "content": user_prompt(website)
        }
    ]

OLLAMA_API = "http://localhost:11434/v1"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

def summarize_website(url):
    website = Website(url)
    ollama_via_openai = OpenAI(base_url=OLLAMA_API, api_key='allama')

    response = ollama_via_openai.chat.completions.create(
        model = MODEL,
        messages = message_for(website)
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    url = 'https://edwarddonner.com'
    summary = summarize_website(url)
    print(f"Summary of {url}:\n{summary}")

