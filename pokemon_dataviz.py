# ============================================
# Pokémon Data Visualization
# Author: Lily Gates
# Date: May 2025
# Description:
# Combines the data scraped from `pokemon_db.py` and `pokemon_db_image_scraper`
# Creates different data visualizations
# ============================================

# Import required packages
import os
from datetime import datetime

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.stats import pearsonr

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.image as mpimg

import seaborn as sns

# --------------------------------------------
# STEP 1: Load in Dataset
# --------------------------------------------
pokemon_csv = pd.read_csv('pokemon_db.csv')
#pokemon_csv.head()
#pokemon_csv.columns

# Create folder to save all graphs if it doesn't exist
output_dir = "pokemon_graphs"
os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------
# STEP 2: Setup Custom Theme Template
# --------------------------------------------
# Custom Theme for Graphs

# Define your custom style
custom_style = {
    # Font and text
    'axes.titlesize': 18,
    'axes.titleweight': 'bold',
    'axes.titlelocation': 'center',
    'axes.labelsize': 14,
    'axes.labelweight': 'normal',

    # Tick params
    'xtick.major.width': 2,
    'ytick.major.width': 2,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,

    # Axis spine width
    'axes.linewidth': 2,

    # Font family and default
    'font.size': 12,
    'font.style': 'normal',

    # Grid and background
    'axes.grid': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
}

# Apply the style globally
plt.rcParams.update(custom_style)

# --------------------------------------------
# STEP 3: Create Visualizations
# --------------------------------------------

# ----------------------------------------------------------------------------------------
## 1. Relationship Between Height and Weight in Pokémon (Scatterplot with Regression Line)
# ----------------------------------------------------------------------------------------
# Original data
x = pokemon_csv['weight_kg']
y = pokemon_csv['height_meters']

# Transformed data (sqrt)
epsilon = 1e-6
x_sqrt = np.sqrt(x + epsilon)
y_sqrt = np.sqrt(y + epsilon)

# Create figure with 2 subplots side-by-side
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False)

# --- LEFT PLOT: Original data ---
ax = axes[0]

# Regression on original data
slope, intercept = np.polyfit(x, y, 1)
sns.regplot(x=x, y=y, ax=ax, scatter_kws={'alpha':0.4, 's':5, 'color': 'steelblue'}, line_kws={'color': 'darkblue'})

# Calculate stats
pearson_r, _ = stats.pearsonr(x, y)
r_squared = pearson_r**2

# Annotate on left plot
equation = r"$y = {0:.2f}x + {1:.2f}$".format(slope, intercept)
pearson_r_text = r"$r = {0:.3f}$".format(pearson_r)
r_squared_text = r"$R^2 = {0:.3f}$".format(r_squared)

for i, text in enumerate([equation, pearson_r_text, r_squared_text]):
    ax.annotate(
        text,
        xy=(0.95, 0.875 - i*0.1),
        xycoords='axes fraction',
        fontsize=10,
        color='black',
        verticalalignment='bottom',
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor=(1,1,1,0.5), edgecolor='black', linewidth=1, pad=0.5)
    )

# Titles and labels for left plot
ax.set_title("Height vs Weight (Original Data)", fontsize=14, weight='bold')
ax.set_xlabel("Weight (kg)", fontsize=12)
ax.set_ylabel("Height (meters)", fontsize=12)

# --- RIGHT PLOT: Transformed data ---
ax = axes[1]

# Regression on sqrt transformed data
slope_t, intercept_t = np.polyfit(x_sqrt, y_sqrt, 1)
sns.regplot(x=x_sqrt, y=y_sqrt, ax=ax, scatter_kws={'alpha':0.4, 's':5, 'color': 'steelblue'}, line_kws={'color': 'darkblue'})

# Calculate stats transformed
pearson_r_t, _ = stats.pearsonr(x_sqrt, y_sqrt)
r_squared_t = pearson_r_t**2

# Annotate on right plot
equation_t = r"$y = {0:.2f}x + {1:.2f}$".format(slope_t, intercept_t)
pearson_r_text_t = r"$r = {0:.3f}$".format(pearson_r_t)
r_squared_text_t = r"$R^2 = {0:.3f}$".format(r_squared_t)

