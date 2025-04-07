# Lily Gates
# April 2025
# Pokemon Database Web Scraper

from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from urllib.parse import urljoin
import time

######################
# SCRAPE THE MAIN PAGE
######################
url = 'https://pokemondb.net/pokedex/all'  # Specific link to the database
base_url = 'https://pokemondb.net'  # Base URL for subsequent Pokemon links
# Get site
site = get(url)

# Parse the content, return raw HTML content
content = BeautifulSoup(site.content, "html.parser")

# Return the Response Code (200 = it is working)
#site.status_code
#print(site)  

# Prints the HTML parsed
#print(content)  
#len(content)

###############################
# SELECT SPECIFIC POKEMON PAGES
###############################

# Selecting the links to specific Pokemon pages
anchor_elem = content.select('a[class="ent-name"]')                
print(f"Total number of ALL Pokemon in database: {len(anchor_elem)}")  # Total number of Pokemon: 1215

# LINKS
# Link to the first Pokemon
anchor_elem[0].get('href')

# Generator expression to create list of all href
list_of_links = [i.get('href') for i in anchor_elem]
list_of_links[:10]  # Show partial links to the first 10 Pokemon

# Combine base_url with specific href for first Pokemon
full_url = urljoin(base_url, anchor_elem[0].get('href'))
#print(full_url)

completed_links = [urljoin(base_url, i.get('href')) for i in content.select('a[class="ent-name"]')]
completed_links[:10]  # Show full links to the first 10 Pokemon

# POKEMON NAMES
# Get names of Pokemon
# Generator expression, for each anchor element, retrieve string (name of Pokemon)
pokemon_names = [x.string for x in content.select('a[class="ent-name"]')]              
pokemon_names[:10]  # Show names of the first 10 TOTAL Pokemon (including potential duplicates)

###########################
# REMOVING DUPLICATE VALUES
###########################

# Create a unique list of only unique Pokemon names
# Note: Some Pokemon share the same URL, but different names based on unique version (e.g., Venusaur vs. Mega Venusaur)

unique_pokemon = []

for i in pokemon_names:
    if i not in unique_pokemon:
        unique_pokemon.append(i)
        
print(f"Total number of UNIQUE Pokemon in database: {len(unique_pokemon)}")  # # Number of unique Pokemon: 1025

#print(unique_pokemon[:10])  # Show names of the first 10 UNIQUE Pokemon

# Create a list of only unique complete URLs
# Note: Some Pokemon share the same URL, but different names based on unique version (e.g., Venusaur vs. Mega Venusaur)

unique_links = []

for i in completed_links:
    if i not in unique_links:
        unique_links.append(i)
        
#print(unique_links[:10])  # Show full links to the first 10 Pokemon

##############################################
# DATAFRAME OF UNIQUE POKEMON AND UNIQUE LINKS
##############################################

# Dataframe of unique_pokemon and unique_links
link_frame = pd.DataFrame({'pokemon': unique_pokemon, 'url': unique_links})
link_frame.head()

#####################################################
# MAIN FUNCTION FOR SCRAPING AND STORING IN DICTIONARY
#####################################################


