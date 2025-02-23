import requests

# fetch data from fpl api
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)

# check if the request was successful
if response.status_code == 200:
    print("api request successful!")
else:
    print(f"api request failed with status code: {response.status_code}")
