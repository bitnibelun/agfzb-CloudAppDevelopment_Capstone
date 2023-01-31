import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#   auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key = False, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

    if api_key:
        # Basic authentication GET
        try:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                params=params, auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("Network exception occurred in: Basic authentication GET")
    else:
        # No authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred in: No authentication GET")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    response = None
    try:
        response = requests.post(url, json = payload, params = kwargs)
    except:
        print("exception when posting request")

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
            review = result["doc"]
            dealership = review["dealership"]
            name = review["name"]
            purchase = review["purchase"]
            review_id = review["_id"]
            review_text = review["review"]
            sentiment_wat = analyze_review_sentiments(review_text)

            try:
                purchase_date = review["purchase_date"]
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                review_obj = DealerReview(r_id=review_id, dealership=dealership, name=name, purchase=purchase, review=review_text,
                                          purchase_date=purchase_date, car_make=car_make, 
                                          car_model=car_model, car_year=car_year, sentiment=sentiment_wat)
            except KeyError:
                review_obj = DealerReview(r_id=review_id, dealership=dealership, name=name, purchase=purchase, review=review_text,
                                             sentiment=sentiment_wat)
                
            review_results.append(review_obj)

    return review_results

# Get dealers by id
def get_dealer_by_id_from_cf(url, dealer_id):
    json_result = get_request(url, dealerId = dealer_id)

    if json_result:
        dealer = json_result["entries"][0]
        dealer_obj = CarDealer(address=dealer["address"],
            city=dealer["city"], full_name=dealer["full_name"],
            id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
            short_name=dealer["short_name"],
            st=dealer["st"], zip=dealer["zip"])

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
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
        #In the method, 
        #make a call to the updated get_request(url, **kwargs) 
        #method with following parameters:"
    """
        params = dict()
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
        auth=HTTPBasicAuth('apikey', api_key))
    """
    # try:
    #     if os.environ['env_type'] == 'PRODUCTION':
    #         url = os.environ['COUCH_URL']
    #         api_key = os.environ["IAM_API_KEY"]
    # except:
    #     url = config('COUCH_URL')
    #     api_key = config('IAM_API_KEY')

    # version = '2021-08-01' #5.2.2
    # authenticator = IAMAuthenticator(api_key)
    # nat = NaturalLanguageUnderstandingV1(version = version, authenticator = authenticator)
    # nat.set_service_url(url)

    # try:
    #     response = nat.analyze(text = dealerreview,
    #                            features = Features
    #                            (sentiment = SentimentOptions())).get_result()

    #     sentiment = response["sentiment"]["document"]["label"]
    # except:
    #     sentiment = "neutral"

    # return sentiment
    return "Happy bro___________________fix analyze_review_sentiments________________________________________"
