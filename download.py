import pickle
import requests
from bs4 import BeautifulSoup

def get_artist_pages_count(artist_slug):
    artist_url = f'https://tekstowo.pl/piosenki_artysty,{artist_slug}.html'
    response = requests.get(artist_url)
    soup = BeautifulSoup(response.text, 'html5lib')
    pagination = soup.find('ul', class_='pagination')
    if pagination is None:
        return 1
    return int(pagination.find_all('li')[-2].text)

def get_page_songs(artist_slug, page_no):
    artist_url = f'https://tekstowo.pl/piosenki_artysty,{artist_slug},strona,{page_no}.html'
    response = requests.get(artist_url)
    soup = BeautifulSoup(response.text, 'html5lib')
    for piosenka in soup.find('div', class_='content').find('div', class_='ranking-lista').find_all('div', class_='box-przeboje'):
        yield 'https://tekstowo.pl' + piosenka.a['href']

def get_artist_songs(artist_slug):
    page_count = get_artist_pages_count(artist_slug)
    for page_no in range(1, page_count+1):
        yield from get_page_songs(artist_slug, page_no)

def get_song_lyrics(song_url):
    response = requests.get(song_url)
    soup = BeautifulSoup(response.text, 'html5lib')
    text = soup.find('div', class_='song-text').text
    lyrics = text.replace('Tekst piosenki:', '').replace('Poznaj historię zmian tego tekstu', '').strip()
    return lyrics

def get_artist_lyrics(artist_slug):
    for song_url in get_artist_songs(artist_slug):
        lyrics = get_song_lyrics(song_url)
        yield lyrics

def save_artist_lyrics(artist_slug):
    obj = list(get_artist_lyrics(artist_slug))
    with open(f'{artist_slug}.pickle', 'wb') as f:
        pickle.dump(obj, f)

if __name__ == '__main__':
    save_artist_lyrics('jacek_kaczmarski')
    save_artist_lyrics('krzysztof_krawczyk')
