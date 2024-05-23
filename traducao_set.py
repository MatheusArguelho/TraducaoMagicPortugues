import pandas as pd
from deep_translator import GoogleTranslator
import requests
import csv
from tqdm import tqdm
import webbrowser
import os
from dicionario import translation_dict


def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise Exception("JSON download failed due to 404 error")
    else:
        raise Exception(f"JSON download failed with status code: {response.status_code}")


def process_card_data(card):
    try:
        oracle_texto = card["oracle_text"]
    except KeyError:
        try:
            oracle_texto = card['card_faces'][0]['oracle_text'] + '\n' + '----' + '\n' + card['card_faces'][1][
                'oracle_text']
        except KeyError:
            oracle_texto = ''
    return {
        "num": card.get("collector_number", ""),
        "name": card["name"],
        "oracle_text": oracle_texto
    }


def filter_card_data(df):
    df = df[~df['num'].str.contains('z')]
    names_to_drop = ['Plains', 'Swamp', 'Island', 'Mountain', 'Forest']
    return df[~df['name'].isin(names_to_drop)]


def translate_and_format_text(text, translation_dict):
    for term, translation in translation_dict.items():
        text = text.replace(term, translation)
    text = GoogleTranslator(source='auto', target='pt').translate(text=text)
    return text.replace('\n', '<br>')


def translate_card_texts(texts, set_code, translation_dict):
    translated_texts = []
    max_char_limit = 5000
    for text in tqdm(texts, desc=f"Translating {set_code}"):
        # Aplica a tradução e formatação individual primeiro
        formatted_text = translate_and_format_text(text, translation_dict)

        if isinstance(formatted_text, str) and len(formatted_text) > max_char_limit:
            chunks = [formatted_text[i:i + max_char_limit] for i in range(0, len(formatted_text), max_char_limit)]
            translated_texts_chunk = []
            for chunk in chunks:
                translated = GoogleTranslator(source='auto', target='pt').translate(text=chunk)
                translated_texts_chunk.append(translated)
            translated_texts.append(' '.join(translated_texts_chunk))
        else:
            translated = GoogleTranslator(source='auto', target='pt').translate(text=formatted_text)
            translated_texts.append(translated)
    return translated_texts


def save_csv_file(df, file_path):
    df.to_csv(file_path, index=False, encoding='utf-8')


def create_html_table(rows):
    html_table = '<table class="styled-table">\n'
    for row in rows:
        html_table += '  <tr>\n'
        for cell in row:
            # Replace '\n' with '<br>' in cell content
            cell_content = cell.replace('\n', '<br>')
            html_table += f'    <td>{cell_content}</td>\n'
        html_table += '  </tr>\n'
    html_table += '</table>'
    return html_table


def read_html_template(template_path):
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()


def fill_html_template(template_content, set_code, html_table):
    return template_content.format(set_code=set_code, html_table=html_table)


def save_html_file(html_content, file_path):
    with open(file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)


def open_html_file(html_file_path):
    webbrowser.open(html_file_path)


def func_traducao():
    try:
        set_code = input("Digite o codigo do set desejado:").lower()
        folder_name = "Sets"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        html_file_path = os.path.join(folder_name, f"set_{set_code}.html")

        # Check if the HTML file already exists
        if os.path.exists(html_file_path):
            print(f"O arquivo {html_file_path} já existe. Abrindo o arquivo...")
            # open_html_file(html_file_path)
            return

        set_url = f"https://api.scryfall.com/sets/{set_code}"
        set_json = download_json(set_url)
        if set_json and 'search_uri' in set_json:
            url = set_json['search_uri']
        else:
            raise Exception("Falha ao obter o URL de pesquisa do conjunto JSON")

        all_card_data = []
        while url:
            json_data = download_json(url)
            all_card_data.extend([process_card_data(card) for card in json_data["data"]])
            url = json_data.get("next_page")

        df = pd.DataFrame(all_card_data)

        if not df.empty:
            df.index += 1
            df['oracle_text'] = df['oracle_text'].fillna(value='DEBUG', inplace=False)

        df = filter_card_data(df)

        translated_texts = translate_card_texts(df['oracle_text'].tolist(), set_code, translation_dict)

        df['traduzido'] = translated_texts

        df = df.rename(columns={'num': 'numero', 'name': 'nome', 'oracle_text': 'texto_ingles'})

        save_csv_file(df, 'traducao.csv')

        with open('traducao.csv', 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            rows = list(csvreader)

        html_table = create_html_table(rows)

        html_template = read_html_template("pagina_set.html")

        html_content = fill_html_template(html_template, set_code, html_table)

        save_html_file(html_content, html_file_path)

        # open_html_file(html_file_path)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    func_traducao()
