import azure.functions as func
import logging
import json
from typing import List

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# class AccessibilityFeature:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
    
#     def __str__(self):
#         return {self.name: self.description}
#     def __repr__(self):
#         return {self.name: self.description}

class Place:
    def __init__(self, id, name, address, city, imageUrl, accessibilityFeatures, phone, description, priciness, rating, numRatings, location, openNow):
        self.id:str = id
        self.name:str = name
        self.description:str = description
        self.address:str = address
        self.city:str = city
        self.location:dict = location
        self.phone:str = phone
        self.imageUrl:str = imageUrl
        self.accessibilityFeatures:List[str] = accessibilityFeatures
        self.priciness:int = priciness
        self.rating:float = rating
        self.numRatings:int = numRatings
        self.openNow:bool = openNow
    
    @classmethod
    def from_json(cls, json_object):
        return cls(id=json_object["place_id"], #
                   name=json_object["name"], #
                   address=json_object["vicinity"],
                   city="TBC",
                   imageUrl="https://lh3.googleusercontent.com/p/AF1QipMd50mfjQzKOgvRvx8Ll0N6RvLnisrU-C108D4F=s1360-w1360-h1020",
                   location=json_object["geometry"]["location"], #
                   accessibilityFeatures=[None],
                   phone="Test",
                   description="TBC",
                   priciness="TEC",
                   rating=json_object["rating"], #
                   numRatings=json_object["user_ratings_total"], #
                   openNow=True)
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def to_dict(self):
        return self.__dict__

# example_place = Place(id= "place001", 
#                       name = "South Australian Museum", 
#                       address="North Terrace", city= "Adelaide",
#                       imageUrl="https://lh3.googleusercontent.com/p/AF1QipMd50mfjQzKOgvRvx8Ll0N6RvLnisrU-C108D4F=s1360-w1360-h1020",
#                       accessibilityFeatures=["Wheelchair-accessible car park","Wheelchair-accessible entrance","Wheelchair-accessible lift", "Wheelchair-accessible toilet"], 
#                       phone="+61882077500", description="The South Australian Museum is a natural history museum and research institution in Adelaide, South Australia, founded in 1856 and owned by the Government of South Australia. It occupies a complex of buildings on North Terrace in the cultural precinct of the Adelaide Parklands.", priciness=0,rating=4.3,
#                       location={"lat":-34.9205,"lng":138.6032}, numRatings= 1000, openNow=True)

def get_sample_data():
    with open("sample_find_places.json", "r") as f:
        data = json.load(f)
    places = []
    for place in data["results"]:
        places.append(Place.from_json(place).to_dict())
    return places

@app.route(route="places", methods=["GET"])
def Places(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')
    
    if query:
        # 1. process query
        # 1.1 Open AI query - get location, interests, etc.

        # 2. Search for places
        # 2.1 Call places API with search parameters
        # 2.2 Get places from API
        # 2.3 Look for places from other data sources?

        # 3. Filter places based on query
        # not sure the best way to do this 

        # 4. Format and return places
        # 4.1 Call place details API for filtered places to get more details
        # 4.2 Format places into places class (needs modification, it's above)
        # 4.3 Return places as JSON
        return_object = {
        "places": get_sample_data()
        }
        return func.HttpResponse(json.dumps(return_object), mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(
             "Please pass a query on the query string or in the request body. Example: govhack-tripplanner.azurewebsites.net/api/places?query='test'",
             status_code=400
        )
    
