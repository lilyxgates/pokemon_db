# Pokémon Database Scraper
*Written by Lily Gates* 
*April 2025*

## Description
This script uses BeautifulSoup to scrape Pokémon data from the Pokémon Database and convert it into a Pandas DataFrame.

## Required Dependencies
- `beautifulsoup4`
- `requests`
- `pandas`
- `urllib.parse`
- `time`

## Purpose
The purpose of this code is to scrape data from `https://pokemondb.net` and gather information on all unique Pokémon, which is then converted into a Pandas DataFrame and saved as a `.csv` file.

## Reflection

### Future Improvements
This project does not include duplicate Pokémon, such as Mega Venusaur. Although duplicates are listed on the main webpage (`https://pokemondb.net/pokedex/all`), they hyperlink to the same URL. When visiting these pages, there are clickable tabs, such as "regular Venusaur" and "Mega Venusaur," but the URL does not change. This caused challenges in the scraping process, so I decided to focus only on the "base" Pokémon, reducing the total from 1,125 to 1,025 Pokémon.

In addition, I prioritized including the most useful data about each Pokémon. For instance, while local Pokédex indexes and numerous descriptors were available, I chose to only include the National Pokédex number (which is more official) and the Pokémon species. One data point I intended to include but did not was "Attributes." The formatting of this data was inconsistent, with bulleted lists and different fonts for "hidden abilities," making it difficult to scrape. Given time constraints, I decided not to include it.

### Demonstration of How Someone Might Use the Data
This Pokémon data can be useful for improving gameplay, such as adjusting the base stats of existing Pokémon or creating new Pokémon to add variety, complexity, and competitiveness to the game. If certain Pokémon types are consistently stronger than others, it can lead to repetitive and predictable gameplay.

**Potential Question:**  
A game designer might ask: "Are Fire-type Pokémon overpowered compared to other types?" To explore this, the designer could analyze the dataset by grouping Pokémon based on their primary and/or secondary elemental types and comparing the average base stats (e.g., Attack, Defense, Speed) for each type. For example, comparing the average Attack stat of Fire-type Pokémon to that of other types (like Water, Grass, or Psychic) might reveal that Fire-types have higher offensive capabilities. If this advantage is not balanced by weaknesses in other areas (e.g., Defense or Speed), it could indicate a design imbalance.

**How the Data Can Be Used to Answer the Question:**  
The dataset includes attributes like element type(s), and base stats (HP, Attack, Defense, Speed, etc.). By analyzing these, the designer can identify trends and outliers, allowing them to adjust base stats, move effectiveness, or game mechanics to ensure a more balanced and engaging experience for all players.

### Additional Steps to Make Data More Useful for Analysis
To better compare Pokémon element types, the dataset could be improved by including an indicator for "Legendary" Pokémon, which are typically stronger than non-legendary Pokémon. Filtering out Legendary Pokémon could help address potential data skew and make for a more balanced analysis.

## Code Explanation (Summary)

### 1. Importing Libraries and Accessing the Main Page
The script imports essential libraries: BeautifulSoup, requests, pandas, urljoin, and time. It fetches and parses the main Pokémon database page (`https://pokemondb.net/pokedex/all`) using BeautifulSoup.

### 2. Extracting and Cleaning Pokémon URLs
The script uses the `select` method on anchor tags with the `ent-name` class to extract links and names for all Pokémon. To avoid duplicates, it creates filtered lists of unique Pokémon names and their corresponding full URLs (via `urljoin`). These URLs are stored in a DataFrame.

### 3. Scraping Individual Pokémon Pages
A function, `pokemon_scraper()`, is defined to scrape detailed data from each Pokémon’s individual page, such as:
- Name and Pokédex number
- Type(s), handling dual types
- Species, height, and weight (with numeric conversion)
- Gender ratio (handling genderless Pokémon)
- Base stats (HP, Attack, Defense, etc.)

This data is stored in a dictionary initialized before the function is called.

### 4. Looping Through All Pokémon
The script loops through all 1,025 unique Pokémon URLs. For each URL, it fetches the page, parses it, and uses `pokemon_scraper()` to collect data. A progress counter is included, with a 1-second delay between requests to avoid overwhelming the server.

### 5. Creating the Final DataFrame
After scraping, the data is converted into a Pandas DataFrame. The Pokédex number is preserved as a string to maintain formatting (e.g., leading zeros). Finally, the dataset is saved as a `.csv` file.
