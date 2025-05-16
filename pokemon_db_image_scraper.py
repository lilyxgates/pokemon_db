# ============================================
# Pokémon Image Scraper
# Author: Lily Gates
# Date: May 2025
# Description:
# Scrapes Pokémon names and image links from pokemondb.net,
# downloads each Pokémon's official artwork, and saves it locally.
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
os.makedirs(folder_name, exist_ok=True)

# File to store progress of downloaded Pokémon
progress_file = "downloaded_pokemon.txt"

# Retry limit for failed downloads
retry_limit = 3

# Ensure the progress file exists
if not os.path.exists(progress_file):
    with open(progress_file, 'w') as f:
        pass  # Just create an empty file

# Load previously downloaded Pokémon to skip them
if os.path.exists(progress_file):
    with open(progress_file, "r") as f:
        downloaded = set(line.strip() for line in f)
else:
    downloaded = set()

# --------------------------------------------
# STEP 5: DOWNLOAD IMAGES
# --------------------------------------------


total = len(link_frame)

for index, row in link_frame.iterrows():
    poke_name = row['pokemon'].lower().replace(' ', '_')
    """
    Usage:
    - Iterates through a DataFrame of Pokémon names and URLs and downloads the artwork image
    - Skips Pokémon that have already been downloaded (tracked via a progress file)
    - Retries failed downloads up to a specified retry limit
    - Adds delays between requests to avoid overloading the server

    Parameters:
    - link_frame (pd.DataFrame): A DataFrame containing Pokémon names and their corresponding detail page URLs.
    - downloaded (set): A set of Pokémon names already downloaded (read from a progress file).
    - folder_name (str): Path to the folder where images will be saved.
    - progress_file (str): Path to the text file tracking downloaded Pokémon.
    - retry_limit (int): Maximum number of retry attempts per Pokémon on failure.
    - total (int): Total number of Pokémon in the list (used for progress printing).

    Returns:
    - For each Pokémon, fetches its individual page, extracts the official artwork image URL,
    downloads the image, and saves it using a formatted filename.
    - Logs status messages to the console throughout the process.
    - Adds each successfully processed Pokémon to the progress file to prevent re-downloading.
    """

    # Skip already downloaded Pokémon
    if poke_name in downloaded:
        print(f"Skipping {poke_name.title()} (already downloaded)")
        continue

    poke_url = row['url']
    print(f"Downloading image {index + 1} of {total}: {poke_name.title()}")

    attempts = 0
    while attempts < retry_limit:
        try:
            # Get Pokémon page
            page = get(poke_url)
            if page.status_code != 200:
                raise Exception(f"Failed to get page, status code {page.status_code}")

            soup = BeautifulSoup(page.content, 'html.parser')
            artwork_tag = soup.select_one('a[rel="lightbox"]')

            # If artwork link found, download image
            if artwork_tag and artwork_tag.has_attr('href'):
                artwork_url = artwork_tag['href']
                img_resp = get(artwork_url)

                if img_resp.status_code == 200:
                    img_path = os.path.join(folder_name, f"{poke_name}_image.jpg")
                    with open(img_path, 'wb') as f:
                        f.write(img_resp.content)
                    print(f"Saved image to {img_path}\n")

                    # Record progress
                    with open(progress_file, "a") as f:
                        f.write(poke_name + "\n")
                    downloaded.add(poke_name)
                    break
                else:
                    raise Exception(f"Failed to download image, status code {img_resp.status_code}")
            else:
                print(f"No artwork image found for {poke_name.title()}\n")
                # Still record progress so we skip next time
                with open(progress_file, "a") as f:
                    f.write(poke_name + "\n")
                downloaded.add(poke_name)
                break

        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts} failed for {poke_name.title()}: {e}")
            if attempts == retry_limit:
                print(f"Skipping {poke_name.title()} after {retry_limit} failed attempts\n")
            else:
                print("Retrying...\n")
            time.sleep(2)  # Wait before retrying

    time.sleep(1)  # Be polite to the server
