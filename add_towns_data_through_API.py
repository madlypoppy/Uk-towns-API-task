import csv
import requests


def wrangle(input_dict):
    
    print(input_dict)
    country_payload = {"country": input_dict["country"]}
    # Try and get the station ID with a GET
    country_request = requests.get("http://127.0.0.1:5000/country/{}".format(input_dict["country"]))
    # If the get returns 400 (http status code for "not found"). then try to add it with a POST.
    if country_request.status_code == 400:
        country_request = requests.post("http://127.0.0.1:5000/country" , json=country_payload)
    # Add the returned country id to the dictionary so we can add a station.
    input_dict["country_id"] = country_request.text 
    requests.post("http://127.0.0.1:5000/town" , json=input_dict)



with open(r"uk-towns-sample.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for name in reader:
        wrangle(name)