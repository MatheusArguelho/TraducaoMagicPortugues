import webbrowser
import requests
from deep_translator import GoogleTranslator


def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    elif response.status_code == 404:
        error_data = response.json()
        error_t = error_data["details"]
        error_t = GoogleTranslator(source='auto', target='pt').translate(text=error_t)
        print("Error:", error_t)
        return None
    else:
        print("Falha ao baixar JSON. Código de status:", response.status_code)
        return None


def descapitalize_and_replace(text):
    return text.lower().replace(" ", "+").replace("'", "")


original_text = input("Digite a carta desejada: ")
nome = descapitalize_and_replace(original_text)

url = f"https://api.scryfall.com/cards/named?fuzzy={nome}"

print(url)

data = download_json(url)
normal_image_url2 = '0'
flavor_original = ''
flavor_original2 = ''

if data is not None:
    name = data["name"]
    try:
        normal_image_url = data["image_uris"]["normal"]
    except KeyError:
        try:
            normal_image_url = data['card_faces'][0]['image_uris']['normal']
            normal_image_url2 = data['card_faces'][1]['image_uris']['normal']
        except KeyError:
            normal_image_url = None
            print("Image não encontrada")

    try:
        oracle_texto = data["oracle_text"]
    except KeyError:
        try:
            oracle_texto = data['card_faces'][0]['oracle_text']
            oracle_texto = oracle_texto + '\n' + '----' + '\n' + data['card_faces'][1]['oracle_text']
        except KeyError:
            oracle_texto = ''
            print("Oracle não encontrado.")

    try:
        flavor_original = data["flavor_text"]
    except KeyError:
        try:
            if 'card_faces' in data:
                if isinstance(data['card_faces'], list) and len(data['card_faces']) > 0:
                    if 'flavor_text' in data['card_faces'][0]:
                        flavor_original = data['card_faces'][0]['flavor_text']
                    else:
                        flavor_original = ''
                        if len(data['card_faces']) > 1 and 'flavor_text' in data['card_faces'][1]:
                            flavor_original2 = data['card_faces'][1]['flavor_text']
                        else:
                            flavor_original2 = ''
                flavor_original = flavor_original + '\n' + '-' + '\n' + flavor_original2
        except KeyError:
            flavor_original = ''
            print("Flavour Text não encontrado.")

    translated = GoogleTranslator(source='auto', target='pt').translate(text=oracle_texto)
    flavor_translated = GoogleTranslator(source='auto', target='pt').translate(text=flavor_original)
    replace_newline_with_br = lambda text: text.replace("\n", "<br>")

    oracle_texto = replace_newline_with_br(oracle_texto)
    translated = replace_newline_with_br(translated)

    # Read the content of the HTML file
    with open("pagina_individual.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    html_content = html_content.format(
        original_text=original_text,
        normal_image_url=normal_image_url,
        normal_image_url2=normal_image_url2,
        oracle_texto=oracle_texto,
        flavor_original=flavor_original,
        translated=translated,
        flavor_translated=flavor_translated
    )

    with open("traducao_carta.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    webbrowser.open("traducao_carta.html")

    print("Arquivo HTML gerado com sucesso e aberto no navegador padrão!")
else:
    print("Nenhum dado recuperado da API. Verifique o nome da carta e tente novamente.")