for i, text in enumerate([equation_t, pearson_r_text_t, r_squared_text_t]):
    ax.annotate(
        text,
        xy=(0.95, 0.875 - i*0.1),
        xycoords='axes fraction',
        fontsize=10,
        color='black',
        verticalalignment='bottom',
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor=(1,1,1,0.5), edgecolor='black', linewidth=1, pad=0.5)
    )

# Titles and labels for right plot
ax.set_title("Height vs Weight (Square Root Transformed)", fontsize=14, weight='bold')
ax.set_xlabel("Square Root of Weight (kg)", fontsize=12)
ax.set_ylabel("Square Root of Height (meters)", fontsize=12)

# Overall figure title and subtitle
fig.suptitle("\nRelationship between Height and Weight in Pokémon", fontsize=24, weight='bold', y=1.18)
fig.text(0.5, 1, "Comparison of Original and Transformed Data with Linear Regression", 
         ha='center', fontsize=18, style='italic')

# Save File
filename = "height_vs_weight_comparison.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# ----------------------------------------------------------------------------------------
## 2. Base Stat Distribution (Histogram)
# ----------------------------------------------------------------------------------------
stats = ['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed']
display_names = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()

for ax, stat, name in zip(axes, stats, display_names):
    ax.hist(pokemon_csv[stat].dropna(), bins=20, color='skyblue', edgecolor='black', density=True)
    ax.set_title(name)
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Format y-axis as percentage
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))

# Overall figure title and subtitle
fig.suptitle("\nBase Stat Distributions",
             fontsize=24, weight='bold', y=1.05)

fig.text(0.5, .92, 'X-axis: Stat Value | Y-axis: Percentage of Pokémon',
         ha='center', fontsize=18, style='italic')


plt.tight_layout()

# Save File
filename = "base_stat_distrib_histogram.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# ----------------------------------------------------------------------------------------
## 3. Percentage of Pokemon with Different Elemental Types (Stacked Bar Graph)
# ----------------------------------------------------------------------------------------
# Calculate proportions for elem_1 and elem_2
elem_1_prop = pokemon_csv['elem_1'].value_counts(normalize=True)
elem_2_prop = pokemon_csv['elem_2'].value_counts(normalize=True)

# Combine into a DataFrame, filling missing types with 0
type_df = pd.DataFrame({
    'Primary': elem_1_prop,
    'Secondary': elem_2_prop
}).fillna(0)

# Convert proportions to percentages
type_df = type_df * 100

# Add a total percentage column
type_df['Total'] = type_df['Primary'] + type_df['Secondary']

# Sort by total percentage descending
type_df = type_df.sort_values('Total', ascending=False)

# Plot stacked bar graph
fig, ax = plt.subplots(figsize=(14, 7))

type_df['Primary'].plot(kind='bar', color='#3D6682', ax=ax, width=0.7, label='Primary')
type_df['Secondary'].plot(kind='bar', color='#44A778', ax=ax, bottom=type_df['Primary'], width=0.7, label='Secondary')

ax.set_xlabel('Pokémon Type')
ax.set_ylabel('Percentage (%)')
ax.set_xticklabels(type_df.index, rotation=45)
ax.set_ylim(0, type_df['Total'].max() * 1.1)
ax.legend(title='Type Category')

# Main title above the figure
fig.suptitle("\nDistribution of Pokémon Types by Primary and Secondary Categories",
             fontsize=24, weight='bold', y=1.05)

# Subtitle just below the main title
fig.text(0.5, 0.90, 'Stacked Bar Chart Showing the Percentage of Pokémon by Elemental type',
         ha='center', fontsize=18, style='italic')

plt.tight_layout()

# Save File
filename = "element_type_stacked_bar.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# ----------------------------------------------------------------------------------------
## 4. Frequency of Pokémon Elemental Types (Heatmap)
# ----------------------------------------------------------------------------------------
# Create the dual-type frequency matrix
dual_type_counts = pokemon_csv.pivot_table(index='elem_1', 
                                           columns='elem_2', 
                                           aggfunc='size', 
                                           fill_value=0)

