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
        print("Error:", error_data["details"])
        return None
    else:
        print("Failed to download JSON. Status code:", response.status_code)
        return None


def descapitalize_and_replace(text):
    return text.lower().replace(" ", "+").replace("'", "")


original_text = input("Digite a carta desejada: ")
nome = descapitalize_and_replace(original_text)

url = f"https://api.scryfall.com/cards/named?fuzzy={nome}"
print(url)

data = download_json(url)
normal_image_url2 = '0'

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
            print("Image URI not found. This card might be missing image data.")

    try:
        oracle_texto = data["oracle_text"]
    except KeyError:
        try:
            oracle_texto = data['card_faces'][0]['oracle_text']
            oracle_texto = oracle_texto + '\n' + '----' + '\n' + data['card_faces'][1]['oracle_text']
        except KeyError:
            oracle_texto = ''
            print("Oracle not found. This card might be missing image data.")

    try:
        flavor_original = data["flavor_text"]
    except KeyError:
        try:
            flavor_original = data['card_faces'][0]['flavor_text']
        except KeyError:
            flavor_original = ''
            print("Flavour Text not found. This card might be missing image data.")

    translated = GoogleTranslator(source='auto', target='pt').translate(text=oracle_texto)
    flavor_translated = GoogleTranslator(source='auto', target='pt').translate(text=flavor_original)
    replace_newline_with_br = lambda text: text.replace("\n", "<br>")

    oracle_texto = replace_newline_with_br(oracle_texto)
    translated = replace_newline_with_br(translated)

    # Writing HTML content to a file
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{original_text}</title>
        <style>
            body {{
                background-color: #f4f4f4; 
            }}
    
            .container {{
                display: flex;
                align-items: center;
                border: 1px solid #ddd; 
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); 
                padding: 20px;
                margin: 20px;
                background-color: #fff; 
                color: #333; 
                transition: box-shadow 0.3s; 
            }}
    
            .container:hover {{
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            }}
    
            .text-container {{
                margin-left: 20px;
            }}
    
            .text-container h2 {{
                margin-top: 0;
                color: #555;
                font-family: Arial, sans-serif; 
            }}
    
            .text-container p {{
                font-family: Arial, sans-serif;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="container">
                <img src="{normal_image_url}" alt="Card Image">
                <img src="{normal_image_url2}" alt="">
            </div>
            <div class="text-container">
                <h2>Texto em inglês:</h2>
                <p>{oracle_texto}</p>
                <p style="font-style: italic;">{flavor_original}</p>
    
                <h2>Tradução:</h2>
                <p>{translated}</p>
                <p style="font-style: italic;">{flavor_translated}</p>
    
            </div>
        </div>
    </body>
    </html>
    """

    # Writing HTML content to a file named 'output.html'
    with open("traducao_carta.html", "w") as file:
        file.write(html_content)

    # Automatically open the HTML file in the default web browser
    webbrowser.open("traducao_carta.html")

    print("HTML file generated successfully and opened in the default web browser!")
else:
    print("No data retrieved from the API. Please check the input and try again.")
