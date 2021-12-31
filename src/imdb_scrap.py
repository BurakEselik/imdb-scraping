from bs4 import BeautifulSoup
import requests
import csv

base_url = 'https://www.imdb.com'
url = '/chart/moviemeter/?ref_=nv_mv_mpm'

def get_url_data(url) -> BeautifulSoup:
    print('Getting data ...')
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup

def parse_data(obj: BeautifulSoup) -> dict:
    print('Parsing data ...')
    movies = {'most_popular_movies':{}}
    tbody = obj.find('tbody', {'class': 'lister-list'})
    trs = tbody.find_all('tr')
    nmr = 0
    for tr in trs:
        nmr += 1    
        movies['most_popular_movies'].update({
            nmr:{
                'MOVIE NAME': tr.find('td', {'class': 'titleColumn'}).a.get_text(),
                'RELEASE DATE': tr.find('td', {'class': 'titleColumn'}).span.get_text().strip('()'),
                'RATE' : tr.find('td', {'class': 'ratingColumn imdbRating'}).get_text().strip(),
                'IMDB LINK' : base_url + tr.find('td', {'class': 'titleColumn'}).a.get('href')
                }
            })
    return movies

def convert_csv(movies: dict):
    to_csv = [i for i in movies['most_popular_movies'].values()]
    keys = to_csv[0].keys()
    with open('most_popular_movies.csv', 'w', newline='') as output_file:
        dict_writher = csv.DictWriter(output_file, keys)
        dict_writher.writeheader()
        dict_writher.writerows(to_csv)

    print('Check the file!')

def main():
    result = get_url_data(base_url + url)
    movies = parse_data(result)
    convert_csv(movies)

if __name__ == '__main__':
    main()