import sys
import requests
from bs4 import BeautifulSoup


def fetch_map_info(map_name):
    url = "https://urtjumpmaps.com/maplist/"

    # Modifier l'URL pour afficher toutes les maps

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    map_entries = soup.find_all('tr')[1:]

    found = False

    for entry in map_entries:
        cells = entry.find_all('td')

        name_link = cells[2].find('a', href=True, onpointerenter=True)
        name = name_link.get_text(strip=True)

        id_attr = name_link.find('img', id=True).get('id')
        reel_name = id_attr if id_attr.startswith('ut') else ""

        if reel_name.lower() == map_name.lower():
            found = True

            mapper_links = cells[3].find_all('a', href=True)
            mapper_names = [link.get_text(strip=True) for link in mapper_links]

            level = cells[4].get_text(strip=True)

            type_link = cells[5].find('a', href=True)
            map_type = type_link.get_text(strip=True) if type_link else "None"

            
            print("^2Name:^7", reel_name)
            print("^2Mapper:^7", ', '.join(mapper_names))
            print("^2Level:^7", level)
            print("^2Type:^7", map_type)
            break

    if not found:
        print("Map '{}' not found.".format(map_name))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: !mapinfo or !mapinfo <mapname>")
        sys.exit(1)

    reel_map_name = sys.argv[1]
    fetch_map_info(reel_map_name)
