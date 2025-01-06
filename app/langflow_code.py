import os
import json
import requests
from dotenv import load_dotenv
import diskcache as dc
import pandas as pd


load_dotenv()
cache = dc.Cache('cache_directory')

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.environ.get("LANGFLOW_ID")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "social_stats"
CACHE_KEY = "all_data_from_langflow"
FORMATTED_DATA_KEY = "formated_all_data_from_langflow_key"

def run_flow(message: str) -> dict:
    try:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
        }
        
        headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()
    except Exception:
        return None


def format_run_flow_data(response):
    try:
        if response:
            try:
                message = response.get("outputs")[0].get("outputs")[0].get("results").get("message").get("text")
                return message
            except Exception as e:
                print(e)
                return {}
        else:
            print(f"Response Not Found for message for query in format_run_flow_data")
            return {}
    except Exception as e:
        print(f"something went wrong format_run_flow_data: {e}")


def get_response_from_langflow(query):

    prompt = """
        You are an expert in analyzing media posts and providing detailed and accurate information. 
        Your primary role is to utilize the provided tools to efficiently look up posts likes, comments, shares, engagement rate.
        Always aim to deliver clear, concise, and helpful responses, ensuring the user's needs are fully met. \n
        Response Format: Markdown
    """
    
    response = run_flow(f"{query} \n {prompt}")
    if response:
        try:
            response = format_run_flow_data(response=response)
            return response if response else ''
        except Exception as e:
            print(e)
            return ''
    else:
        print(f"Response Not Found for message for query: {query}")
        return ''



def get_all_data_from_langflow():

    query = "Get all data for Carousal, Reels, Static"

    prompt = """
        Generate a JSON response as a JSON string containing the extracted data. 
        Ensure the structure is easily parsable, 
        and provide only the JSON string as output without any additional text.
        Response format:
        {
            'posts': [
                {
                    'post_id': <post-id>,
                    'type': <post-type>,
                    'category': <post-category>,
                    'date_posted': <posted-date>,
                    'likes': <likes on post>,
                    'comments': <comments on post>,
                    'shares': <no of times post shared>
                },
                {
                    'post_id': <post-id>,
                    'type': <post-type>,
                    'category': <post-category>,
                    'date_posted': <posted-date>,
                    'likes': <likes on post>,
                    'comments': <comments on post>,
                    'shares': <no of times post shared>
                },
            ...
            ]
        }
    """

    # Check if data present in cache
    if cache.get(CACHE_KEY):
        return cache.get(CACHE_KEY)

    response = run_flow(f"query \n {prompt}")


    if response:
        try:
            message = response.get("outputs")[0].get("outputs")[0].get("results").get("message").get("text")
            data = json.loads(message)
            cache.set(CACHE_KEY, data, expire=3600)
            return data
        except Exception as e:
            print(e)
            return {}
    else:
        print(f"Response Not Found for message for query: {query}")
        return {}


def format_data():
    
    # Try fetching cached data
    cached_data = cache.get(FORMATTED_DATA_KEY)
    if cached_data:
        return cached_data 
    
    results = get_all_data_from_langflow()
    reels = 0
    carousel = 0
    static = 0
    tech = 0
    travel = 0
    food = 0
    fashion = 0
    likes = 0
    comments = 0
    shares = 0
    engagement_data = {}
    posts = []
    for post_list in results.values():
        for post in post_list:
            posts.append(post)
            # post type
            if post.get('type') == 'Reels':
                reels += 1
            if post.get('type') == 'Carousel':
                carousel += 1 
            if post.get('type') == 'Static':
                static += 1
            
            # post category
            if post.get('category') == 'Fashion':
                fashion += 1
            if post.get('category') == 'Travel':
                travel += 1
            if post.get('category') == 'Tech':
                tech += 1
            if post.get('category') == 'Food':
                food += 1

            # post engagement
            likes += post.get('likes', 0)
            comments += post.get('comments', 0)
            shares += post.get('shares', 0)
        
            post_date = post.get('date_posted', '')
            if post_date:
                if post_date not in engagement_data:
                    engagement_data[post_date] = {'likes': 0, 'comments': 0, 'shares': 0}

                # Accumulate the engagement metrics
                engagement_data[post_date]['likes'] += post.get('likes', 0)
                engagement_data[post_date]['comments'] += post.get('comments', 0)
                engagement_data[post_date]['shares'] += post.get('shares', 0)

    
    # Convert the data into a DataFrame
    df = pd.DataFrame(posts)

    # Calculate average engagement by post type
    avg_engagement = df.groupby('type').agg({
        'likes': 'mean',
        'comments': 'mean',
        'shares': 'mean'
    }).reset_index()

    category_avg_engagement = df.groupby('category').agg({
        'likes': 'mean',
        'comments': 'mean',
        'shares': 'mean'
    }).reset_index()

    # Create a DataFrame to prepare data for animation (combining the post type and engagement)
    post_type_engagement_df = pd.melt(avg_engagement, id_vars='type', value_vars=['likes', 'comments', 'shares'],
                            var_name='Engagement Type', value_name='Average Engagement')


    # Create a DataFrame to prepare data for animation (combining the post Category and engagement)
    post_category_engagement_df = pd.melt(category_avg_engagement, id_vars='category', value_vars=['likes', 'comments', 'shares'],
                            var_name='Engagement Type', value_name='Average Engagement')

    post_type_data = {
        "Reels": reels,
        "Carousel": carousel,
        "Static": static,
        "fashion": fashion,
        "travel": travel,
        "tech":tech,
        "food": food,
        "total_likes": likes,
        "total_comments": comments,
        "total_shares": shares
    }

    # Convert to DataFrame for easier manipulation
    engagement_df = pd.DataFrame.from_dict(engagement_data, orient='index')
    engagement_df['date'] = pd.to_datetime(engagement_df.index)
    engagement_df.reset_index(drop=True, inplace=True)

    # Store the result in cache for subsequent use
    cached_result = (post_type_data, engagement_df, post_type_engagement_df, post_category_engagement_df, df)
    cache.set(FORMATTED_DATA_KEY, cached_result, expire=3600)

    return post_type_data, engagement_df, post_type_engagement_df, post_category_engagement_df, df


# # Initialize the cache
# cache = dc.Cache('cache_directory')

# # Or clear the entire cache
# cache.clear()

# print("Cache key deleted or cache cleared.")