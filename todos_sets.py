import requests
import subprocess


def fetch_set_codes():
    url = "https://api.scryfall.com/sets"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [set_data['code'] for set_data in data['data'] if set_data['set_type'] in ['expansion']][::-1]
    else:
        print("Failed to fetch set codes from Scryfall API.")
        return []


def run_traducao_set(set_code):
    subprocess.run(["python", "traducao_set.py"], input=set_code, text=True)


def main():
    set_codes = fetch_set_codes()
    if set_codes:
        for set_code in set_codes:
            run_traducao_set(set_code)
    else:
        print("No set codes fetched. Exiting...")


if __name__ == "__main__":
    main()
