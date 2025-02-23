import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_fpl_data():
    cache_file = "fpl_data_cache.json"
    
    # Check if the cache file exists and is less than 1 day old
    if os.path.exists(cache_file):
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))
        if file_age < timedelta(days=1):  # Use cached data if it's less than 1 day old
            print("Using cached data...")
            return pd.read_json(cache_file)
    
    # Fetch "fresh" data from the API
    print("Fetching fresh data from FPL API...")
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Extract player data
    players = data['elements']
    teams = {team['id']: team['name'] for team in data['teams']}
    positions = {pos['id']: pos['singular_name'] for pos in data['element_types']}

    player_data = []
    for player in players:
        player_info = {
            'id': player['id'],
            'name': player['web_name'],
            'team': teams[player['team']],
            'position': positions[player['element_type']],
            'cost': player['now_cost'] / 10,  # Convert cost to millions
            'total_points': player['total_points'],
            'points_per_game': float(player['points_per_game']),
            'form': float(player['form']),
            'ict_index': float(player['ict_index']),
            'selected_by_percent': float(player['selected_by_percent'])
        }
        player_data.append(player_info)

    df = pd.DataFrame(player_data)
    
    # Save the data to the cache file
    df.to_json(cache_file, orient='records')
    return df