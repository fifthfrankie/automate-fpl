import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value
from fetch import fetch_fpl_data

# Fetch player data
df = fetch_fpl_data()

# Precompute player metrics
player_costs = df.set_index('id')['cost'].to_dict()
player_points = df.set_index('id')['total_points'].to_dict()
player_positions = df.set_index('id')['position'].to_dict()
player_teams = df.set_index('id')['team'].to_dict()

# Define the problem
model = LpProblem("FPL_Optimization", LpMaximize)

# Decision variables: whether to pick a player or not
player_vars = LpVariable.dicts("Player", df['id'], cat='Binary')

# Objective function: Maximize total points
model += lpSum(player_points[i] * player_vars[i] for i in df['id'])

# Constraints
# Budget constraint: Total cost must be <= £100 million
model += lpSum(player_costs[i] * player_vars[i] for i in df['id']) <= 100

# Position constraints
goalkeepers = [i for i, pos in player_positions.items() if pos == 'Goalkeeper']
defenders = [i for i, pos in player_positions.items() if pos == 'Defender']
midfielders = [i for i, pos in player_positions.items() if pos == 'Midfielder']
forwards = [i for i, pos in player_positions.items() if pos == 'Forward']

model += lpSum(player_vars[i] for i in goalkeepers) == 2
model += lpSum(player_vars[i] for i in defenders) == 5
model += lpSum(player_vars[i] for i in midfielders) == 5
model += lpSum(player_vars[i] for i in forwards) == 3

# Team constraint: No more than 3 players from any one team
for team in df['team'].unique():
    team_players = [i for i, t in player_teams.items() if t == team]
    model += lpSum(player_vars[i] for i in team_players) <= 3

model.solve()

print(f"Status: {model.status}")
print(f"Total Points: {value(model.objective)}")

# Extract selected players
selected_players = [i for i in df['id'] if player_vars[i].varValue == 1]
selected_df = df[df['id'].isin(selected_players)]
print(selected_df[['name', 'team', 'position', 'cost', 'total_points']])