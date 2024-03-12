import pandas as pd
from deep_translator import GoogleTranslator
import requests
import csv
from tqdm import tqdm
import webbrowser


def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    elif response.status_code == 404:
        print("Failed to download JSON. Status code: 404")
        raise Exception("JSON download failed due to 404 error")
    else:
        print("Failed to download JSON. Status code:", response.status_code)
        return None


def process_pages(url):
    json_data = download_json(url)
    if json_data:
        if 'object' in json_data and json_data['object'] == 'error':
            print("Error:", json_data["details"])
            return []
        print("JSON downloaded successfully:")
        card_data = []
        for card in json_data["data"]:
            try:
                oracle_texto = card["oracle_text"]
                #print('2'+oracle_texto)
            except KeyError:
                try:
                    oracle_texto = card['card_faces'][0]['oracle_text'] + '\n' + '----' + '\n' + card['card_faces'][1][
                        'oracle_text']
                    #print('1' + oracle_texto)
                except KeyError:
                    oracle_texto = ''
                    print("Oracle not found. This card might be missing image data.")
            card_data.append({
                "num": card.get("collector_number", ""),
                "name": card["name"],
                "oracle_text": oracle_texto
            })
        next_page = json_data.get("next_page")
        if next_page:
            card_data.extend(process_pages(next_page))
        return card_data
    else:
        return []


try:
    set_code = input("Digite o codigo do set desejado:").lower()
    set_url = f"https://api.scryfall.com/sets/{set_code}"
    set_json = download_json(set_url)
    if set_json and 'search_uri' in set_json:
        url = set_json['search_uri']
    else:
        raise Exception("Failed to get search URI from set JSON")

    all_card_data = process_pages(url)

    df1 = pd.DataFrame(all_card_data)

    if not df1.empty:
        df1.index += 1
        df1['oracle_text'] = df1['oracle_text'].fillna(value='DEBUG', inplace=False)

    df1 = df1[~df1['num'].str.contains('z')]

    texts = df1['oracle_text'].tolist()
    translated_texts = []

    MAX_CHAR_LIMIT = 5000

    for text in tqdm(texts, desc="Translating"):
        if isinstance(text, str) and len(text) > MAX_CHAR_LIMIT:
            chunks = [text[i:i + MAX_CHAR_LIMIT] for i in range(0, len(text), MAX_CHAR_LIMIT)]
            translated_texts_chunk = []
            for chunk in chunks:
                translated = GoogleTranslator(source='auto', target='pt').translate(text=chunk)
                translated_texts_chunk.append(translated)
            translated_texts.append(' '.join(translated_texts_chunk))
        else:
            translated = GoogleTranslator(source='auto', target='pt').translate(text=text)
            translated_texts.append(translated)

    df1['traduzido'] = translated_texts

    df1 = (df1.rename(columns={'num': 'numero', 'name': 'nome', 'oracle_text': 'texto_ingles'}))

    df1.to_csv('traducao.csv', index=False)
    #df1.to_json(f'json_{set_code}.json', orient='records')

    with open('traducao.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)

    html_table = '<table class="styled-table">\n'
    for row in rows:
        html_table += '  <tr>\n'
        for cell in row:
            # Replace '\n' with '<br>' in cell content
            cell_content = cell.replace('\n', '<br>')
            html_table += f'    <td>{cell_content}</td>\n'
        html_table += '  </tr>\n'
    html_table += '</table>'

    with open("pagina_set.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Replace placeholders with actual values
    html_content = html_content.format(
        set_code=set_code,
        html_table=html_table
    )

    with open("traducao_set.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    webbrowser.open("traducao_set.html")

except Exception as e:
    print(e)
