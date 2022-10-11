from epl_players_scraper import *
import pandas as pd
import re
import numpy as np


def change_column_Dtype(position_table):
    "helper method which recasts the column types in the player position dataframes"
    col_counter = 0
    for col in position_table.columns:
        if col_counter >= 5: #ignore the first 5 columns
            position_table[f"{col}"] = pd.to_numeric(position_table[f"{col}"])
            if col != "Passes per match": #only Passes per match should stay as type float
                position_table[f"{col}"] = position_table[f"{col}"].astype('Int64')
        col_counter += 1
    return position_table


def fix_club_name(club_names, name):
    """helper method which reformats the way club names were scraped to something cleaner"""

    for club in club_names:
        if not name.find(club):

            return club


def convert_yr_to_dict_key(year):
    """helper method to turn a season into a format that the seasons dictionary will recognize"""

    previous_yr = str(int(year) + 1)[-2:]
    key = year + f'/{previous_yr}'

    return key


def store_player_overview(url, player_id):
    """Uses method call to scape player overview page. Then insets the biographical data into a list. Returns this new list
    followed by other information collected from the overview page that is needed for the store_player_stats method"""

    player_full_name, player_information, player_clubs_by_season = scrape_player_overview(url)
    player_info = [np.nan] * 7

    player_info[0] = player_id
    player_info[1] = player_full_name
    player_info[2] = player_information.get("Position")
    player_info[3] = player_information.get("Nationality")

    birthday = None

    if type(player_information.get("Date of Birth")) == str:
        birthday = player_information.get("Date of Birth")

        if len(birthday) > 10:
            birthday = birthday[:-5] #removes the player age if given

    player_info[4] = birthday
    player_info[5] = player_information.get("Height")
    player_info[6] = player_information.get("Weight")

    return player_info, player_clubs_by_season, player_full_name


def store_player_stats(url, player_id, player_full_name, player_clubs_by_season, seasons, club_names, stats_columns):
    """Uses method call to scape the players stats page. Then inserts stastical data into a pandas dataframe and returns the dataframe """

    season_year = [year[:4] for year in seasons.keys()]
    player_stats = []
    season_tracker = [] # makes sure that if a season is duplicated, the extra line is writen to the secondary club column in the previous list
    counter = -1 #keeps track of how many times temp_list has been appended to player_stats

    for item in range(len(player_clubs_by_season)):

        #BELOW: since playerClubsBySeasons returns all of the seasons a player has ever played, this makes sure that it only
        #uses information from the specified seasons
        if player_clubs_by_season[item][0][:4] in season_year:
            if player_clubs_by_season[item][0] not in season_tracker: #Checks for duplicate seasons

                #BELOW: manipulates the url to link to the player stats page and calls the scraper function
                top_stat, normal_stat= scrape_player_stats(url[:-8]+f"stats?co=1&se={seasons[convert_yr_to_dict_key(player_clubs_by_season[item][0][:4])]}")

                temp_list = []
                temp_list.append(player_id)
                temp_list.append(player_full_name)
                temp_list.append(player_clubs_by_season[item][0])
                temp_list.append(fix_club_name(club_names, player_clubs_by_season[item][1]))
                temp_list.append(None)

                for i in range(5, len(stats_columns)):
                    if i < 8: #appends values found in topStat
                        temp_list.append(top_stat.get(stats_columns[i]))

                    else: #appends values found in normalStat
                        temp_list.append(normal_stat.get(stats_columns[i]))

                season_tracker.append(player_clubs_by_season[item][0])
                player_stats.append(temp_list)
                counter += 1

            else: #if a season is duplicated, club_name will get appended to the previous list, but only if it is a differnt club than the primary club
                club = fix_club_name(club_names, player_clubs_by_season[item][1])

                if club != player_stats[counter][3]:
                    player_stats[counter][4] = club


    return pd.DataFrame(player_stats, columns=stats_columns)


def clean_player_info_by_position(player_bio, player_stats):
    """Cleans the raw data stored in raw_player_stats.csv and creates 4 new dataframes based on player positions"""
    #BELOW: merges the tables to tell which player has what positon
    player_stats = pd.merge(player_stats, player_bio[["Position", "Player ID", "Full Name"]], on=["Player ID", "Full Name"])

    #BELOW: removes the percent sign from these columns
    player_stats["Shooting accuracy %"] = player_stats["Shooting accuracy %"].str[:-1]
    player_stats["Tackle success %"] = player_stats["Tackle success %"].str[:-1]

    #BELOW: scraper failed to collect data for 73 entries out of 3769 - or around 2% of all statistics
    did_not_collect_data_indexes = player_stats[player_stats["Wins"].isna()].index.tolist()
    player_stats.iloc[did_not_collect_data_indexes, 5:-1] = -1 #sets all rows where data was not colelcted to -1

    #BELOW: due to naming discrepancies on premier league website, scraper failed to pick up club names for the players at indexes specified
    player_stats.iloc[[490, 603, 834, 1125, 1537, 1941, 2490, 2863, 3111, 3410],[3]] = 'Brighton and Hove Albion'
    player_stats.iloc[[1879, 3182, 3253], [3]] = 'Bournemouth'

    player_stats["Secondary Club"].fillna("No Club", inplace=True) # replaces NaN values with a string

    #BELOW: creates and returns dataframes based on player position and deals with any left over NaN values
    defenders = player_stats[player_stats["Position"] == "Defender"]
    defenders = defenders.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,17,18,20,21,22,23,24,25,26,27,28,29,30,33]]
    defenders.fillna(0, inplace=True)
    defenders = change_column_Dtype(defenders)

    attackers = player_stats[player_stats["Position"] == "Forward"]
    attackers = attackers.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,23,33]]
    attackers = change_column_Dtype(attackers)

    midfielders = player_stats[player_stats["Position"] == "Midfielder"]
    midfielders = midfielders.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,23,24,25,26,27,28,29,33]]
    midfielders.fillna(0, inplace=True)
    midfielders = change_column_Dtype(midfielders)

    goalies = player_stats[player_stats["Position"] == "Goalkeeper"]
    goalies = goalies.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,17,18,21,22,30,31,32]]
    goalies = change_column_Dtype(goalies)

    return attackers, midfielders, defenders, goalies


def clean_player_biographical(player_bio):
    """This method only exists becasue I did not tell the scraper to store the information properly the first time around.
    I will use this method to remove the 'cm' and 'kg' from the height and weight columns and cast the column types over
    to int. Returns player_bio"""

    player_bio["Height(cm)"] = player_bio["Height(cm)"].str[:-2]
    player_bio["Weight(kg)"] = player_bio["Weight(kg)"].str[:-2]

    player_bio["Height(cm)"] = player_bio["Height(cm)"].astype("Int64")
    player_bio["Weight(kg)"] = player_bio["Weight(kg)"].astype("Int64")

    # Reformats birthdates to be in the yyyy-mm-dd notation
    player_bio["Birthday"] = player_bio["Birthday"].str[-4:] + "-" + player_bio["Birthday"].str[3:5] + "-" + player_bio["Birthday"].str[:2]
    return player_bio


