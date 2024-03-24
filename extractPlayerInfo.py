def extract_batter_info(match_data):
    player_info = {}
    for innings in match_data['scoreCard']:
        for batsman_key, batsman_details in innings['batTeamDetails']['batsmenData'].items():
            bat_id = str(batsman_details['batId'])
            player_info[bat_id] = batsman_details
            player_info[bat_id].update({"match_id": innings.get('matchId')})
    return player_info

def merge_bowler_info(match_data, player_info):
    for innings in match_data['scoreCard']:
        if 'bowlTeamDetails' in innings and 'bowlersData' in innings['bowlTeamDetails']:
            for bowler_key, bowler_details in innings['bowlTeamDetails']['bowlersData'].items():
                bowler_id = str(bowler_details['bowlerId'])
                bowler_details.pop('runs', None)
                if bowler_id in player_info:
                    player_info[bowler_id].update(bowler_details)
                else:
                    player_info[bowler_id] = bowler_details
    return player_info

def merge_fielder_info(match_data, player_info):
    for innings in match_data['scoreCard']:
        if 'batTeamDetails' in innings and 'batsmenData' in innings['batTeamDetails']:
            for batsman_key, batsman_details in innings['batTeamDetails']['batsmenData'].items():
                if batsman_details.get('outDesc', '') and batsman_details.get('outDesc') != "not out":
                    fielder1_id = str(batsman_details.get('fielderId1', 0))
                    fielder2_id = str(batsman_details.get('fielderId2', 0))

                    if fielder2_id == '0':
                        fielder_points = 10
                    else:
                        fielder_points = 5

                    for fielder_id in [fielder1_id, fielder2_id]:
                        if fielder_id not in player_info:
                            player_info[fielder_id] = {"fielding_points": fielder_points}
                        else:
                            if "fielding_points" not in player_info[fielder_id]:
                                player_info[fielder_id]["fielding_points"] = fielder_points
                            else:
                                player_info[fielder_id]["fielding_points"] += fielder_points
    return player_info

def mark_player_of_the_match(match_data, player_info):
    players_of_the_match = match_data['matchHeader']['playersOfTheMatch']
    for player in players_of_the_match:
        player_info[str(player.get('id'))].update({"player_of_the_match_points": 25})
    return player_info


def extract_combined_player_info(match_data):    
    player_info = extract_batter_info(match_data)
    player_info = merge_bowler_info(match_data, player_info)
    player_info = merge_fielder_info(match_data, player_info)
    player_info = mark_player_of_the_match(match_data, player_info)
    return player_info