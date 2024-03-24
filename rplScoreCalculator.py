import requests
import json
from RPL.extractPlayerInfo import (
    extract_combined_player_info,
)

base_url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/"

headers = {
    'authority': 'cricbuzz-cricket.p.rapidapi.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'expires': '0',
    'origin': 'https://rapidapi.com',
    'pragma': 'no-cache',
    'referer': 'https://rapidapi.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'usequerystring': 'true',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
    'x-rapidapi-key': '8a68681554msh2e734ec36aed65ep1762d5jsn7fb8822222b0',
    'x-rapidapi-ua': 'RapidAPI-Playground'
}

batsman_points = {'runs':1,'fours':1,'sixes':2,'duck':0,'fifty':20,'seventyfive':30,'hundred':50}
bowler_points = {'wickets':25,'maidens':8}

def get_match_info(matchId):
    url = base_url + matchId + "/scard"
    response = requests.get(url, headers=headers)
    response_data = response.json()
    with open('response.json', 'w') as file:
        # If you're sure it's JSON, use json.dump to write it directly as JSON
        import json
        json.dump(response_data, file, indent=4)

def calculate_player_points(player_data, matchId):
    total_points = {}

    for player_id, details in player_data.items():
        points = details.get("fielding_points",0)
        points += details.get("player_of_the_match_points",0)

        # Batting points
        runs = details.get('runs', 0)
        balls = details.get('balls', 0)
        fours = details.get('fours', 0)
        sixes = details.get('sixes', 0)
        strike_rate = details.get('strikeRate', 0)

        # Runs points
        points += runs
        if runs == 0 and balls != 0 :
            points -= 2  # Penalty for scoring 0 runs

        # Boundary points
        points += fours + (2 * sixes)

        # Milestone points
        if runs >= 50:
            points += 20
        elif runs >= 75:
            points += 30
        elif runs >= 100:
            points += 50

        # Bowling points
        wickets = details.get('wickets', 0)
        maidens = details.get('maidens',0)
        economy = details.get('economy',0)
        overs = details.get('overs',0)
        points += 25 * wickets + maidens * 8

        # Bonus points for multiple wickets
        if wickets == 3:
            points += 20
        elif wickets == 4:
            points += 30
        elif wickets > 4:
            points += 50  # Additional points for each wicket beyond 4

        #Strike Rate Points
        if runs > 0:
            if strike_rate > 200:
                points = points + 6
            elif strike_rate > 160:
                points = points + 4
            elif strike_rate > 140:
                points = points + 2

        #Strike Rate Penalty
        if runs > 0:
            if strike_rate <= 50:
                points = points - 6
            elif strike_rate <= 60:
                points = points - 4
            elif strike_rate <= 70:
                points = points - 2

        # Economy Points
        if overs > 0:
            if economy < 4:
                points = points + 12
            elif economy < 5:
                points = points + 8
            elif economy < 6:
                points = points + 4

        # Economy Penalty Points
        if overs > 0:
            if economy > 11:
                points = points - 12
            elif economy > 10:
                points = points - 8
            elif economy > 9:
                points = points - 4

        total_points[player_id] = points
        print(matchId,",",player_id,",",points)


if __name__ == "__main__":
    match_id = 89654
    #for match_id in 89654,89661,89665:
    get_match_info(str(match_id))
    match_data = {}
    with open('response.json') as file:
        match_data = json.load(file)
    player_info = extract_combined_player_info(match_data)  # Pass match_data to the function
    calculate_player_points(player_info, match_id)