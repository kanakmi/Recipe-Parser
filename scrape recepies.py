import requests
from bs4 import BeautifulSoup

search_url = "https://food.ndtv.com/search/recipes?searchtext="

search_keys = ['adhirasam', 'aloo_gobi', 'aloo_matar', 'aloo_methi', 'aloo_shimla_mirch', 'aloo_tikki', 'anarsa', 'ariselu', 'bandar_laddu', 'basundi', 'bhatura', 'bhindi_masala', 'biryani', 'boondi', 'butter_chicken', 'chak_hao_kheer', 'cham_cham', 'chana_masala', 'chapati', 'chhena_kheeri', 'chicken_razala', 'chicken_tikka', 'chicken_tikka_masala', 'chikki', 'daal_baati_churma', 'daal_puri', 'dal_makhani', 'dal_tadka', 'dharwad_pedha', 'doodhpak', 'double_ka_meetha', 'dum_aloo', 'gajar_ka_halwa', 'gavvalu', 'ghevar', 'gulab_jamun', 'imarti', 'jalebi', 'kachori', 'kadai_paneer', 'kadhi_pakoda', 'kajjikaya', 'kakinada_khaja', 'kalakand', 'karela_bharta', 'kofta', 'kuzhi_paniyaram', 'lassi', 'ledikeni', 'litti_chokha', 'lyangcha', 'maach_jhol', 'makki_di_roti_sarson_da_saag', 'malapua', 'misi_roti', 'misti_doi', 'modak', 'mysore_pak', 'naan', 'navrattan_korma', 'palak_paneer', 'paneer_butter_masala', 'phirni', 'pithe', 'poha', 'poornalu', 'pootharekulu', 'qubani_ka_meetha', 'rabri', 'ras_malai', 'rasgulla', 'sandesh', 'shankarpali', 'sheer_korma', 'sheera', 'shrikhand', 'sohan_halwa', 'sohan_papdi', 'sutar_feni', 'unni_appam']

not_found = []
recipes = []

for search_key in search_keys:
    search_key = search_key.replace("_", "+")

    try:
        search_content = requests.get(search_url + search_key).content

        search_soup = BeautifulSoup(search_content, "html.parser")

        url = search_soup.find("a", {"class": "crd_img"})["href"]

        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        recipe_image = soup.find("img", {"id": "story_image_main"})
        # print(recipe_image["src"])

        cook_time = soup.find_all("span", {"class": "RcpInf_crd_tx2"})

        key_Ingredients = soup.find("p", {"class": "aut_crd-txt"})

        ingredients_list = soup.find_all("li", {"class": "RcpIngd-tp_li"})
        ing = []
        for i in ingredients_list:
            ing.append(i.text)

        procedure = soup.find_all("span", {"class": "RcHTM_li-tx"})
        p = []
        for i in procedure:
            p.append(i.text)

        search_key = search_key.replace("+", " ")
        search_key = search_key.title()
        
        recipe = {'title': search_key, 'url': url, 'image': recipe_image["src"], 'prep_time': cook_time[1].text, 'cook_time': cook_time[2].text, 'serving': cook_time[3].text, 'key_ingredients': key_Ingredients.text.split(', '), 'ingredients': ing, 'procedure': p}

        recipes.append(recipe)

    except:
        not_found.append(search_key)

print(not_found)

import pandas as pd

df = pd.DataFrame(recipes)

print(df.head())

df.to_feather('recipes.feather')