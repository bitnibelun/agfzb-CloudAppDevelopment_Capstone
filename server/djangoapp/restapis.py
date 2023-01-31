import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import requests

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#   auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print("API: ", kwargs)
    print("API: GET from {} ".format(url))

    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
            params=kwargs)
    except:
        # If any error occurs
        print("API: Network exception occurred in: No authentication GET")

    status_code = response.status_code
    print("API: With status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    response = None
    try:
        response = requests.post(url, json = json_payload, params = kwargs)
    except Exception as e:
        print("API: exception when posting request: ", e)

    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter

    results_list = get_request(url)
    if results_list:

        for result in results_list:
            # Get its content in `doc` object
            dealer = result["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"],
                                   city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    review_results = []

    results_list = get_request(url, dealerId=dealer_id)

    if results_list:
        
        for result in results_list:
            # Get its content in `doc` object
            # review = result["doc"]
            dealership = result["dealership"]
            name = result["name"]
            purchase = result["purchase"]
            review_id = result["_id"]
            review_text = result["review"]
            sentiment_wat = analyze_review_sentiments(review_text)

            try:
                purchase_date = result["purchase_date"]
                car_make = result["car_make"]
                car_model = result["car_model"]
                car_year = result["car_year"]
                review_obj = DealerReview(r_id=review_id, dealership=dealership, name=name, purchase=purchase, review=review_text,
                                          purchase_date=purchase_date, car_make=car_make, 
                                          car_model=car_model, car_year=car_year, sentiment=sentiment_wat)
            except KeyError:
                review_obj = DealerReview(r_id=review_id, dealership=dealership, name=name, purchase=purchase, review=review_text,
                                             sentiment=sentiment_wat)
                
            review_results.append(review_obj)

    return review_results

# Get dealer by id
def get_dealer_by_id_from_cf(url, dealer_id):

    dealer = get_request(url, dealerId = dealer_id)

    if dealer:
        dealer_obj = CarDealer(address=dealer[0]["address"],
            city=dealer[0]["city"], full_name=dealer[0]["full_name"],
            id=dealer[0]["id"], lat=dealer[0]["lat"], long=dealer[0]["long"],
            short_name=dealer[0]["short_name"],
            st=dealer[0]["st"], zip=dealer[0]["zip"])

    return dealer_obj


#Get dealers by state
def get_dealers_by_state_from_cf(url, state):
    results = []

    results_list = get_request(url, st = state)
    if results_list:
        for dealer in results_list:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"],
                                   city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
# - Get the returned sentiment label such as Positive or Negative

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e8582871-e597-4d4a-b116-506f8b3ddb95" 
    api_key = "2E7pm6WeSSztuyVKNFj68PPeRlou8-OirKrOgiQNHACp" 

    authenticator = IAMAuthenticator(api_key) 
    nat = NaturalLanguageUnderstandingV1(version = '2021-08-01', authenticator = authenticator) 
    nat.set_service_url(url) 

    try:
        response = nat.analyze(text = dealerreview, 
        features = Features(sentiment = SentimentOptions(targets = [dealerreview]))).get_result() 
        sentiment=json.dumps(response, indent=2) 
        sentiment = response['sentiment']['document']['label'] 

    except ApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
        sentiment = "neutral"

    return sentiment

