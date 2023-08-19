import os
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

maps_key = os.getenv("GOOGLE_MAPS_API_KEY")


find_location = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={input}&inputtype=textquery&fields=place_id,name,geometry&key={maps_key}"
search_place_text = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&fields=place_id,name&key={maps_key}"
get_place_details_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={maps_key}"


find_place_nearby = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&types=restaurant&name=harbour&key=AIzaSyBR85dl_oSCesioQp29jOEWJYgDsgNcSOM"

#get_place_photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={maps_key}"

def get_place_details(place_id: str):
    response = requests.get(get_place_details_url.format(place_id=place_id, maps_key=maps_key)).json()
    if response.get("status") == "OK":
        place = response["result"]
        return place

def get_location_from_query(location: str):
    response = requests.get(find_location.format(input=location, maps_key=maps_key)).json()
    if response.get("status") == "OK":
        location = response["candidates"][0]["geometry"]["location"]
        return location
    else:
        return None

def get_places_from_query(query: str, location: Optional[dict]):
    if location:
        query += f"&location={location['lat']}%{location['lng']}"
    response = requests.get(search_place_text.format(input=query, maps_key=maps_key)).json()
    if response.get("status") == "OK":
        places = response["results"]
    return [place["place_id"] for place in places if place['rating'] > 3.0] # hardcoded rating limit lol
