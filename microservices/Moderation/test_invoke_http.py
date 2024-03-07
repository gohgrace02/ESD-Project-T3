# # test_invoke_http.py
# from invokes import invoke_http
import requests

# # invoke book microservice to get all books
# results = invoke_http("http://api1-ap.webpurify.com/services/rest//?method=webpurify.live.check&api_key=c4eb16473bd9be59faee65a329fdad48&text='string'", method='GET')

# print( type(results) )
# print()
# print( results )

comment = "fuck fuck"
url = f"http://api1-ap.webpurify.com/services/rest//?method=webpurify.live.check&api_key=c4eb16473bd9be59faee65a329fdad48&text={comment}&format=json"  # Replace with the actual API endpoint URL

try:
    response = requests.get(url)

    # Access the response content (replace with actual data parsing)
    data = response.json()
    print(data)
    print(data["rsp"]["found"])
    print(type(data["rsp"]["found"]))

except requests.exceptions.RequestException as e:
    print(f"Error calling API: {e}")

