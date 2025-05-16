# Lily Gates
# May 2025

# --- IMPORTS AND SETUP ---
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

# -------------------------
# SCRAPE DATA USING BEAUTIFUL SOUP
# -------------------------

# Define the main URL for scraping all Pokemon data
url = 'https://pokemondb.net/pokedex/all'  # Full Pokemon database page
base_url = 'https://pokemondb.net'          # Base URL to join with relative links

# Request the page content
site = get(url)

# Parse the raw HTML content using BeautifulSoup
content = BeautifulSoup(site.content, "html.parser")

# Select all anchor tags containing Pokemon names (class="ent-name")
anchor_elem = content.select('a[class="ent-name"]')                

# Extract all href links for each Pokemon using a list comprehension
list_of_links = [i.get('href') for i in anchor_elem]

# Generate full URLs for each Pokemon by joining base URL with relative hrefs
completed_links = [urljoin(base_url, i.get('href')) for i in anchor_elem]

# Extract all Pokemon names (text inside anchor elements)
pokemon_names = [x.string for x in anchor_elem]

# -------------------------
# REMOVE DUPLICATE POKEMON NAMES AND LINKS
# -------------------------

# Initialize empty lists to store unique Pokemon names and links
unique_pokemon = []
for i in pokemon_names:
    if i not in unique_pokemon:
        unique_pokemon.append(i)

#print(f"Total number of UNIQUE Pokemon in database: {len(unique_pokemon)}")
#print(unique_pokemon[:10])  # Display first 10 unique Pokemon names

# Similarly, create a unique list of full URLs to avoid duplicates
unique_links = []
for i in completed_links:
    if i not in unique_links:
        unique_links.append(i)

# -------------------------
# CREATE DATAFRAME WITH UNIQUE POKEMON NAMES AND LINKS
# -------------------------

link_frame = pd.DataFrame({
    'pokemon': unique_pokemon,
    'url': unique_links
})

# -------------------------
# DEFINE FUNCTION TO SCRAPE DETAILED DATA FOR EACH POKEMON
# -------------------------

pokedex_dict = {
    'poke_name_from_link': [],
    'pokedex_num': [],
    'elem_1': [],
    'elem_2': [],
    'species': [],
    'height_meters': [],
    'weight_kg': [],
    'male': [],
    'female': [],
    'hp': [],
    'attack': [],
    'defense': [],
    'sp_atk': [],
    'sp_def': [],
    'speed': [],
    'total': []
}

# SCRAPER FUNCTION TO EXTRACT DETAILED POKEMON DATA FROM EACH PAGE

