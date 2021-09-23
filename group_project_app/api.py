from urllib.parse import urlparse, urlencode, parse_qsl
from django.conf import settings
import requests, os, pandas
from dotenv import load_dotenv
load_dotenv()

#Google Maps Client API
GOOGLE_API_KEY = str(os.getenv('GOOGLE_API_KEY'))
class GoogleMapsClient(object):
    lat=None
    lng=None
    data_type='json'
    location_query=None
    api_key= GOOGLE_API_KEY
    
    def __init__(self, api_key=str(os.getenv('GOOGLE_API_KEY')), address_or_postal_code= None, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if api_key == None:
            raise Exception('Api key is requried!')
        self.api_key= api_key
        self.location_query= address_or_postal_code
        if self.location_query != None:
            self.extract_cords()
        
    def extract_cords(self, location=None):
        loc_query=self.location_query
        if location != None:
            loc_query=location
        endpoint=f"https://maps.googleapis.com/maps/api/geocode/{self.data_type}"
        params={"address":loc_query, "key": self.api_key}
        url_params=urlencode(params)
        url=f"{endpoint}?{url_params}"
        r= requests.get(url)
        if r.status_code not in range(200, 299):
            return {}
        latlng={}
        try:
            latlng= r.json()['results'][0]['geometry']['location']
        except:
            pass
        lat, lng=latlng.get('lat'), latlng.get('lng')
        self.lat=lat
        self.lng=lng
        return lat, lng
    def search(self, keyword="Bars", radius=8100, location=None):
        lat, lng= self.lat, self.lng
        if location != None:
            lat, lng= self.extract_cords(location)
        endpoint= f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
        params={
            'key': self.api_key,
            'location':f"{lat},{lng}",
            'radius':radius,
            'keyword': keyword
        }

        params_encoded=urlencode(params)
        places_url=f"{endpoint}?{params_encoded}"
        r=requests.get(places_url)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def detail(self, place_id=None, fields=['name','rating','formatted_phone_number','formatted_address']):
        detail_base_endpoint = f'https://maps.googleapis.com/maps/api/place/details/{self.data_type}'
        detail_params={
            'place_id':f"{place_id}",
            'fields':','.join(fields),
            'key':self.api_key
        }
        detail_params_encoded=urlencode(detail_params)
        details_url =f"{detail_base_endpoint}?{detail_params_encoded}"
        r=requests.get(details_url)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()


