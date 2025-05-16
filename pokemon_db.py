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
    Extracts detailed Pokémon info from a BeautifulSoup page object.
    Updates pokedex_dict in place.
    """

    poke_name_from_link = poke_content.select('h1')[0].string
    pokedex_data = poke_content.select('table[class="vitals-table"]')

    pokedex_num = pokedex_data[0].select('td')[0].contents[0].string

    elem_type = list(pokedex_data[0].select('td')[1].children)
    elements = [x.string for x in elem_type if not str(x).isspace()]
    elem_1 = elements[0]
    elem_2 = elements[1] if len(elements) > 1 else None

    species = pokedex_data[0].select('td')[2].string

    height = pokedex_data[0].select('td')[3].string.replace(u'\xa0', '')
    height_meters = float(height.split('m')[0])

    weight = pokedex_data[0].select('td')[4].string.replace(u'\xa0', '')
    weight_kg = float(weight.split('kg')[0])

    gender = list(pokedex_data[2].select('td')[1].children)
    gender_stats = [x.string for x in gender if not str(x).isspace()]
    if "Genderless" in gender_stats:
        male = female = 0.0
    else:
        male = float(gender_stats[0].split('%')[0])
        female = float(gender_stats[2].split('%')[0])

    stats_table = pokedex_data[3].select('tr')
    hp = int(stats_table[0].select('td')[1].string)
    attack = int(stats_table[1].select('td')[1].string)
    defense = int(stats_table[2].select('td')[1].string)
    sp_atk = int(stats_table[3].select('td')[1].string)
    sp_def = int(stats_table[4].select('td')[1].string)
    speed = int(stats_table[5].select('td')[1].string)
    total = int(stats_table[6].select('td')[1].string)

    # Append all extracted values
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

print("\n=== FETCHING AND SAVING POKÉMON DATA... ===\n")

for count, poke_site in enumerate(link_frame['url'], start=1):
    page = get(poke_site)
    poke_content = BeautifulSoup(page.content, "html.parser")
    pokemon_scraper(poke_content, pokedex_dict)

    print(f"{count} of {len(link_frame['url'])} complete")
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

print(f"\n✅ Data saved successfully to '{file_name}'")

# --------------------------------------------
# STEP 7: OPTIONAL - READ CSV FOR VERIFICATION
# --------------------------------------------

pokemon_csv = pd.read_csv(file_name)
pokemon_csv.head()
