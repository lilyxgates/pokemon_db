# ============================================
# Pokémon Data Webscraper
# Author: Lily Gates
# Date: May 2025
# Description: Scrapes detailed Pokémon data from pokemondb.net
# ============================================

# --- IMPORTS AND SETUP ---
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

# --------------------------------------------
# STEP 1: FETCH MAIN POKÉMON LIST AND LINKS
# --------------------------------------------

# Define the main URL and base URL
url = 'https://pokemondb.net/pokedex/all'
base_url = 'https://pokemondb.net'

# Request and parse the main page
site = get(url)
content = BeautifulSoup(site.content, "html.parser")

# Extract anchor elements containing Pokémon names
anchor_elem = content.select('a[class="ent-name"]')

# Get names and full URLs
pokemon_names = [x.string for x in anchor_elem]
completed_links = [urljoin(base_url, i.get('href')) for i in anchor_elem]

# --------------------------------------------
# STEP 2: REMOVE DUPLICATES
# --------------------------------------------

# Get unique Pokémon names and links
unique_pokemon = []
unique_links = []

for name, link in zip(pokemon_names, completed_links):
    if name not in unique_pokemon:
        unique_pokemon.append(name)
        unique_links.append(link)

# Create a dataframe of names and links
link_frame = pd.DataFrame({
    'pokemon': unique_pokemon,
    'url': unique_links
})
# --------------------------------------------
# STEP 3: INITIALIZE DATA STRUCTURE
# --------------------------------------------

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

# --------------------------------------------
# STEP 4: DEFINE SCRAPER FUNCTION
# --------------------------------------------


def pokemon_scraper(poke_content, pokedex_dict):
    """
    Extract detailed Pokémon data from a BeautifulSoup-parsed page and 
    append the extracted information to the provided dictionary.

    Args:
        poke_content (bs4.BeautifulSoup): Parsed HTML content of a Pokémon's webpage.
        pokedex_dict (dict): Dictionary with lists that stores Pokémon data fields 
                             such as name, stats, types, and more.

    Returns:
        None: This function updates pokedex_dict in place by appending new data.

    The function extracts the following data fields for each Pokémon:
        - poke_name_from_link: Pokémon name as shown in the page's <h1> header.
        - pokedex_num: National Pokédex number (string).
        - elem_1: Primary elemental type (string).
        - elem_2: Secondary elemental type or None if absent.
        - species: Species category (string).
        - height_meters: Height in meters (float).
        - weight_kg: Weight in kilograms (float).
        - male: Percentage male (float), 0 if genderless.
        - female: Percentage female (float), 0 if genderless.
        - hp: Hit Points stat (int).
        - attack: Attack stat (int).
        - defense: Defense stat (int).
        - sp_atk: Special Attack stat (int).
        - sp_def: Special Defense stat (int).
        - speed: Speed stat (int).
        - total: Total base stats (int).

    Notes:
        - The function assumes the webpage structure is consistent with the 
          'vitals-table' CSS class used in the official Pokémon wiki or similar.
        - It handles genderless Pokémon by setting male and female percentages to zero.
        - Pokedex description entries are extracted but not appended to the dictionary 
          in this version (can be added if needed).
    """
    
    # Pokemon name
    poke_name_from_link = poke_content.select('h1')[0].string
    
    # Locate the table that contains the data
    pokedex_data = poke_content.select('table[class="vitals-table"]')
    
    # National Pokedex Number
    pokedex_num = pokedex_data[0].select('td')[0].contents[0].string
    
    # Element type(s)
    elem_type = list(pokedex_data[0].select('td')[1].children)
    elements = []
    for x in elem_type:
        if not str(x).isspace():
            elements.append(x.string)
    elem_1 = elements[0]
    elem_2 = None
    if len(elements) > 1:  # Sometimes there is more than one type
        elem_2 = elements[1]
    
    # Species
    species = pokedex_data[0].select('td')[2].string
    
    # Height
    height = pokedex_data[0].select('td')[3].string.replace(u'\xa0','')
    height_meters = float(height.split('m')[0])

    # Weight
    weight = pokedex_data[0].select('td')[4].string.replace(u'\xa0','')
    weight_kg = float(weight.split('kg')[0])

    # Gender
    gender = list(pokedex_data[2].select('td')[1].children)
    gender_stats = []
    for x in gender:
        if not str(x).isspace():
            gender_stats.append(x.string)

    if "Genderless" in gender_stats:
        male = float(0)
        female = float(0)
    else:
        male = float(gender_stats[0].split('%')[0])  # Extracts only the percent digits
        female = float(gender_stats[2].split('%')[0])  # Extracts only the percent digits

    # Fighting Stats
    hp = int(list(pokedex_data[3].select('tr')[0])[3].string)
    attack = int(list(pokedex_data[3].select('tr')[1])[3].string)
    defense = int(list(pokedex_data[3].select('tr')[2])[3].string)
    sp_atk = int(list(pokedex_data[3].select('tr')[3])[3].string)
    sp_def = int(list(pokedex_data[3].select('tr')[4])[3].string)
    speed = int(list(pokedex_data[3].select('tr')[5])[3].string)
    total = int(list(pokedex_data[3].select('tr')[6])[3].string)
    
    # Append elements in the list for each key
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

# --------------------------------------------
# STEP 5: LOOP THROUGH URLS AND SCRAPE DATA
# --------------------------------------------

# --------------------------------------------
# STEP 5: LOOP THROUGH URLS AND SCRAPE DATA
# --------------------------------------------

print("\n=== FETCHING AND SAVING POKÉMON DATA... ===\n")

# Iterate over each Pokémon URL in the link_frame DataFrame
# 'enumerate' is used to keep track of progress (count) starting from 1
for count, poke_site in enumerate(link_frame['url'], start=1):
    # Send an HTTP GET request to the Pokémon’s individual page
    page = get(poke_site)
    
    # Parse the HTML content of the page using BeautifulSoup
    poke_content = BeautifulSoup(page.content, "html.parser")
    
    # Extract relevant Pokémon data from the page and append it to the pokedex_dict
    pokemon_scraper(poke_content, pokedex_dict)
    
    # Print progress update showing how many Pokémon have been processed out of total
    print(f"{count} of {len(link_frame['url'])} complete")
    
    # Pause for 1 second between requests to avoid overloading the server (politeness)
    time.sleep(1)

# --------------------------------------------
# STEP 6: SAVE FINAL DATAFRAME TO CSV
# --------------------------------------------

pokedex_df = pd.DataFrame(pokedex_dict)
pokedex_df['pokedex_num'] = pokedex_df['pokedex_num'].astype(str)

merged_df = pd.merge(link_frame, pokedex_df, left_on="pokemon", right_on="poke_name_from_link")
final_df = merged_df.drop(columns=["poke_name_from_link"])

file_name = "pokemon_db.csv"
final_df.to_csv(file_name, index=False)

print(f"\nData saved successfully as '{file_name}'")

# --------------------------------------------
# STEP 7: READ CSV FOR VERIFICATION
# --------------------------------------------

pokemon_csv = pd.read_csv(file_name)
pokemon_csv.head()
