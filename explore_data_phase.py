"""Matthew Shumway
06/13/2024

explore_data_phase.py

Now that all Dead and Co data is stored in setlists.csv, the purpose of this file will be to explore some 
insights into the data. What I'm thinking so far:

- Total number of distinct songs ever played by Dead and Co - get an idea of what the repoitare of songs is
- Total number of songs ever played
- Most frequently played songs (top 30-50?)
- 2024 Most frequently played songs
- What days of the week they play (guessing Thursday, Friday, Saturday)
- Distribution of songs played on each day (most popular on Thursday, most popular on Friday, etc.)
- For each song, is it more frequently played in the first, second, third, or encore set?
- Song transition - for each song, which songs precede it? which songs come after it?
- (Maybe) special dates/anniversiries - Jerry Garcia's death date?
_ Per tour, which songs are the most popular?
"""

import pandas as pd
from matplotlib import pyplot as plt
import itertools
from collections import Counter
import numpy as np
from utils import *


def num_distinct_songs(df, return_set=False):
    all_songs_set = set()

    for column in ['set1', 'set2', 'set3', 'encore']:
        all_songs_set.update(list(itertools.chain.from_iterable(df[column])))

    if return_set:
        return len(all_songs_set), all_songs_set
    else:
        return len(all_songs_set)
    
def num_total_songs(df):
    return sum([len(list(itertools.chain.from_iterable(df[column]))) for column in ["set1", "set2", "set3", "encore"]])

def all_time_most_played(df, num, year=None):
    plt.figure(figsize=(12,8))

    if year:
        df['date'] = pd.to_datetime(df['date'])
        df_date = df[df['date'].dt.year == year]
    else:
        df_date = df

    all_songs_list = []

    for column in ["set1", "set2", "set3", "encore"]:
        all_songs_list.extend(list(itertools.chain.from_iterable(df_date[column])))
    
    count_dict = dict(Counter(all_songs_list))

    sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    # top_freq = [item[0] for item in sorted_items[:num]]

    songs, freq = zip(*sorted_items)
    songs, freq = list(songs), np.array(list(freq)) / len(all_songs_list)

    start = 3 if year == 2024 else 2  # 2024 has the video clip played at every show at the Sphere

    plt.bar(songs[start:num+start], freq[start:num+start], color=colors, edgecolor='black')  # first 2 are always drums and space
    plt.xticks(rotation=90)
    plt.xlabel("SONGS")
    plt.ylabel("FREQUENCY")
    plt.ylim(0.006, None)
    plt.subplots_adjust(bottom=0.4)  # Increase the left margin
    plt.title("All time most played songs") if not year else plt.title(f"Most played songs in {year}")
    plt.show()

def day_of_the_week_frequency(df):
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    day_counts = df['day_of_week'].value_counts()
    day_counts.plot(kind='bar', color=colors, edgecolor='black')
    plt.xlabel('Day of the Week')
    plt.xticks(rotation=45)
    plt.ylabel('Count')
    plt.title('Occurrences of Each Day of the Week')
    plt.show()

def most_played_day_of_week(df, num):
    """Plots a 2x4 subplot grid displaying the (num) most popular songs on each of the seven days of the week
    Consider adding a year parameter to do it based on a desired year or frame.
    """
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    songs_by_day = {day: [] for day in df['day_of_week'].unique()}
    
    for index, row in df.iterrows():
        day = row['day_of_week']
        for col in ['set1', 'set2', 'set3', 'encore']:
            songs_by_day[day].extend(row[col])
    
    for day in df["day_of_week"].unique():
        songs_by_day[day] = [song for song in songs_by_day[day] if song not in ["Drums", "Space"]]

    song_counts_by_day = {day: Counter(songs) for day, songs in songs_by_day.items()}
    sorted_songs_by_day = {day: dict(counts.most_common(num)) for day, counts in song_counts_by_day.items()}

    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(16, 8))
    axes = axes.ravel()

    for i, (day, top_songs) in enumerate(sorted_songs_by_day.items()):
        ax = axes[i]
        ax.bar(top_songs.keys(), top_songs.values(), color=colors, edgecolor='black')
        ax.set_title(day)
        ax.set_xlabel('Song')
        ax.set_ylabel('Popularity')
        ax.tick_params(axis='x', rotation=90)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Load the dataframe
    df = pd.read_csv("/Users/mwshumway/Desktop/DeadAndCo/setlists.csv")
    for column in ["set1", "set2", "set3", "encore"]:
        df[column] = df[column].apply(eval)
    print("\n" + "Informative Statistics about Dead & Co. setlists")
    print("=" * 100)
    print("All time number of total songs played: " + str(num_total_songs(df)))
    print("All time number of distinct songs played: " + str(num_distinct_songs(df)))
    # all_time_most_played(df, 50, 2024)  
    # day_of_the_week_frequency(df)
    most_played_day_of_week(df, 5)
    
