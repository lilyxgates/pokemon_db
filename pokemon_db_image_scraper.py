# ============================================
# Pokémon Image Scraper
# Author: Lily Gates
# Date: May 2025
# Description:
# Scrapes Pokémon names and image links from pokemondb.net,
# downloads each Pokémon's image, and saves it locally.
# Features:
# - Avoids duplicate downloads (tracked via text file)
# - Retries failed downloads
# - Adds delays to avoid overwhelming the server
# ============================================

# Import required packages
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import urljoin

# --------------------------------------------
# STEP 1: SCRAPE DATA
# --------------------------------------------
# URLs for scraping
url = 'https://pokemondb.net/pokedex/all'  # Page with all Pokémon
base_url = 'https://pokemondb.net'         # Base URL for joining with relative paths

# Retrieve and parse the site content
site = get(url)
content = BeautifulSoup(site.content, "html.parser")

# Extract anchor tags containing Pokémon names and links
anchor_elem = content.select('a[class="ent-name"]')

# Get list of Pokémon names
pokemon_names = [x.string for x in anchor_elem]

# Create list of full URLs to individual Pokémon pages
completed_links = [urljoin(base_url, a.get('href')) for a in anchor_elem]

# --------------------------------------------
# STEP 2: REMOVE DUPLICATES
# --------------------------------------------
# Create unique list of Pokémon names
unique_pokemon = []
for name in pokemon_names:
    if name not in unique_pokemon:
        unique_pokemon.append(name)

# Create unique list of links (some Pokémon share pages)
unique_links = []
for link in completed_links:
    if link not in unique_links:
        unique_links.append(link)

# --------------------------------------------
# STEP 3: ORGANIZE INTO DATAFILE
# --------------------------------------------
# Combine names and links into a DataFrame
link_frame = pd.DataFrame({
    'pokemon': unique_pokemon,
    'url': unique_links
})

# --------------------------------------------
# STEP 4: SETUP FOR DOWNLOADING IMAGES
# --------------------------------------------
# Create folder to store images
folder_name = "pokemon_images"
os.makedirs(folder_name, exist_ok=True)  # Ensure folder exists, if not, make

# Number of times to retry downloading an image if it fails
retry_limit = 3

delay_between_requests = 1  # Seconds

# --------------------------------------------
# STEP 5: DOWNLOAD IMAGES
# --------------------------------------------
total = len(link_frame)
start_time = time.time()
failed_pokemon = []

for counter, (_, row) in enumerate(link_frame.iterrows(), start=1):
    """
    Iterates through a DataFrame of Pokémon names and URLs to download their artwork images.

    Features:
    - Skips Pokémon that have already been downloaded (tracked via a progress file).
    - Attempts to download the official artwork image; falls back to sprite image if artwork is missing.
    - Retries failed downloads up to a specified retry limit.
    - Adds delays between requests to avoid overloading the server.
    - Tracks and displays progress, including estimated time remaining.

    Parameters:
    - link_frame (pd.DataFrame): A DataFrame with 'pokemon' and 'url' columns, containing Pokémon names and their detail page URLs.
    - downloaded (set): Set of Pokémon names already downloaded (read from a progress file).
    - folder_name (str): Directory path where downloaded images will be saved.
    - progress_file (str): Path to a file that logs downloaded Pokémon names.
    - retry_limit (int): Number of retry attempts allowed per Pokémon if an error occurs.
    - total (int): Total number of Pokémon entries (used for status display).

    Returns:
    - Saves each downloaded image with a standardized filename format: "<poke_name>_image.jpg".
    - Prints status updates to the console, including progress, retries, and estimated remaining time.
    - Updates the progress file and `downloaded` set to prevent duplicate work.
    """
    poke_name = row['pokemon'].lower().replace(' ', '_')
    poke_url = row['url']
    img_filename = f"{poke_name}_image.jpg"
    img_path = os.path.join(folder_name, img_filename)

    # Skip if image already exists
    if os.path.exists(img_path):
        print(f"Skipping {poke_name.title()} (image already exists)\n")
        continue

    remaining_total = total - counter
    elapsed_time = time.time() - start_time
    avg_time = elapsed_time / counter
    est_remaining = avg_time * remaining_total
    mins, secs = divmod(int(est_remaining), 60)

    print(f"Downloading image {counter} of {total}: {poke_name.title()}")
    print(f"Remaining: {remaining_total} | Estimated time left: {mins}m {secs}s")

    attempts = 0
    while attempts < retry_limit:
        try:
            page = get(poke_url)
            if page.status_code != 200:
                raise Exception(f"Failed to get page, status code {page.status_code}")

            soup = BeautifulSoup(page.content, 'html.parser')

            # Try official artwork
            image_url = None
            artwork_tag = soup.select_one('a[rel="lightbox"]')
            if artwork_tag and artwork_tag.has_attr('href'):
                image_url = artwork_tag['href']
            else:
                # Try fallback sprite
                sprite_tag = soup.select_one('img[src*="/sprites/"]')
                if sprite_tag and sprite_tag.has_attr('src'):
                    image_url = sprite_tag['src']
                    # Fix malformed or protocol-relative URL
                    if image_url.startswith('//'):
                        image_url = 'https:' + image_url
                    elif image_url.startswith('/'):
                        image_url = 'https://img.pokemondb.net' + image_url

            if image_url:
                img_resp = get(image_url)
                if img_resp.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(img_resp.content)
                    print(f"Saved image to {img_path}\n")
                    break
                else:
                    raise Exception(f"Failed to download image, status code {img_resp.status_code}")
            else:
                print(f"No artwork or sprite found for {poke_name.title()}\n")
                break

        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts} failed for {poke_name.title()}: {e}")
            if attempts == retry_limit:
                print(f"Skipping {poke_name.title()} after {retry_limit} failed attempts\n")
                failed_pokemon.append(poke_name)
            else:
                print("Retrying...\n")
            time.sleep(2)  # wait before retry

    time.sleep(delay_between_requests)

# Log failures
if failed_pokemon:
    print("\nThe following Pokémon failed to download:")
    for name in failed_pokemon:
        print(f"- {name.title()}")

    with open("failed_pokemon.txt", "w") as f:
        for name in failed_pokemon:
            f.write(name + "\n")
else:
    print("\nAll Pokémon images downloaded successfully!")