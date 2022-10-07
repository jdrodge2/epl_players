import pandas as pd
from epl_players_scraper import *
from clean_epl_players import *

"""This script is the executable for gatering all of the data specified from the Premier League website"""

"""Change encoding of the csv file to 'ANSI' before opening in Excel to properly display accent characters on player
names. Chose not to script this as encoding would need to be changed back to UTF-8 before manipulating the read csv"""

# Used for Testing purposes
# player_urls = ["https://www.premierleague.com/players/4664/Hugo-Lloris/overview", "https://www.premierleague.com/players/3960/Harry-Kane/overview",
#                "https://www.premierleague.com/players/23033/Lucas-Torreira/overview", "https://www.premierleague.com/players/5758/Lucas-Digne/overview" ]
#
# club_names = ['All Clubs', 'Arsenal', 'Aston Villa', 'Brentford', 'Brighton and Hove Albion', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Leeds United',
#                   'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United', 'Newcastle United', 'Norwich City', 'Southampton', 'Tottenham Hotspur',
#                   'Watford', 'West Ham United', 'Wolverhampton Wanderers', 'Fulham', 'Sheffield United', 'West Bromwich Albion', 'AFC Bournemouth', 'Cardiff City',
#                   'Huddersfield Town', 'Stoke City', 'Swansea City']


bio_columns = ["Player ID", "Full Name", "Position", "Nationality", "Birthday", "Height(cm)", "Weight(kg)"]

stats_columns = ["Player ID", "Full Name", "Season", "Primary Club", "Secondary Club", "Appearances",
                "Wins", "Losses", "Goals", "Yellow cards", "Red cards", "Fouls", "Penalties scored", "Freekicks scored",
                "Shots", "Shots on target", "Shooting accuracy %", "Assists", "Passes per match", "Big chances missed",
                "Big Chances Created", "Own goals", "Goals Conceded", "Tackles", "Tackle success %", "Duels won", "Duels lost",
                "Successful 50/50s", "Aerial battles won", "Aerial battles lost", "Clean sheets", "Saves", "Penalties Saved",
                "Offsides"]
player_bio = []
player_stats = pd.DataFrame(columns=stats_columns)
player_id = 1

website = r'https://www.premierleague.com/players'
seasons = scrape_seasons_index(load_webpage(website)) #loads initial webpage and returns seasons dictionary
player_urls, club_names = scrape_player_urls_and_club_names(seasons) #takes season indexes and loads them into the url found within the script

for url in player_urls: #loops through all of the urls that werereturned

    #BELOW: calls scrape_player_overview and cleans then information scraped from the player overview page
    player_info, player_clubs_by_season, player_full_name = store_player_overview(url, player_id)
    player_bio.append(player_info)

    # BELOW: calls scrape_player_stats and cleans then information scraped from the player stats page
    player_stats = pd.concat([player_stats, store_player_stats(url, player_id, player_full_name,
                                                             player_clubs_by_season, seasons, club_names, stats_columns)])
    player_id += 1

player_bio = pd.DataFrame(player_bio, columns=bio_columns)

#BELOW: writes the collected data to two separate CSV files
player_bio.to_csv(r'C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\raw_player_biographical.csv', index=False)
player_stats.to_csv(r'C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\raw_player_stats.csv', index=False)

# #BELOW: reads back in the data from where it was stored
player_bio = pd.read_csv(r"C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\raw_player_biographical.csv")
player_stats = pd.read_csv(r"C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\raw_player_stats.csv")

# #BELOW: returns newly cleaned tables by player positon and biographies
attackers, midfielders, defenders, goalies = clean_player_info_by_position(player_bio, player_stats)
player_bio = clean_player_biographical(player_bio)

# #BELOW: writes tables to their own individual csv files
player_bio.to_csv(r"C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\player_biographical.csv", index=False, na_rep="\\N")
attackers.to_csv(r'C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\attacker_stats.csv', index=False)
midfielders.to_csv(r'C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\midfielder_stats.csv', index=False)
defenders.to_csv(r'C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\defender_stats.csv', index=False)
goalies.to_csv(r'C:\Users\1rodg\PycharmProjects\epl-players\venv\CSV Files\goalie_stats.csv', index=False)