# Calculate row and column sums for sorting
row_sums = dual_type_counts.sum(axis=1)
col_sums = dual_type_counts.sum(axis=0)
dual_type_counts_sorted = dual_type_counts.loc[
    row_sums.sort_values(ascending=False).index,
    col_sums.sort_values(ascending=False).index
]

# Replace 0s with NaN for color masking
data_alpha = dual_type_counts.replace(0, np.nan)
data_sorted = dual_type_counts_sorted.replace(0, np.nan)

# Create annotation matrices
annot_alpha = dual_type_counts.applymap(lambda x: str(x) if x > 0 else '')
annot_sorted = dual_type_counts_sorted.applymap(lambda x: str(x) if x > 0 else '')

# Set up the colormap
cmap = plt.cm.RdPu
cmap.set_bad(color='white')

# Normalize for colorbars (shared scale)
norm = plt.Normalize(vmin=np.nanmin(dual_type_counts.values), vmax=np.nanmax(dual_type_counts.values))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Create figure with 2 rows, 2 columns: heatmaps in left column, colorbars in right column
fig = plt.figure(figsize=(15, 20), constrained_layout=True)
gs = fig.add_gridspec(2, 2, width_ratios=[20, 1])

# Top heatmap (A: sorted by frequency)
ax1 = fig.add_subplot(gs[0, 0])
sns.heatmap(data_sorted, annot=annot_sorted,
            fmt='', cmap=cmap, cbar=False,
            ax=ax1, annot_kws={"size": 15})
ax1.set_title('\nA. Sorted by Frequency\n', fontsize=18, weight='bold')
ax1.set_xlabel('Secondary Type', fontsize=14, weight='bold')
ax1.set_ylabel('Primary Type', fontsize=14, weight='bold')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)

# Colorbar for top heatmap (vertical)
cbar_ax1 = fig.add_subplot(gs[0, 1])
cbar1 = fig.colorbar(sm, cax=cbar_ax1, orientation='vertical')
cbar1.set_label('', fontsize=16, weight='bold')
cbar1.ax.tick_params(labelsize=14)

# Bottom heatmap (B: alphabetical order)
ax2 = fig.add_subplot(gs[1, 0])
sns.heatmap(data_alpha, annot=annot_alpha,
            fmt='', cmap=cmap, cbar=False,
            ax=ax2, annot_kws={"size": 15})
ax2.set_title('\nB. Alphabetical Order\n', fontsize=18, weight='bold')
ax2.set_xlabel('Secondary Type', fontsize=14, weight='bold')
ax2.set_ylabel('Primary Type', fontsize=14, weight='bold')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)

# Colorbar for bottom heatmap (vertical)
cbar_ax2 = fig.add_subplot(gs[1, 1])
cbar2 = fig.colorbar(sm, cax=cbar_ax2, orientation='vertical')
cbar2.set_label('', fontsize=16, weight='bold')
cbar2.ax.tick_params(labelsize=14)

# Shared title and subtitle
fig.suptitle('\nFrequency of Pokémon Dual Types (Primary vs. Secondary)', 
             fontsize=24, weight='bold', y=1.09)

fig.text(0.5, 1.02, 
         'A: Types Ordered by Total Frequency | B: Types Ordered Alphabetically\nWhite = No Pokémon with That Combination', 
         ha='center', fontsize=18, style='italic')

# Save File
filename = "dual_type_heat_graph.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# ----------------------------------------------------------------------------------------
## 5. Average Base Stats by Primary Elemental Type (Radial Graph)
# # ----------------------------------------------------------------------------------------
ordered_stats = ['hp', 'defense', 'sp_def', 'speed', 'attack', 'sp_atk']
display_names = ['HP', 'Defense', 'Sp. Def', 'Speed', 'Attack', 'Sp. Atk']

elements_stats_pivot = pd.pivot_table(
    pokemon_csv,
    values=ordered_stats,
    index='elem_1',
    aggfunc='mean',
    margins=True,               # adds the margins (totals/averages)
    margins_name='Overall Average'  # custom name for the totals row and column
)

# Rename columns and index label for readability
elements_stats_pivot.columns = display_names
elements_stats_pivot.index.name = 'Primary Type'

# DataFrame Pivot Table
elements_stats_pivot = elements_stats_pivot.round(1)
print(elements_stats_pivot)

