import requests
import logging
import json

import azure.functions as func
# SAS URL
# https://g7storage.blob.core.windows.net/all-forms?st=2019-10-24T09%3A21%3A08Z&se=2019-10-25T09%3A21%3A08Z&sp=rl&sv=2018-03-28&sr=c&sig=rEwSIlrn0aO2DP0aQ1LQkUpCE74P3Cw1W3BG8TDy7Kk%3D

def main(req: func.HttpRequest) -> func.HttpResponse:
    headers_final = {"Content-type": "application/json"}
    logging.info('Form Recognizer HTTP trigger function processed a request.')

    body = None
    try:
        body = req.get_json()
    except:
        return func.HttpResponse(
             "Unable to json load request body",
             status_code=400
        )

    values = []
    resp = None

    for item in body['values']:
        d = item['data']
        url = d['url']
        sas = d['sas']

        ########### Python Form Recognizer Analyze #############

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
            post_url = base_url + "/models/" + model_id + "/analyze"
            
            r = requests.get(url + sas)
            pdf = None
            if r.status_code == 200:
                pdf = r.content # could be bad

            resp = requests.post(url = post_url, data = pdf , headers = headers)
            logging.info("!!!!!!!!! Response status code: %d" % resp.status_code)    
            logging.info("!!!!!!!!! Response body:\n%s" % resp.json())

            result = {}
            form_resp = resp.json()

            keys = ['Name:', 'Departure Date:', 'Return Date:', 'Destination City:', 'Destination Country:']
 
            keyswithvalues = {}
        
            for page in form_resp['pages']:
                for keyvaluepair in page['keyValuePairs']:
                    key_txt = "".join([x['text'] for x in keyvaluepair['key']])
                    if key_txt in keys:
                        #print('key: %s' % key)
                        vals = [x['text'] for x in keyvaluepair['value']]
                        val_txt = "".join([x['text'] for x in keyvaluepair['value']])
                        #DEBUG print('key: %s' % key_txt, 'value: %s' % " ".join(vals))
                        keyswithvalues.update( {key_txt : val_txt} )
                        #DEBUG print(keyswithvalues)
            
            record_dict = {
                'recordId': item['recordId'],
                'data': {
                    'form_result': keyswithvalues
                }
            }

            values.append(record_dict)
        
        except Exception as e:
            raise(e)

    values_dict = {
        'values': values
    }

    ret = json.dumps(values_dict)

    return func.HttpResponse(ret, headers=headers_final)

    
