from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
import re

""" The purpose of this script is to define method calls that will be used for different webscraping needs."""


def get_soup(url, use_selenium = False):
    """Loads website into Beautiful soup using lxml format and returns the Soup. Processes
    direct hyperlinks and selenium page source html code depending on the inputs given"""

    if use_selenium == False:
        website = requests.get(url)
        soup = BeautifulSoup(website.content, "lxml")

    else:
        soup = BeautifulSoup(load_webpage(url).page_source, "lxml")

    return soup


def load_webpage(url):
    """Loads different Premier League webpage links into the driver, accepts cookies when necessary and returns the driver"""

    options = webdriver.ChromeOptions()
    options.add_argument('headless') #specifies to run selenium without opening the Google Chrome GUI
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # add options=options when headless
    driver.get(url)
    time.sleep(1) #Makes sure that the webpage is fully loaded before proceeding

    try: #attempts to accept cookies if popup appears
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[5]/button[1]").click()
        time.sleep(1) #Makes sure that the webpage is fully loaded before proceeding

    except: #bypasses Unable to find element error when cookies popup does not appear
        pass

    """Uncomment the Code below when not running headless.
    Code is needed to close fifa23 pop-up ad."""
    # driver.find_element(By.XPATH, "/html/body/main/div[1]/nav/a[2]").click()

    return driver


def scroll_webpage(driver):
    """Scrolls the full length of a webpage to make sure that all html data is loaded
    before any scraping is performed. Returns the driver. Similar code found here (10/2/2022):
    https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage"""

    screen_height = driver.execute_script("return window.screen.height;")
    count = 1 #Counts the number of times that the page has scrolled to the bottom

    while True:
        driver.execute_script(f"window.scrollTo(0, {screen_height}*{count});") #scrolls exactly one screen height
        count += 1
        time.sleep(1) #Makes sure that the webpage is fully loaded before proceeding
        scroll_height = driver.execute_script("return document.body.scrollHeight;") #Stores how far has been scrolled

        if screen_height * count > scroll_height: #Once the page cannot scroll any farther, the while loop completes
            return driver
            break


def scrape_seasons_index(driver, num_seasons = 4): #Collects the last 4 full seasons... code will need to be updated if
                                                    # ran between end of most recent season and next season
    """Returns a dictionary with the season years as the key, and the index's needed to manipulate URLs as the value"""

    dropdown_list = driver.find_element(By.XPATH, r"/html/body/main/div[2]/div/div/section/div[1]/ul")
    li = dropdown_list.find_elements(By.TAG_NAME, "li")
    seasons = [[item.get_attribute("data-option-name"), item.get_attribute("data-option-id")] for item in li]
    seasons = seasons[1:num_seasons+1]
    seasons = {item[0]:item[1] for item in seasons}

    return seasons


def scrape_player_urls_and_club_names(seasons):
    """Collects the homepage URLs for individual players who participated in a particular season. Collects all of the clubs
    that participated in a particular season. Drops duplicate clubs and urls that exist across multiple seasons. Returns a lists
    for both player urls and club names"""

    club_names = pd.DataFrame()
    player_urls = pd.DataFrame()

    for value in seasons.values():
        website = f'https://www.premierleague.com/players?se={value}&cl=-1'
        driver = scroll_webpage(load_webpage(website)) #initializes the driver

        #Finds club names and adds them to the dataframe
        dropdown_list = driver.find_element(By.XPATH, r"/html/body/main/div[2]/div/div/section/div[2]/ul")
        li = dropdown_list.find_elements(By.TAG_NAME, "li")
        clubs = pd.DataFrame([item.get_attribute("data-option-name") for item in li], columns=["Club Name"])
        club_names = pd.concat([club_names, clubs])

        #Finds player urls and adds them to the the dataframe
        player_names = driver.find_elements(By.CLASS_NAME, 'playerName')
        link_to_player = pd.DataFrame([player.get_attribute("href") for player in player_names], columns=["Player URL"])
        player_urls = pd.concat([player_urls, link_to_player])

    club_names.drop_duplicates(inplace=True)
    club_names = club_names.values.tolist()
    club_names = [club for list_obj in club_names for club in list_obj][1:] #reduces the 2d list to a 1d list

    player_urls.drop_duplicates(inplace=True)
    player_urls = player_urls.values.tolist()
    player_urls = [link for list_obj in player_urls for link in list_obj] #reduces the 2d list to a 1d list

    return player_urls, club_names


def scrape_player_overview(url):
    """Scrapes an individual player's overview page. Returns a dictionary with general biographical information.
    Returns a list containing only the player's full name. Returns a list containing what clubs an individual played for
    within a particular season"""

    soup = get_soup(url)

    player_information = [item.get_text().strip(" \n ") for item in soup.findAll('div', attrs={"class": "info"})]
    player_info_label =[item.get_text().strip(" \n ") for item in soup.findAll('div', attrs={"class": "label"})]
    player_information = {player_info_label[i]:player_information[i] for i in range(len(player_information))}

    player_full_name = [item.get_text().strip(" \n ") for item in soup.findAll('div', attrs={"class": "name t-colour"})][0]
    player_club_by_season = pd.concat(pd.read_html(url))[["Season  Season", "Club"]].dropna().values.tolist()

    return player_full_name, player_information, player_club_by_season


def scrape_player_stats(url):
    """Scrapes an individuals statistics page for a particular season. Returns 2 dictionaries both containing statistical
    information"""

    soup = get_soup(url, use_selenium=True)

    top_stat = [item.get_text().strip(" \n ").split("\n") for item in soup.findAll('div', attrs={"class": "topStat"})]
    top_stat = [re.split(r"\s{2,}", item[0]) for item in top_stat]
    top_stat = {item[0]:item[1] for item in top_stat}

    normal_stat = [item.get_text().strip(" \n ").split("\n") for item in soup.findAll('div', attrs={"class": "normalStat"})]
    normal_stat = [re.split(r"\s{2,}", item[0]) for item in normal_stat]
    normal_stat = {item[0]:item[1] for item in normal_stat}

    return top_stat, normal_stat

