import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

from utils import *

def get_html_from_url(url):

    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_page_setlist_htmls(soup):
    setlist_urls = []

    for link in soup.find_all("a"):
        link_str = link.get('href')
        if link_str and link_str.startswith('../setlist/'):
            cleaned_link_str = link_str.replace('../', core_setlist_url)
            setlist_urls.append(cleaned_link_str)
    
    return [get_html_from_url(url) for url in setlist_urls]

def parse_setlist(page_setlist_htmls):
    setlist_data = []

    for setlist_html in page_setlist_htmls:
        soup = BeautifulSoup(setlist_html, "html.parser")
        month, day, year = soup.find(class_="month").text.strip(), soup.find(class_="day").text.strip(), soup.find(class_="year").text.strip()
        # Reformat the data into desired format
        day = day if len(day) == 2 else "0" + day
        date = f"{month_conversion[month]}/{day}/{year}"

        # Check if show has happened
        show_date = datetime.strptime(date, "%m/%d/%Y").date()
        today = datetime.today().date()
        if show_date >= today:
            continue

        venue_info = soup.find(class_="setlistHeadline").text.strip()
        
        venue_name = re.search(venue_name_pattern, venue_info).group(1).strip()
        setlist_items = soup.find_all("li", class_="setlistParts")
        songs = [item.text.strip() for item in setlist_items if item.text.strip()]
        if "Encore 2:" in songs:
            songs.remove("Encore 2:")
        if "Set: 1:" in songs:
            songs[0] = "Set 1:"
        if "Set: 2:" in songs:
            temp_idx = songs.index("Set: 2:")
            songs[temp_idx] = "Set 2:"
        
        idxE = extract_set(songs, "Encore:")
        encore = extract_songs(songs, idxE + 1) if idxE else []

        idx2 = extract_set(songs, "Set 2:")
        set2 = []

        idx3 = extract_set(songs, "Set 3:")
        set3 = []

        if idx3:  # if there was a set3, then there was a set1 and set2
            set3 = extract_songs(songs, idx3 + 1, idxE if idxE else None)

        if idx2:
            set2 = extract_songs(songs, idx2 + 1, idx3 if idx3 else (idxE if idxE else None))
            set1 = extract_songs(songs, 1, idx2)
        else:
            set1 = extract_songs(songs, 1, idxE if idxE else None)


        setlist_data.append({
            'date': date,
            'venue_name': venue_name,
            'set1': set1,
            'set2': set2,
            'set3': set3,
            'encore': encore
        })
    
    return setlist_data


def get_all_setlists(base_url, page_count):
    all_setlists_data = []

    for page in range(1, pages+1):  # edit back to range(1, pages+1)
        url = f"{base_url}?page={page}"
        outer_soup = BeautifulSoup(get_html_from_url(url), "html.parser")
        page_setlist_htmls = get_page_setlist_htmls(outer_soup)
        setlist_data = parse_setlist(page_setlist_htmls)
        all_setlists_data.extend(setlist_data)

    return all_setlists_data



if __name__ == "__main__":
    all_setlist_data = get_all_setlists(base_url, pages)
    df = pd.DataFrame(all_setlist_data)
    df.to_csv("/Users/mwshumway/Desktop/DeadAndCo/setlists.csv", index=False)
    print("Successfully converted to CSV")


