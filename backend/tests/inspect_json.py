import requests

# fetch data from fpl api
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)

# parse the json response
data = response.json()

# inspect the keys in the json data
print(data.keys())

# check if 'elements', 'teams', and 'element_types' exist
if "elements" in data and "teams" in data and "element_types" in data:
    print("data contains expected keys.")
else:
    print("missing expected keys in the data.")
