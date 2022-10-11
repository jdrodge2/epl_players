# Jacob Rodgers' English Premier League  (EPL) Data Analyst Project

## Project Breakdown
In this repo I have included 4 different directories. The `Web scraping and Cleaning` directory which includes 3 python scripts:
* `epl_players_scraper` :
  * In this script I used python libraries `Selenium`, `BeauftifulSoup`, `Pandas` and `re` to webscrape the EPL website. I had to use `Selenium` for this as it included many dynamically loading webpages.
     * Methods were written to webscrape individual player URLS for the last 4 completed premier league seasons
     * Each of these URLS were visited to obtain player biographical information and then manipulated to obtain player statistical information
* `clean_epl_players` :
   * In this script I used python libraries `Pandas` and `re` to clean the unoraganized data that I scraped with the previous script
      * Data was converted into two different dataframes. One for biographical and the other for statistical.
      * Each player was given an unique id so that the two tables could be joined together if needed
* `epl_players` : 
   * This script is the executable that I wrote which calls upon the two previous scripts and writes the data to 7 different CSV files.

All of the CSV files that I created for this project can be found in the `CSV Files` directory:
* All of the following files were created from the webscraper:
   * `raw_player_biographical` - uncleaned data from the scraper
   * `raw_player_stats` - uncleaned data from the scraper
   * `player_biographical` - cleaned data which reformats the birthday, removes measurements from numbers, and recasts value types
   * `attacker_stats` - cleaned statistical data separated out for Forwards
   * `defender_stats` - cleaned statistical data separated out for Defenders
   * `midfielder_stats` - cleaned statistical data separated out for Midfielders
   * `goalie_stats` - cleaned statistical data separated out for Goalies
 * The last two csv files were created using SQL queries
   * `player_misconduct` - stores information regarding the players age as well as the total amount of fouls, yellow & red cards players have recieved across all seasons captured
   * `player_season_avg_misconduct` - used the previous csv file to show the aveage amount of misconducts individual players recieve on a seasonly basis

Next there is the `MySQL` directory which includes:
* `Table Creation`
   * A SQL script that creates all of the tables needed and reads in the data collected within the original 5 cleaned CSV data files
* `player_misconduct` - The SQL queries I used to create the last 2 CSV files listed

NOTE: To complete this section of the project I used both `MySQL Workbench` and `MAMP` for the `MySQL Server`

Lastly there is the `Visualizations` directory which includes:
* `epl_visuals` 
   * A power Bi file that I created to capture 3 different visualizations
* `Visuals_screen_captures` - A brief powerpoint showing static versions of the visualizations created in the power Bi file.
   * The First slide shows a pie chart of how player nationalities in the EPL are broken down followed by a world map of where majority of players come from
   * The Second slide shows the Top attackers in the EPL based on the data collected for individual wins, goals, big chances created and assists
   * The Last slide shows the most aggressive indivuals based on the average amount of misconducts players face within a single season


## Conclusion

  This was my first time completing a data analyst project and I learned many things along the way. That being said, since this project was mostly Python heavy, I do intend to try and complete another project in the near future that spends more time polishing my SQL and BI/Tableau skills. Both the SQL and Power BI visualizations that I used for this project were more on the basic side of things. Regarding SQL, I would like to practice Views, Complex Joins, Common Table Expressions, Global temp tables, triggers, and indexing as I have not used many of these elements since I recently graduated in May. I am also interested in how I may be able to connect MySQL workbench directly to Power BI/Tableau for easy table and query access so that I may be able to create higher end visualizations. Finally, visualization is the place that I currently feel the weakest at. I know how to do a decent amount of visualizing with the `Matplotlib` and `Seaborn` python packages, but going forward I plan to practice Tableau/Power Bi through complex open source datasets That I will most likely download from Kaggle or Google BigQuery.
  
**Thanks for taking the time to read through all of this! If you have any suggestions on how I can make my code better/become a stronger data analyst please feel free to share you knowledge with me!**