# Define stats and display names
ordered_stats = ['hp', 'defense', 'sp_def', 'speed', 'attack', 'sp_atk']
display_names = ['HP', 'Defense', 'Sp. Def', 'Speed', 'Attack', 'Sp. Atk']

# Rotate the stat order by N positions (e.g., start at index 3)
rotation_index = 3
ordered_stats = ordered_stats[rotation_index:] + ordered_stats[:rotation_index]
display_names = display_names[rotation_index:] + display_names[:rotation_index]

# Group by primary type and compute mean stats
type_avg = pokemon_csv.groupby('elem_1')[ordered_stats].mean()

# Setup for radar plot
num_vars = len(ordered_stats)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Close the loop

types = sorted(type_avg.index.tolist())
n_types = len(types)

# Grid layout
n_cols = 3
n_rows = int(np.ceil(n_types / n_cols))

# Set up the subplot grid with polar projection
fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 4, n_rows * 4), subplot_kw=dict(polar=True))
axes = axes.flatten()

max_radius = type_avg.values.max()

# Plot each type
for i, type_ in enumerate(types):
    values = type_avg.loc[type_].tolist()
    values += values[:1]

    ax = axes[i]
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(display_names, fontsize=8)

    # Remove radial labels and set consistent range
    ax.set_yticklabels([])
    ax.set_ylim(0, max_radius)

    # Add stat values with white box and black outline
    for angle, value in zip(angles[:-1], values[:-1]):
        ax.text(
            angle,
            value + max_radius * 0.03,  # slightly outside the data point
            f"{value:.1f}",
            ha='center',
            va='center',
            fontsize=7,
            color='black',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
        )

    pretty_name = type_.title()
    ax.set_title(pretty_name, fontsize=12, fontweight='bold', y=1.01, color='black')

# Hide any unused subplots if total plots < grid size
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Adjust spacing between subplots
fig.subplots_adjust(hspace=3, wspace=5)

# Shared title and subtitle
fig.suptitle('\nAverage Base Stats by Primary Element Type',
             fontsize=24, weight='bold', y=1.025)

fig.text(0.5, 0.98,
         'Visualizing the Balance of Stat Profiles with Mini Coxcomb Charts',
         ha='center', fontsize=18, style='italic')

plt.tight_layout()

# Save File
filename = "avg_base_stats_by_element_type_radial_graphs.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# ----------------------------------------------------------------------------------------
## 6. Deviations in Pokémon Base Stats by Primary Elemental Type
# # ----------------------------------------------------------------------------------------
# Ordered stats and display names
ordered_stats = ['hp', 'defense', 'sp_def', 'speed', 'attack', 'sp_atk']
display_names = ['HP', 'Defense', 'Sp. Def', 'Speed', 'Attack', 'Sp. Atk']

# Create the pivot table with overall average (margins)
elements_stats_pivot = pd.pivot_table(
    pokemon_csv,
    values=ordered_stats,
    index='elem_1',
    aggfunc='mean',
    margins=True,
    margins_name='Overall Average'
)

# Rename columns and index name
elements_stats_pivot.columns = display_names
elements_stats_pivot.index.name = 'Primary Type'

# Round for nicer display
elements_stats_pivot = elements_stats_pivot.round(1)

# Calculate difference from overall average (excluding the overall average row itself)
overall_avg = elements_stats_pivot.loc['Overall Average']
diff = elements_stats_pivot.drop('Overall Average').subtract(overall_avg)

# Plotting parameters
types = diff.index.tolist()
n_types = len(types)
n_cols = 3
n_rows = int(np.ceil(n_types / n_cols))

fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4))
axes = axes.flatten()

for i, type_ in enumerate(types):
    ax = axes[i]
    values = diff.loc[type_]
    
    # Colors: blue if above average, orange if below average
    colors = ['#0072B2' if v >= 0 else '#D55E00' for v in values]
    
    bars = ax.bar(display_names, values, color=colors)
    
    # Add value labels with white box and black outline
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2, height,
            f'{height:.1f}',
            ha='center', 
            va='bottom' if height >= 0 else 'top',
            fontsize=9,
            fontweight='bold',
            color='black',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2')
        )
    
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title(type_.title(), fontsize=15, weight='bold')
    
    ax.set_xticks(range(len(display_names)))
    ax.set_xticklabels(display_names, rotation=0, ha='center', fontsize=11)
    
    # Set y-axis limits with some padding
    min_y = diff.values.min()
    max_y = diff.values.max()
    ax.set_ylim(min_y - 5, max_y + 5)

