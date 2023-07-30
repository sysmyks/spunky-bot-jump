import sys
import os
import zipfile
import re
import json

# --------------------------------------------#
# --------here put your path of maps----------#
# --------------------------------------------#
path_map_depo = 'C:\\Users\\gehuts\\Desktop\\urt+serv\\q3ut4\\'


def create_empty_map_info_file():
    if not os.path.exists("map_info.json"):
        with open("map_info.json", "w") as file:
            json.dump({}, file)


def filter(path_map_depo, mapname):
    zip_file_path = path_map_depo + mapname + ".pk3"
    print(zip_file_path)

    if not os.path.exists(zip_file_path):
        print("Le fichier ZIP n'existe pas.")
        sys.exit(1)

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            print("Fichier ZIP trouvé")
            bsp_file_name = "maps/" + mapname + ".bsp"

            if bsp_file_name in zip_file.namelist():
                print("Fichier BSP trouvé")

                with zip_file.open(bsp_file_name, 'r') as bsp_file:
                    print("Lecture du fichier BSP")
                    bsp_content = bsp_file.read()

                    info = set()
                    pattern = rb'\{[^{}]*"classname"[^{}]*\}'
                    matches = re.findall(pattern, bsp_content)
                    for match in matches:
                        match_str = match.decode('utf-8')

                        info.add(match_str)

                    bsp_info = list(info)
                    return bsp_info
            else:
                print("Le fichier BSP n'a pas été trouvé dans l'archive ZIP.")
    except zipfile.BadZipFile:
        print("Erreur : Le fichier n'est pas au format ZIP valide.")
    except Exception as e:
        print("Une erreur est survenue :", str(e))


def parser_jumpstop(bsp_info):
    try:
        bsp_info = ' '.join(bsp_info)
        unique_names = set()
        jumpstops = []
        blocks = re.findall(r'{[^}]*}', bsp_info)

        for block in blocks:
            if 'classname' in block and ('"ut_jumpstart"' in block or '"ut_jumpstop"' in block):
                type_match = re.search(r'"type" "(.*?)"', block)
                if type_match:
                    current_type = int(type_match.group(1))
                else:
                    current_type = None

                name_match = re.search(r'"name" "(.*?)"', block)
                if name_match:
                    current_name = name_match.group(1)
                else:
                    current_name = None

                if current_name is not None and current_type is not None:

                    if current_name not in unique_names:
                        jumpstops.append(
                            {"name": current_name, "type": current_type})
                        unique_names.add(current_name)

        if not jumpstops:
            name_matches = re.findall(r'"name" "(.*?)"', bsp_info)
            for name in name_matches:

                if name not in unique_names:
                    jumpstops.append({"name": name, "type": 1})
                    unique_names.add(name)

        return jumpstops

    except Exception as e:
        print("Une erreur est survenue :", str(e))
        return None


def parser_location(bsp_info):
    try:
        bsp_info_str = ' '.join(bsp_info)
        pattern = r'"message" "(.*?)"'
        matches = re.findall(pattern, bsp_info_str)
        unique_messages = list(set(matches))
        return unique_messages

    except Exception as e:
        print("Une erreur est survenue :", str(e))
        return None


def save_map_info(mapname, way, loc):
    try:
        map_info = {}
        if os.path.exists("map_info.json") and os.path.getsize("map_info.json") > 0:
            with open("map_info.json", "r", encoding="utf-8") as file:
                map_info = json.load(file)

        if mapname in map_info:
            print(
                f"Les informations pour la carte {mapname} sont déjà enregistrées.")
            return

        map_info[mapname] = {
            "way": way,
            "loc": loc
        }

        with open("map_info.json", "w", encoding="utf-8") as file:
            json.dump(map_info, file, indent=4, ensure_ascii=False)

        print(
            f"Informations pour la carte {mapname} enregistrées avec succès.")

    except Exception as e:
        print("Une erreur est survenue lors de l'enregistrement :", str(e))


# --------------------------------------------#
# ------------------main----------------------#
# --------------------------------------------#

create_empty_map_info_file()
mapname = ' '.join(sys.argv[1:])
bsp_info = filter(path_map_depo, mapname)
way = parser_jumpstop(bsp_info)
loc = parser_location(bsp_info)

if way is not None:
    print("Way :")
    print(way)

if loc is not None:
    print("Location :")
    print(loc)

save_map_info(mapname, way, loc)
