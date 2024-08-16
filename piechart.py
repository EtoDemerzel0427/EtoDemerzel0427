import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import sys
import time

# Apply the rose-pine-moon.mplstyle
plt.style.use('./rose-pine-moon.mplstyle')

# Function to fetch the JSON file with retry logic
def fetch_json_with_retry(url, retries=10, delay=5):
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            if 'data' in data:
                return data
            else:
                print(f"Attempt {i + 1}: 'data' field not found in the JSON response.")
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Attempt {i + 1}: Error occurred - {e}")
        if i < retries - 1:
            time.sleep(delay)  # Wait before retrying
    sys.exit("Failed to fetch data after several attempts. Exiting script.")

# URL to fetch the JSON data
url = "https://wakatime.com/share/@c2b10ff7-0b0f-409e-a083-aada74b2744c/66cdeaf0-85f3-453c-9430-20dacc5c7787.json"

# Fetch the JSON data
data = fetch_json_with_retry(url)

# Read and prepare the data
df = pd.DataFrame(data["data"])

# Filter out items with a percentage lower than a threshold (e.g., 1%)
threshold = 1
filtered_df = df[df['percent'] >= threshold]
other_percent = 100 - filtered_df['percent'].sum()
other_df = pd.DataFrame([{'name': 'Other', 'percent': other_percent}])
filtered_df = pd.concat([filtered_df, other_df], ignore_index=True)

# Choose a beautiful color palette
palette = sns.color_palette("husl", len(filtered_df))

# Plot the pie chart using seaborn
fig, ax = plt.subplots(figsize=(10, 8))

# Create an "explode" list to separate one random slice
explode = [0.01] * len(filtered_df)
# random_index = random.randint(0, len(filtered_df) - 1)
# explode[random_index] = 0.08

wedges, texts, autotexts = ax.pie(filtered_df['percent'], labels=filtered_df['name'], colors=palette,
                                  autopct='%1.1f%%', startangle=90, pctdistance=0.85, textprops=dict(color="w"),
                                  explode=explode, shadow=True, labeldistance=1.05)

# Add a circle in the center with the background color
bg_color = plt.rcParams['axes.facecolor']
circle = plt.Circle((0, 0), 0.70, fc=bg_color)

# Equal aspect ratio ensures the pie chart is circular
ax.axis('equal')
ax.add_artist(circle)
plt.title("Programming Language Percentages")
plt.tight_layout()
plt.savefig("language_percentages.png")
