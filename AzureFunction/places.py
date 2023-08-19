import os
import requests
import json
from dotenv import load_dotenv
from typing import Optional, List, Union

load_dotenv()

maps_key = os.getenv("GOOGLE_MAPS_API_KEY")

fields_places = "business_status,place_id,name,formatted_address,editorial_summary,formatted_phone_number,geometry,photos,price_level,rating,types,website,wheelchair_accessible_entrance,user_ratings_total,opening_hours"

find_location = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={input}&inputtype=textquery&fields=place_id,name,geometry&key={maps_key}"
search_place_text = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={maps_key}"
get_place_details_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={maps_key}"


find_place_nearby = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&types=restaurant&name=harbour&key=AIzaSyBR85dl_oSCesioQp29jOEWJYgDsgNcSOM"


class Place:
    def __init__(self, id, name, description, address, location, imageReference, phone, wheelchair_accessible_entrance, priciness, rating, numRatings, openNow,status,website,types):
        self.id:str = id
        self.name:str = name
        self.description:str = description
        self.address:str = address
        self.location:dict = location
        self.phone:str = phone
        self.imageReference:str = imageReference
        self.wheelchair_accessible_entrance:List[str] = wheelchair_accessible_entrance
        self.priciness:int = priciness
        self.rating:float = rating
        self.numRatings:int = numRatings
        self.openNow:bool = openNow
        self.status:str = status
        self.website:str = website
        self.types:List[str] = types
    
    @classmethod
    def from_json(cls, place_result: dict):
        return cls(id=place_result.get("place_id", None),
                 name = place_result.get("name", None),
                 description=place_result.get("editorial_summary",{}).get('overview',None),
                 address=place_result.get("formatted_address"),
                 location=place_result.get("geometry",{}).get("location",{}),
                 imageReference=place_result.get("photos",[{}])[0].get("photo_reference",None),
                 phone=place_result.get("formatted_phone_number",None),
                 wheelchair_accessible_entrance=place_result.get("wheelchair_accessible_entrance",None),
                 priciness=place_result.get("price_level",None),
                 rating=place_result.get("rating",None),
                 numRatings=place_result.get("user_ratings_total",None),
                 openNow=place_result.get("opening_hours",{}).get("open_now",None),
                 status=place_result.get("business_status",None),
                 website=place_result.get("website",None),
                 types=place_result.get("types",None))
    
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def to_dict(self):
        return self.__dict__
    

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

def get_place_object(place_result: tuple):
    place_id = place_result[0]
    place_name = place_result[1]
    result = requests.get(get_place_details_url.format(place_id=place_id, fields=fields_places, maps_key=maps_key)).json()
    if result.get("status") == "OK":
        place_result = result["result"]
        assert place_result["place_id"] == place_id
    return Place.from_json(place_result)


def get_places_from_query(query: Union[str, List[str]], location: Optional[dict]):
    if isinstance(query, list):
        query = "+".join(query)
    if location:
        query += f"&location={location['lat']}%2C{location['lng']}"
    #return query
    response = requests.get(search_place_text.format(query=query, 
                                                     maps_key=maps_key,)
                                                     ).json()
    if response.get("status") == "OK":
        places = response["results"]
    return [(place['place_id'],place['name']) for place in places if place['rating'] > 3.0] # hardcoded rating limit lol (place["place_id"], place['name'])
