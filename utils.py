base_url = "https://www.setlist.fm/setlists/dead-and-company-2bc42076.html"
core_setlist_url = "https://www.setlist.fm/"
pages = 25

month_conversion = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

venue_name_pattern = r'at\s+(.+?)\n'

colors = ['blue', 'red', 'white', 'black']  # You can customize this list



def extract_songs(songs, start, end=None):
    try:
        ret = [song[:song.index('\n')] for song in songs[start:end]]
        return ret
    except ValueError:
        print(songs)
    

def extract_set(songs, set_name):
    if set_name in songs:
        return songs.index(set_name)
    return None