# Remove any unused axes (if n_types < n_rows * n_cols)
for j in range(n_types, n_rows * n_cols):
    fig.delaxes(axes[j])


# Title and subtitle
fig.suptitle('\nDeviations in Pokémon Base Stats by Primary Type',
             fontsize=24, weight='bold', y=1.025)

fig.text(0.5, 0.98,
         'Visualizing how average stats differ from overall population means across Pokémon types',
         ha='center', fontsize=18, style='italic')

plt.tight_layout()

# Save File
filename = "deviations_in_base_stats_by_element_type_bar.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# ----------------------------------------------------------------------------------------
## 7. Top 10 Pokémon by Base Stat Category
# ----------------------------------------------------------------------------------------
stats = ['hp', 'defense', 'sp_def', 'speed', 'attack', 'sp_atk']

display_names = {
    'hp': 'HP',
    'defense': 'Defense',
    'sp_def': 'Sp. Defense',
    'speed': 'Speed',
    'attack': 'Attack',
    'sp_atk': 'Sp. Attack'
}

fig, axes = plt.subplots(3, 2, figsize=(12, 24))
axes = axes.flatten()

num_items = 10
top_margin = 0.93
bottom_margin = 0.07
vertical_space = top_margin - bottom_margin

spacing = vertical_space / (num_items - 0.7)

for ax, stat in zip(axes, stats):
    top10 = pokemon_csv.sort_values(stat, ascending=False).head(10).reset_index(drop=True)
    ax.axis('off')
    ax.set_title(f'Top 10 Pokémon by {display_names[stat]}',
                 fontsize=16, fontweight='bold', pad=20, loc='center', y=0.98)

    for i, pokemon_name in enumerate(top10['pokemon']):
        img_filename = pokemon_name.lower().replace(' ', '_') + '_image.jpg'
        img_path = os.path.join('pokemon_images', img_filename)

        y_pos = top_margin - i * spacing
        stat_value = top10.loc[i, stat]

        # Adjust x positions for better alignment
        x_name = 0.15
        x_image = 0.6
        x_stat = 0.75

        ax.text(x_name, y_pos, f"{i+1}. {pokemon_name}", fontsize=16, va='center', transform=ax.transAxes)
        ax.text(x_stat, y_pos, f"{stat_value}", fontsize=16, va='center', transform=ax.transAxes)

        if os.path.exists(img_path):
            image_ax = ax.inset_axes([x_image, y_pos - 0.039, 0.1, 0.1], transform=ax.transAxes)
            image_ax.imshow(mpimg.imread(img_path))
            image_ax.axis('off')

fig.suptitle('\nTop 10 Pokémon by Base Stat Categories',
             fontsize=24, weight='bold', y=1.0)

fig.text(0.5, 0.94,
         'Highest Scoring in HP, Defense, Sp. Defense, Speed, Attack, and Sp. Attack',
         ha='center', fontsize=18, style='italic')

fig.tight_layout(rect=[0, 0, 1, 0.95])

filename = "top_10_by_base_stat.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# ----------------------------------------------------------------------------------------
## 8. Top 10 Pokémon by Total Base Stat, Grouped by Elemental Type
# # ----------------------------------------------------------------------------------------

# # ----------------------------------------------------------------------------------------
### 8a. Grouped by Primary AND Secondary Elemental Type
# # ----------------------------------------------------------------------------------------
elements = pokemon_csv['elem_1'].dropna().unique()
n_cols = 3
n_rows = 6
fig, axes = plt.subplots(n_rows, n_cols, figsize=(22, 36))  # Bigger figure for larger content
axes = axes.flatten()

num_items = 10
top_margin = 0.92
bottom_margin = 0.05
vertical_space = top_margin - bottom_margin
spacing = vertical_space / (num_items - 1.2)  # Increased spacing for bigger font/images

