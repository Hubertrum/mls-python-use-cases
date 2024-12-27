import csv
import requests
import json

def get_url_data(url: str) -> list:

    response = requests.get(url, stream=True)

    return response.json()


def save_as_csv(countries_list: list) -> None:

    # Specify the file name
    filename = "countries_ccn3.csv"

    countries = []

    for country in countries_list:
        Row = {}
        Row["country"] = country["name"]["official"]
        Row["ccn3"] = country["ccn3"]
        countries.append(Row)

    # Get the keys from the first dictionary as the header
    header = countries[0].keys()

    # Write to CSV file
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        
        # Write the header
        writer.writeheader()
        
        # Write the data
        writer.writerows(countries)

    print(f"Country data has been written to {filename}")


def run_all() -> None:

    countries_list = get_url_data("https://restcountries.com/v3.1/all?fields=name,ccn3") 

    save_as_csv(countries_list)

if __name__ == "__main__":

    run_all()