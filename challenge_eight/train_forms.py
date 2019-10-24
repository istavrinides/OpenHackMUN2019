########### Python Form Recognizer Train #############
from requests import post as http_post

# Endpoint URL
base_url = r"https://group7formrecognizer.cognitiveservices.azure.com" + "/formrecognizer/v1.0-preview/custom"
source = r"https://g7storage.blob.core.windows.net/forms-training?st=2019-10-24T09%3A04%3A27Z&se=2019-10-25T09%3A04%3A27Z&sp=rl&sv=2018-03-28&sr=c&sig=01hRG8dwJ2rEbAGUJ3oL6UdHjfls4K55OHSkOMHjVn4%3D"
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '2a396a382bb64044ba35a80c06f5cc1e',
}
url = base_url + "/train" 
body = {"source": source}
try:
    resp = http_post(url = url, json = body, headers = headers)
    print("Response status code: %d" % resp.status_code)
    print("Response body: %s" % resp.json())
except Exception as e:
    print(str(e))