def pokemon_scraper(poke_content, pokedex_dict):
    """
    Parses the HTML content of a Pokemon's page and extracts key information 
    about the Pokemon such as stats, type, species, gender ratio, and physical attributes.
    
    Args:
        poke_content (BeautifulSoup object): Parsed HTML content of the Pokemon page.
        pokedex_dict (dict): Dictionary to append the extracted data into.
        
    Updates pokedex_dict in place by appending the following keys:
        - poke_name_from_link: Pokemon's name from the page header
        - pokedex_num: National Pokedex number
        - elem_1, elem_2: Primary and secondary element types
        - species: Pokemon species description
        - height_meters: Height in meters (float)
        - weight_kg: Weight in kilograms (float)
        - male: Percentage male gender (float, or 0 if genderless)
        - female: Percentage female gender (float, or 0 if genderless)
        - hp, attack, defense, sp_atk, sp_def, speed, total: Base stats as integers
    """

    # Extract Pokemon name from the page header
    poke_name_from_link = poke_content.select('h1')[0].string

    # Locate the table with Pokemon vitals and stats
    pokedex_data = poke_content.select('table[class="vitals-table"]')

    # National Pokedex number
    pokedex_num = pokedex_data[0].select('td')[0].contents[0].string

    # Element types (1 or 2 types)
    elem_type = list(pokedex_data[0].select('td')[1].children)
    elements = [x.string for x in elem_type if not str(x).isspace()]
    elem_1 = elements[0]
    elem_2 = elements[1] if len(elements) > 1 else None

    # Species
    species = pokedex_data[0].select('td')[2].string

    # Height in meters (strip special characters and convert to float)
    height = pokedex_data[0].select('td')[3].string.replace(u'\xa0','')
    height_meters = float(height.split('m')[0])

    # Weight in kg (strip special characters and convert to float)
    weight = pokedex_data[0].select('td')[4].string.replace(u'\xa0','')
    weight_kg = float(weight.split('kg')[0])

    # Gender distribution percentages or genderless
    gender = list(pokedex_data[2].select('td')[1].children)
    gender_stats = [x.string for x in gender if not str(x).isspace()]

    if "Genderless" in gender_stats:
        male = 0.0
        female = 0.0
    else:
        male = float(gender_stats[0].split('%')[0])
        female = float(gender_stats[2].split('%')[0])

    # Fighting stats (HP, Attack, Defense, etc.)
    hp = int(list(pokedex_data[3].select('tr')[0])[3].string)
    attack = int(list(pokedex_data[3].select('tr')[1])[3].string)
    defense = int(list(pokedex_data[3].select('tr')[2])[3].string)
    sp_atk = int(list(pokedex_data[3].select('tr')[3])[3].string)
    sp_def = int(list(pokedex_data[3].select('tr')[4])[3].string)
    speed = int(list(pokedex_data[3].select('tr')[5])[3].string)
    total = int(list(pokedex_data[3].select('tr')[6])[3].string)

    # Append all extracted values to the respective lists in the dictionary
    pokedex_dict['poke_name_from_link'].append(poke_name_from_link)
    pokedex_dict['pokedex_num'].append(pokedex_num)
    pokedex_dict['elem_1'].append(elem_1)
    pokedex_dict['elem_2'].append(elem_2)
    pokedex_dict['species'].append(species)
    pokedex_dict['height_meters'].append(height_meters)
    pokedex_dict['weight_kg'].append(weight_kg)
    pokedex_dict['male'].append(male)
    pokedex_dict['female'].append(female)
    pokedex_dict['hp'].append(hp)
    pokedex_dict['attack'].append(attack)
    pokedex_dict['defense'].append(defense)
    pokedex_dict['sp_atk'].append(sp_atk)
    pokedex_dict['sp_def'].append(sp_def)
    pokedex_dict['speed'].append(speed)
    pokedex_dict['total'].append(total)

# -------------------------
# LOOP THROUGH EACH UNIQUE POKEMON URL AND SCRAPE DATA
# -------------------------

print("\Fetching and Saving Pokémon Data...\n")

count = 0

for poke_site in link_frame['url']:
    """
    Loop through all Pokemon URLs, scrape each Pokemon page, and extract relevant data.
    """
    # Request the page content for this Pokemon
    page = get(poke_site)

    # Parse the HTML content
    poke_content = BeautifulSoup(page.content, "html.parser")

    # Extract and store Pokemon data by calling the scraper function
    pokemon_scraper(poke_content, pokedex_dict)

    # Increment counter and print progress
    count += 1
    print(f"{count} of {len(link_frame['url'])}")

    # Sleep for 1 second between requests to be polite to the server
    time.sleep(1)

# -------------------------
# CONVERT DICTIONARY TO DATAFRAME AND SAVE AS CSV
# -------------------------

# Create a DataFrame from the scraped Pokemon data dictionary
pokedex_df = pd.DataFrame(pokedex_dict)

# Ensure pokedex_num is a string (not integer)
pokedex_df['pokedex_num'] = pokedex_df['pokedex_num'].astype(str)

# Merge the basic Pokemon info with detailed stats on 'pokemon' name
merged_df = pd.merge(link_frame, pokedex_df, left_on="pokemon", right_on="poke_name_from_link")

# Drop duplicate 'poke_name_from_link' column after merge
final_df = merged_df.drop(columns=["poke_name_from_link"])

# Save the final DataFrame to a CSV file
file_name = "pokemon_db.csv"
final_df.to_csv(file_name, index=False)
print(f"A .CSV file '{file_name}' has been saved to the current working directory.")

# -------------------------
# READ CSV BACK INTO PANDAS (to verify or further process)
# -------------------------

pokemon_csv = pd.read_csv(file_name)
pokemon_csv
