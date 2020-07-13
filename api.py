import csv
from flask import Flask, jsonify, request
from model import Country, Town, dbconnect
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

#Readme: https://www.w3schools.com/tags/ref_httpmethods.asp


@app.route('/country/<search_term>', methods=['GET'])
def get_country(search_term):
    session = dbconnect()
    try:
        country_instance = session.query(Country).filter(Country.country == search_term).one()
        return jsonify(country_instance.id), 200
    except:
        # print(e)
        return "Country doesn't exist in database", 400

@app.route('/town/<search_term>', methods=['GET'])
def get_town(search_term):
    session = dbconnect()
    try:
        town_instance = session.query(Town).filter(Town.name == search_term).one()
        return jsonify(town_instance.id), 200
    except:
        # print(e)
        return "Town doesn't exist in database", 400

# What the hell does this post endpoint do!!
@app.route('/country', methods=['POST'])
def add_country():
    session = dbconnect()
    request_dict = request.get_json()
    try: # Try to create the country
        country_instance = Country()
        country_instance.country = request_dict["country"]
        session.add(country_instance)
        session.commit()
        return jsonify(country_instance.id)
    except exc.IntegrityError: # If the region doesn't exist - freak out and send back 400.
        session.rollback()
        return "already exists", 400

# What the hell does this post endpoint do!!
@app.route('/town', methods=['POST'])
def add_town():
    session = dbconnect()
    request_dict = request.get_json()
    try: 
        country_instance = session.query(Country).filter(Country.id == request_dict["country_id"]).one()
    except:
        return "Country ID doesn't exist in database", 400

    
    try: # Try to create the town
        town_instance = Town()
        town_instance.name = request_dict["name"]
        town_instance.county = request_dict["county"]
        town_instance.grid_reference = request_dict["grid_reference"]
        town_instance.easting = request_dict["easting"]
        town_instance.northing = request_dict["northing"]
        town_instance.longitude = request_dict["longitude"]
        town_instance.latitude = request_dict["latitude"]
        town_instance.elevation = request_dict["elevation"]
        town_instance.postcode_sector = request_dict["postcode_sector"]
        town_instance.local_government_area = request_dict["local_government_area"]
        town_instance.nuts_region = request_dict["nuts_region"]
        town_instance.town_type = request_dict["town_type"]
        town_instance.country = country_instance
        session.add(town_instance)
        session.commit()
        return jsonify(town_instance.id)
    except exc.IntegrityError: # If the town doesn't exist - freak out and send back 400.
        session.rollback()
        return "already exists", 400
    

if __name__ == '__main__':
    app.run(debug=True)