pokedex_dict = {'poke_name_from_link': [],
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

def pokemon_scraper(poke_content, pokedex_dict):
    """
    Args
        poke_content: bs4 content after parsing each page
        pokedex_dict: output with specific stats for each pokemon
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


########################################################
# LOOPING THROUGH ALL URLS AND SCRAPING CONTENT FOR EACH
########################################################
# Note: Will take about 17 minutes to scrape and save data for 1000+ Pokemon

count = 0

# Iterate thru the URL column in link_frame and scrape content

for poke_site in link_frame['url']:

    # Send a get() request to specific Pokemon link
    page = get(poke_site)

    # Parse the content using BeautifulSoup and call the result content
    poke_content = BeautifulSoup(page.content, "html.parser")
    
    # Call function
    pokemon_scraper(poke_content, pokedex_dict)
    
    # Counter
    count += 1
    print(f"{count} of {len(link_frame['url'])}")
    
    # Print Dictionary -- Only run to test
    #print(pokedex_dict)
    
    # Add sleeper timer for 1 seconds
    time.sleep(1)
    
####################################################
# CREATING AND MERGING DATAFRAME OF LINKS AND STATS
####################################################

# Pokedex DataFrame
pokedex_df = pd.DataFrame(pokedex_dict)

# Ensuring `pokedex_df['pokedex_num']` stays as a str datatype
pokedex_df['pokedex_num'] = pokedex_df['pokedex_num'].astype(str)

pokedex_df

# Merge `link_frame` (df with pokemon name and URL) with `pokedex_df` (df with pokemon name and stats)

merged_df = pd.merge(link_frame, pokedex_df, left_on = "pokemon", right_on = "poke_name_from_link")
final_df = merged_df.drop(columns=["poke_name_from_link"])

final_df

####################################################
# CONVERT TO .CSV FILE AND THEN READ .CSV BACK IN
####################################################

# CONVERT TO .CSV
# Save and Export `final_df` as .csv
file_name = "pokemon_db.csv"
final_df.to_csv(file_name, index=False)

# READ .CSV BACK IN
pokemon_csv = pd.read_csv(file_name)
pokemon_csv

####################################################
# CHECKING DATA TYPES FOR DATAFRAME AND .CSV FILE
####################################################

# Checking Data Types -- For `final_df`
print("---------Data Types for `final_df` Dataframe--------")
print(f"The 'pokemon' column contains type {type(final_df['pokemon'][0])}")
print(f"The 'url' column contains type {type(final_df['url'][0])}")
print(f"The 'pokedex_num' column contains type {type(final_df['pokedex_num'][0])}")
print(f"The 'elem_1' column contains type {type(final_df['elem_1'][0])}")
print(f"The 'elem_2' column contains type {type(final_df['elem_2'][0])}")
print(f"The 'species' column contains type {type(final_df['species'][0])}")
print(f"The 'height_meters' column contains type {type(final_df['height_meters'][0])}")
print(f"The 'weight_kg' column contains type {type(final_df['weight_kg'][0])}")
print(f"The 'male' column contains type {type(final_df['male'][0])}")
print(f"The 'female' column contains type {type(final_df['female'][0])}")
print(f"The 'hp' column contains type {type(final_df['hp'][0])}")
print(f"The 'attack' column contains type {type(final_df['attack'][0])}")
print(f"The 'defense' column contains type {type(final_df['defense'][0])}")
print(f"The 'sp_atk' column contains type {type(final_df['sp_atk'][0])}")
print(f"The 'sp_def' column contains type {type(final_df['sp_def'][0])}")
print(f"The 'speed' column contains type {type(final_df['speed'][0])}")
print(f"The 'total' column contains type {type(final_df['total'][0])}")

print("\n")

# Checking Data Types -- For `pokemon_csv`
print("---------Data Types for `pokemon_csv` Dataframe--------")
print(f"The 'pokemon' column contains type {type(pokemon_csv['pokemon'][0])}")
print(f"The 'url' column contains type {type(pokemon_csv['url'][0])}")
print(f"The 'pokedex_num' column contains type {type(pokemon_csv['pokedex_num'][0])}")
print(f"The 'elem_1' column contains type {type(pokemon_csv['elem_1'][0])}")
print(f"The 'elem_2' column contains type {type(pokemon_csv['elem_2'][0])}")
print(f"The 'species' column contains type {type(pokemon_csv['species'][0])}")
print(f"The 'height_meters' column contains type {type(pokemon_csv['height_meters'][0])}")
print(f"The 'weight_kg' column contains type {type(pokemon_csv['weight_kg'][0])}")
print(f"The 'male' column contains type {type(pokemon_csv['male'][0])}")
print(f"The 'female' column contains type {type(pokemon_csv['female'][0])}")
print(f"The 'hp' column contains type {type(pokemon_csv['hp'][0])}")
print(f"The 'attack' column contains type {type(pokemon_csv['attack'][0])}")
print(f"The 'defense' column contains type {type(pokemon_csv['defense'][0])}")
print(f"The 'sp_atk' column contains type {type(pokemon_csv['sp_atk'][0])}")
print(f"The 'sp_def' column contains type {type(pokemon_csv['sp_def'][0])}")
print(f"The 'speed' column contains type {type(pokemon_csv['speed'][0])}")
print(f"The 'total' column contains type {type(pokemon_csv['total'][0])}")

# Note: The values in 'pokedex_num' could be considered a str (because it has leading zeros)
# When the 'final_df' is converted into .csv, it retains the leading zeros
# However, when it is read back in using `pd.read_csv`, the 'pokedex_num' column is converted into numpy.inst64