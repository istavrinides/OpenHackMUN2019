########### Python Form Recognizer Analyze #############
from requests import post as http_post

# Endpoint URL
base_url = r"https://group7formrecognizer.cognitiveservices.azure.com" + "/formrecognizer/v1.0-preview/custom"
file_path = "/mnt/c/Users/erbaumer/Downloads/Insurance Form 06.pdf"
model_id = "3a874606-1491-44b3-9809-d23317f20f60"
headers = {
    # Request headers
    'Content-Type': 'application/pdf',
    'Ocp-Apim-Subscription-Key': '2a396a382bb64044ba35a80c06f5cc1e',
}

try:
    url = base_url + "/models/" + model_id + "/analyze" 
    with open(file_path, "rb") as f:
        data_bytes = f.read()  
    resp = http_post(url = url, data = data_bytes, headers = headers)
    print("Response status code: %d" % resp.status_code)    
    print("Response body:\n%s" % resp.json())   
except Exception as e:
    print(str(e))