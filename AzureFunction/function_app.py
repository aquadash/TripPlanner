import azure.functions as func
import logging
import json
from typing import List

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

class Place:
    def __init__(self, id, name, address, city, imageUrl, accessibilityFeatures, phone, description, priciness):
        self.id:str = id
        self.name:str = name
        self.description:str = description
        self.address:str = address
        self.city:str = city
        self.phone:str = phone
        self.imageUrl:str = imageUrl
        self.accessibilityFeatures:List[str] = accessibilityFeatures
        self.priciness:int = priciness
    
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def to_dict(self):
        return self.__dict__

example_place = Place("place001", 
                      "South Australian Museum", 
                      "North Terrace", "Adelaide",
                      "https://lh3.googleusercontent.com/p/AF1QipMd50mfjQzKOgvRvx8Ll0N6RvLnisrU-C108D4F=s1360-w1360-h1020",
                      ["Wheelchair-accessible car park","Wheelchair-accessible entrance","Wheelchair-accessible lift", "Wheelchair-accessible toilet"], 
                      "+61882077500", "The South Australian Museum is a natural history museum and research institution in Adelaide, South Australia, founded in 1856 and owned by the Government of South Australia. It occupies a complex of buildings on North Terrace in the cultural precinct of the Adelaide Parklands.", 0)

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
    
    return_object = {
        "places": [example_place.to_dict()]
    }

    if query:
        return func.HttpResponse(json.dumps(return_object), mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(
             "Please pass a query on the query string or in the request body. Example: govhack-tripplanner.azurewebsites.net/api/places?query='test'",
             status_code=400
        )
    
