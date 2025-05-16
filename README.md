# Pokémon Database Scraper  
*Written by Lily Gates*  
*May 2025*


## Description  
This Python script scrapes Pokémon data from the Pokémon Database website (`https://pokemondb.net`) using BeautifulSoup and converts the data into a Pandas DataFrame. The resulting dataset includes key Pokémon attributes such as base stats, types, species, height, weight, and gender ratios, and is saved as a `.csv` file for further analysis.


## Required Dependencies  
- `beautifulsoup4`  
- `requests`  
- `pandas`  
- `urllib.parse`  
- `time`  


## Purpose  
The goal of this project is to collect comprehensive data on all **unique** Pokémon from the database, enabling data analysis and exploration of Pokémon characteristics. The scraped data can be useful for game design insights, balancing, or academic study.


## Usage  
Run the Python script to scrape the data and automatically save it to `pokemon_db.csv`. You can then load this CSV in any data analysis environment, such as Jupyter notebooks or Excel, to explore Pokémon traits and stats.


## Reflection

### Future Improvements  
- **Handling Duplicates:** The script currently excludes duplicate forms like Mega Evolutions because although duplicates appear on the main page, they link to the same URL with tabbed content. Scraping these tabs would require more complex navigation and parsing. Focusing on base forms reduced the total Pokémon scraped from 1,125 to 1,025.  
- **Additional Attributes:** Some data points, such as Pokémon "Attributes" (including hidden abilities), were not included due to inconsistent formatting that made automated scraping difficult. These could be added in future iterations with more advanced parsing or manual curation.

### Demonstration: How This Data Can Be Used  
Game designers or researchers can use this dataset to analyze the balance of Pokémon types and stats. For example:

- **Question:** Are Fire-type Pokémon overpowered compared to other types?  
- **Approach:** Group Pokémon by their primary and secondary element types, calculate average base stats like Attack and Defense, and compare these averages across types.  
- **Insight:** If Fire-types consistently have higher Attack without balancing weaknesses, it might indicate a need for gameplay adjustments.

The dataset provides all necessary variables (types, base stats, species) to conduct such analysis and inform game balancing decisions.

### Additional Steps to Improve Dataset Usability  
- Add a "Legendary" flag to identify and potentially exclude Legendary Pokémon from analyses, since their elevated stats can skew averages.  
- Include tabbed form data (Mega Evolutions, regional forms) to offer a fuller dataset for deeper insights.
- Add evolution chains and the stage for the evolution a Pokémon (if applicable)

## Code Explanation (Summary)

### 1. Importing Libraries and Accessing the Main Page  
Essential libraries are imported. The script fetches the main Pokémon list page and parses the HTML to identify links to individual Pokémon pages.

### 2. Extracting and Cleaning Pokémon URLs  
Using CSS selectors, the script extracts Pokémon names and URLs, removes duplicates, and constructs full URLs with `urljoin`. The cleaned lists are stored in a DataFrame.

### 3. Scraping Individual Pokémon Pages  
The `pokemon_scraper()` function extracts detailed info from each Pokémon page, including:
- Name and National Pokédex number  
- One or two element types  
- Species description  
- Height and weight (converted to floats)  
- Gender ratios (including genderless handling)  
- Base stats: HP, Attack, Defense, Special Attack, Special Defense, Speed, and total  

The data is appended to a dictionary that collects results for all Pokémon.

### 4. Looping Through All Pokémon  
The script iterates over all unique Pokémon URLs, scraping each page and extracting data with a 1-second delay between requests to respect server load. A progress counter tracks completion.

### 5. Creating the Final DataFrame  
The collected data dictionary is converted into a Pandas DataFrame. The National Pokédex number is maintained as a string for proper formatting. This detailed DataFrame is merged with the initial name-URL DataFrame and saved as a CSV file for analysis.