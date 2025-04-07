# Pokemon Database Scraper

Written by Lily Gates  
April 2025

## Description
Use BeautifulSoup to scrape Pokemon data and convert into Pandas DataFrame

## Required Dependencies
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from urllib.parse import urljoin
import time

## PURPOSE
The purpose of my code is to scrape from the website `https://pokemondb.net` and obtain all of the unique Pokemon and the respective data. The data is then converted into a pandas dataframe, which is finally exported as a .csv file.


## REFLECTION

### Future Improvements:
This project does not include duplicate Pokemon, such as Mega Venasaur. Although duplicate Pokemon are listed on the main webpage with the grid of Pokemon, (`https://pokemondb.net/pokedex/all`) they hyperlink to the same URL. When going to the directed URL, there are sometimes options for clickable tabs, such as the regular Venasaur or Mega Venasaur. However, the URL does not change. As such, I had exceptional challenges with trying to include my webscraping. As a result, I chose to only include the "base" Pokemon, rather than it's varients. This reduced the total Pokemon from 1125 to 1025. 

In addition to simplifying things, I chose to include what I felt were the most useful data about each Pokemon. For example, knowing the local pokedex indexes or the numerous descriptors of the Pokemon seemed superflous given that I included the National Pokedex Number (which is the most official and complete) as well as the "species." One data I inteded to include, but did not, was the "Attributes." The formatting was strange beccause it included ocassionally bulleted lists and different fonts for "hidden abilities." Given the time availible and the difficulty, I decided to abstain from including it.

### Demonstration on How Someone Might Use the Data
This Pokemon data can be used to improve game play, by potentially adjusting base-stats of existing Pokemon, as well as creating new pokemon that add to the diversity, complexity, and competitiveness of Pokemon. If certain Pokemon types are consistently stronger than others, it can lead to repetitive and predictive gameplay.

Potential Question:
A game designer might ask: “Are Fire-type Pokemon overpowered compared to other types?” To explore this, the designer could analyze the dataset by grouping Pokemon based on their primary and or secondary elemental type and comparing average base stats such as Attack, Defense, and Speed across each type. For example, by comparing the average Attack stat of Fire-type Pokemon to that of other types (like Water, Grass, or Psychic), the designer might discover that Fire-types have significantly higher offensive capabilities. If this advantage isn’t balanced by weaknesses in other areas (like Defense or Speed), it could point to a design imbalance.

How the Data Can Be Used to Answer:
The Pokemon dataset includes attributes such as, element type(s), fighting base stats (e.g., HP, Attack, Defense, Speed, etc.). By leveraging this information, the designer can identify trends and outliers. This insight allows the team to adjust base stats, move effectiveness, or game mechanics to ensure a more balanced and engaging experience for all players. In this way, the Pokemon dataset becomes a valuable tool not just for analysis, but for informed decision-making in the game design process—leading to better gameplay and a more competitive environment.

### Additional Steps to Make Data Useful for Analysis
However, in order for this idea of comparing Pokemon element types, we would also need to slightly improve the dataset. The original dataset does not include a special indicator for "Legendary" Pokemon, which are notoriously stronger than non-legendary Pokemon. By filtering for legendary Pokemon, it can potentially address skews to the data.



## EXPLAINING THE CODE (Summary)
**Summary: Web Scraping the Pokémon Database**

**1. Importing Libraries and Accessing the Main Page**

The script begins by importing essential libraries like BeautifulSoup, requests, pandas, urljoin, and time. It then fetches the main Pokémon database page (https://pokemondb.net/pokedex/all) and parses it using BeautifulSoup.

**2. Extracting and Cleaning Pokémon URLs**

Using select on anchor tags with the class ent-name, it extracts links and names for all Pokémon. To ensure no duplicates, the code creates filtered lists of unique Pokémon names and their corresponding full URLs (by joining with the base URL). These are stored in a DataFrame.

**3. Scraping Individual Pokémon Pages**

A function, pokemon_scraper(), is defined to extract detailed data from each individual Pokémon page, including:

* Name and Pokédex number
* Type(s) (with conditionals for dual types)
* Species, height, and weight (cleaned and converted to numeric)
* Gender ratio (with handling for genderless Pokémon)
* Base stats (HP, Attack, Defense, etc.)
    
These values are stored in a dictionary initialized before the function.

**4. Looping Through All Pokémon**

The script loops through all 1,025 unique Pokémon URLs. For each one, it fetches the page, parses it, and calls the scraper function to extract and store data. A counter tracks progress, and a 1-second delay is used between requests to avoid overwhelming the server.

**5. Creating the Final DataFrame**

After scraping, the dictionary is converted into a pandas DataFrame. The Pokédex number is explicitly kept as a string to preserve formatting (e.g., leading zeros). The final dataset can then be saved as a .csv file.