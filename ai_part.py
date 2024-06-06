
from openai import OpenAI
import requests
import json
from dotenv import load_dotenv
import os
import io
import base64
import markdown
import pandas as pd

load_dotenv()

client = OpenAI()

def parse_response_to_json(response_content):
    try:
        response_json = json.loads(response_content)
        return response_json
    except json.JSONDecodeError as e:
        print("Failed to parse JSON response:", e)
        return None

def get_news():
    params = {
        "engine": "google",
        "tbm": "nws",
        "q": "부동산 시장",
        "api_key": "ef7cf5ed8fde36c261b9ab294e3d03d09d0a3450af43065fab191e2b88c22bb3",
    }

    response = requests.get('https://serpapi.com/search', params=params)
    data = response.json()

    return data.get('news_results')


def write_news_to_file(news, filename):
    with open(filename, 'w') as file:
        for news_item in news:
            if news_item is not None:
                title = news_item.get('title', 'No title')
                snippet = news_item.get('snippet', 'No snippet')
                link = news_item.get('link', 'No link')
                file.write(f"Title: {title}\n")
                file.write(f"content: {snippet}\n")
                file.write(f"Link: {link}\n")
               
     
        
        
        
                
def get_data(company_name, company_ticker, period="1y", filename="korea_real_estate_market.txt"):
    news = get_news()
    if news:
        write_news_to_file(news, filename)
    else:
        print("No news found.")      

def financial_analyst():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role":
            "user",
            "content":" "
        }],
        functions=[{
            "name": "get_data",
            "description":
            "Get financial data on Korean real estate market for the purpose of analyzing liquidity risk management",
            "parameters": {
                "type": "object",
                "properties": {
                    "kr_market": {
                        "type":
                        "string",
                        "description":
                        "Korean real estate market",
                    },
                    },
                    "period": {
                        "type": "string",
                        "description": "The period of analysis"
                    },
                    "filename": {
                        "type": "string",
                        "description": "the filename to store data"
                    }
                },
                "required": ["kr_market"],
            }],
        function_call={"name": "get_data"}
    )

    message = response.choices[0].message

    if message.function_call:
        # Parse the arguments from a JSON string to a Python dictionary
        arguments = json.loads(message.function_call.arguments)

        # Parse the return value from a JSON string to a Python dictionary
        news = get_news()
        if news:
            write_news_to_file(news, "korea_real_estate_market.txt")
        else:
            print("No news found.")      

        with open("korea_real_estate_market.txt", "r") as file:
            content = file.read()[:14000]

        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "Analyze Korean real estate market"
                },
                message,
                {
                    "role": "system",
                    "content": """Summary and Suggest 5 most important news about Korean Estate Market
                    in terms of trading liquidity risk. You have to read all the news in the file and
                    find the most fitted news in terms of risk of the Korean Estate Market.
                    Your response must be just providing title(bold and large font), short summary and imarge url of the news, while new-spacing the line.
                    Title should be markdown-ed.
                    Number the news like 1,2,3,4,5 in the context of ranking of the importance.
                    Finally You summarize the 5 news in a paragraph.
                    Respond in Korean. 
                      """
                },
                {
                    "role": "assistant",
                    "content": content,
                },
            ],
        )
        text=markdown.markdown(second_response.choices[0].message.content)
        with open("content.md", 'w') as md_file:
            md_file.write(text)
            #file.write(f"content: {snippet}\n")
            #file.write(f"Link: {link}\n")

def generate_plan():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role":
            "user",
            "content":" "
        }],
        functions=[{
            "name": "get_data",
            "description":
            "Get financial data on Korean real estate market for the purpose of analyzing liquidity risk management",
            "parameters": {
                "type": "object",
                "properties": {
                    "kr_market": {
                        "type":
                        "string",
                        "description":
                        "Korean real estate market",
                    },
                    },
                    "period": {
                        "type": "string",
                        "description": "The period of analysis"
                    },
                    "filename": {
                        "type": "string",
                        "description": "the filename to store data"
                    }
                },
                "required": ["kr_market"],
            }],
        function_call={"name": "get_data"}
    )

    message = response.choices[0].message

    if message.function_call:
        # Parse the arguments from a JSON string to a Python dictionary
        arguments = json.loads(message.function_call.arguments)

        # Parse the return value from a JSON string to a Python dictionary
        news = get_news()
        if news:
            write_news_to_file(news, "korea_real_estate_market.txt")
        else:
            print("No news found.")      

        with open("korea_real_estate_market.txt", "r") as file:
            content = file.read()[:14000]

        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": "Analyze Korean real estate market"
                },
                message,
                {
                    "role": "system",
                    "content": """Given the news, read all the articles via link, and generate 3 contingency plans
                    that could hedge the trading liquidity risk as if you hold the real estate in Korea.
                    Provide what it is, advantages and disadvantages, and how to do that when suggesting the contingency plans.
                    Just provide about contingency plans, you don't have to provide title, overviews or conclusions or something else.
                    Don't respond other than the contingency plans. Don't respond other than the contingency plans.
                    Make it in the markdown form, with large and bold title of the plans.
                    Respond in Korean.
                    """
                },
                {
                    "role": "assistant",
                    "content": content,
                },
            ],
        )
        text=markdown.markdown(second_response.choices[0].message.content)
        with open("plans.md", 'w') as md_file:
            md_file.write(text)