for ax, elem in zip(axes, elements):
    subset = pokemon_csv[(pokemon_csv['elem_1'] == elem) | (pokemon_csv['elem_2'] == elem)]
    top10 = subset.sort_values('total', ascending=False).head(10).reset_index(drop=True)

    ax.axis('off')
    ax.set_title(f'Top 10 {elem} Pokémon', fontsize=20, fontweight='bold', pad=20, y=0.95)

    for i, row in top10.iterrows():
        name = row['pokemon']
        total = row['total']
        img_name = name.lower().replace(' ', '_')
        img_path = os.path.join('pokemon_images', f"{img_name}_image.jpg")

        y_pos = top_margin - i * spacing

        ax.text(0.05, y_pos, f"{i+1}. {name} (Total: {total})", fontsize=22, va='center', transform=ax.transAxes)
        
        if os.path.exists(img_path):
            img = mpimg.imread(img_path)
            imagebox = ax.inset_axes([0.7, y_pos - 0.045, 0.095, 0.095], transform=ax.transAxes)
            imagebox.imshow(img)
            imagebox.axis('off')

# Main title and subtitle
fig.suptitle('\nTop 10 Pokémon by Total Base Stat\nGrouped by Primary or Secondary Elemental Type',
             fontsize=32, weight='bold', y=0.96)

fig.text(0.5, 0.905,
         'Ranking Pokémon by total base stats within each primary or secondary elemental type',
         ha='center', fontsize=26, style='italic')

plt.tight_layout(rect=[0, 0, 1, 0.94])

# Save file
filename = "top_10_total_stats_by_primary_and_secondary_elements.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()

# # ----------------------------------------------------------------------------------------
### 8b. Grouped by Primary ONLY Elemental Type
# # ----------------------------------------------------------------------------------------
elements = pokemon_csv['elem_1'].dropna().unique()
n_cols = 3
n_rows = 6
fig, axes = plt.subplots(n_rows, n_cols, figsize=(22, 36))  # Bigger figure for larger content
axes = axes.flatten()

num_items = 10
top_margin = 0.92
bottom_margin = 0.05
vertical_space = top_margin - bottom_margin
spacing = vertical_space / (num_items - 1.2)  # Increased spacing for bigger font/images

for ax, elem in zip(axes, elements):
    subset = pokemon_csv[pokemon_csv['elem_1'] == elem]
    top10 = subset.sort_values('total', ascending=False).head(10).reset_index(drop=True)
    count = top10.shape[0]

    ax.axis('off')
    ax.set_title(f'Top 10 {elem} Pokémon', fontsize=20, fontweight='bold', pad=20, y=0.95)

    for i in range(10):
        y_pos = top_margin - i * spacing

        if i < count:
            row = top10.loc[i]
            name = row['pokemon']
            total = row['total']
            img_name = name.lower().replace(' ', '_')
            img_path = os.path.join('pokemon_images', f"{img_name}_image.jpg")

            ax.text(0.05, y_pos, f"{i+1}. {name} (Total: {total})", fontsize=22, va='center', transform=ax.transAxes)

            if os.path.exists(img_path):
                img = mpimg.imread(img_path)
                imagebox = ax.inset_axes([0.7, y_pos - 0.045, 0.095, 0.095], transform=ax.transAxes)
                imagebox.imshow(img)
                imagebox.axis('off')
        else:
            # Placeholder row
            ax.text(0.05, y_pos, f"{i+1}. Not enough Pokémon meet this criteria", 
                    fontsize=18, color='gray', va='center', style='italic', transform=ax.transAxes)



# Main title and subtitle
fig.suptitle('\nTop 10 Pokémon by Total Base Stat\nGrouped by Primary Elemental Type',
             fontsize=32, weight='bold', y=0.96)

fig.text(0.5, 0.905,
         'Ranking Pokémon by total base stats within each primary elemental type',
         ha='center', fontsize=26, style='italic')

plt.tight_layout(rect=[0, 0, 1, 0.94])


# Save file
filename = "top_10_total_stats_by_primary_only_elements.png"
save_path = os.path.join("pokemon_graphs", filename)
fig.savefig(save_path, bbox_inches='tight')
print(f"Graph saved to: {save_path}")

plt.show()
