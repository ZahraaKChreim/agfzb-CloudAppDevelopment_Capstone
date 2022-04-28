import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, SentimentOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            # Basic authentication GET
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            #print(params)
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    #print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"], short_name=dealer_doc["short_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId, **kwargs):
    # Call get_request with a URL parameter
    dealer_obj = None
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer['doc']
            if dealer_doc["id"] == dealerId:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
    if dealer_obj is not None:
        return dealer_obj 
    else:
        return 'Not Found'

def get_dealer_reviews_from_cf(url, dealer_Id, **kwargs):
    results = []
    json_result = get_request(url, dealerId=dealer_Id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review

            car_make=review_doc["car_make"] if "car_make" in review_doc else ''
            car_model=review_doc["car_model"] if "car_model" in review_doc else ''
            car_year=review_doc["car_year"] if "car_year" in review_doc else ''
            dealership=review_doc["dealership"] if "dealership" in review_doc else ''
            id=review_doc["id"] if "id" in review_doc else ''
            name=review_doc["name"] if "name" in review_doc else ''
            purchase=review_doc["purchase"] if "purchase" in review_doc else ''
            purchase_date=review_doc["purchase_date"] if "purchase_date" in review_doc else ''
            review=review_doc["review"] if "review" in review_doc else ''

            review_obj = DealerReview(car_make=car_make,
                                      car_model=car_model,
                                      car_year=car_year,
                                      dealership=dealership,
                                      id=id,
                                      name=name,
                                      purchase=purchase,
                                      purchase_date=purchase_date,
                                      review=review,
                                      sentiment=analyze_review_sentiments(review_doc["review"]))

            # review_obj = DealerReview(car_make=review_doc["car_make"],
            #                           car_model=review_doc["car_model"],
            #                           car_year=review_doc["car_year"],
            #                           dealership=review_doc["dealership"],
            #                           id=review_doc["id"],
            #                           name=review_doc["name"],
            #                           purchase=review_doc["purchase"],
            #                           purchase_date=review_doc["purchase_date"],
            #                           review=review_doc["review"],
            #                           sentiment=analyze_review_sentiments(review_doc["review"]))
            
            results.append(review_obj)

        return results

def analyze_review_sentiments(text): 

    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/54c28c4e-87e0-438f-8cd3-428a91564a26" 
    api_key = "Gqtihhn17RuCdlLPxfTehrRheLDmMnvJ0daPiZ4t07jd" 
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-27',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( text=text, language='en', features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 

    label=json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label'] 
    print('analyze_review_sentiments', text, '-', label)
    return(label) 

def post_request(url, json_payload, **kwargs):
    requests.post(url, params=kwargs, json=json_payload)
