import requests

# API URL
url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=49ee266250fb4efe9d06edec49bbae3b"

# Fetching data
response = requests.get(url)

# Checking if the request was successful
if response.status_code == 200:
    # Parsing the response JSON
    data = response.json()
    
    # Extracting only the titles
    titles = [article['title'] for article in data['articles']]
    
    # Getting only the first three titles
    top_three_titles = titles[:3]
    
    # Formatting the titles with numbers
    formatted_titles = "\n".join([f"{i + 1}. {title}" for i, title in enumerate(top_three_titles)])
    
    # Printing the formatted titles
    print(formatted_titles)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
