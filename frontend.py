import json
from colorama import Fore, Style
import pandas as pd
from pandas.io.json import json_normalize
import urllib
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from pprint import pprint
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

endpoint = 'https://grup7azsearch.search.windows.net'

index_name = 'margiesidxv5' # w/ suggester
#index_name = 'margiesidxv3' # Polish

suggester_name = 'LocationSuggester'
api_version = '?api-version=2019-05-06'
headers = {
    'Content-Type': 'application/json',
    'api-key': 'D1B2DF3F5AC1482E5557FE00092E2677'
}

@app.route('/', methods=['GET'])
def index():
	return("""
        <head>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
            <script src="https://code.jquery.com/jquery-2.2.4.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
		
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/awesomplete/1.1.5/awesomplete.css" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/awesomplete/1.1.5/awesomplete.js"></script>
        <style>
            body {
                background: url('https://assets.awwwards.com/awards/images/2015/04/pattern.jpg');
            }
            * {
                font-family: serif;
            }
            label {
                font-size: 26px;
            }
        </style>
        
        </head>


        <style>#forkongithub a{background:#000;color:#fff;text-decoration:none;font-family:arial,sans-serif;text-align:center;font-weight:bold;font-size:16px;padding:5px 40px;line-height:2rem;position:relative;transition:0.5s;}#forkongithub a:hover{background:#c11;color:#fff;}#forkongithub a::before,#forkongithub a::after{content:"";width:100%;display:block;position:absolute;top:1px;left:0;height:1px;background:#fff;}#forkongithub a::after{bottom:1px;top:auto;}@media screen and (min-width:800px){#forkongithub{position:fixed;display:block;top:0;right:0;width:200px;overflow:hidden;height:200px;z-index:9999;}#forkongithub a{width:200px;position:absolute;top:60px;right:-60px;transform:rotate(45deg);-webkit-transform:rotate(45deg);-ms-transform:rotate(45deg);-moz-transform:rotate(45deg);-o-transform:rotate(45deg);box-shadow:4px 4px 10px rgba(0,0,0,0.8);}}</style><span id="forkongithub"><a href="https://github.com/codepo8/css-fork-on-github-ribbon">DON'T FORK__ ME ON GitHub</a></span>

        <body style="margin:50px">
        <!-- img src="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Falexmang.ro%2Fwp-content%2Fuploads%2F2014%2F09%2Fazure_search_client_library_logo.png&f=1&nofb=1" width="400" -->
        <img src="https://www.monitis.com/blog/wp-content/uploads/2013/12/altavista.png" style="margin-top: -30px; margin-bottom: -20px">
        <h1>ENTERPRISE SEARCH UI<h1>
		<h3>(build 2.8.9304, Fall 1996 update)</h3>

        <form action="/query" method="post" style="margin: 40px">
            <div class="form-group">
                <label for="query">Query</label><br>
                <input type="query" class="form-control2" name="query" aria-describedby="emailHelp" placeholder="Enter your query" size="70">
            </div>

            <div class="form-group">
                <label for="select">Select</label><br>
                <input type="filter" class="form-control2" name="select" placeholder="Enter your $select" size="70">
            </div>

            <div class="form-group">
                <label for="filter">Filter</label><br>
                <input type="filter" class="form-control2" name="filter" placeholder="Enter your $filter" size="70">
            </div>

            <p>Query type</p>
            <div class="btn-group btn-group-toggle" data-toggle="buttons">
                <label class="btn btn-secondary">
                    <input type="radio" name="full" autocomplete="off" checked>full</label>
                <label class="btn btn-secondary">
                    <input type="radio" name="simple" autocomplete="off">simple</label>
            </div>

            <br><br>
            <button type="submit" class="btn btn-success">I'M FEELING LUCKY</button>
        </form>

        <div style="float:right; padding: 20px; margin-top: -400px">
            <h3>Best viewed with</h3>
            <img src="https://media.giphy.com/media/anjRJ4nv9WJzO/source.gif" width="200">
        </div>

       <script>
            items = ['bananna', 'apple'];
            aw = new Awesomplete(document.querySelector("input[name='query']"),{ list: items });
            $("input[name='query']").on('keypress', function() {            
                fetch('http://localhost:5000/suggest?keystrokes=' + this.value)
                                .then(result => {
                                    result.json().then(res => {
                                        res.value.forEach(element => {
                                            items.push(element['@search.text']);
                                            console.log(items);
                                        });
                                        aw.list = items;
                                        items = [];
                                    });
                                });
                        });
        </script>

        </body>
	""")

@app.route('/suggest', methods=['GET', 'POST'])
def suggest():
    keystrokes = request.args.get('keystrokes')
    print(f'Keystrokes = {keystrokes}')
    # GET https://[service name].search.windows.net/indexes/[index name]/docs/suggest?[query parameters]
    url = f'{endpoint}/indexes/{index_name}/docs/suggest{api_version}&search={keystrokes}&suggesterName={suggester_name}'
    print(url)

    s = requests.Session()
    retries = Retry(total=30, backoff_factor=0.3)
    s.mount('http://', HTTPAdapter(max_retries=retries))
    
    ok = False
    while not ok:
        try:
            response = s.get(url, headers=headers)
            ok = True
        except ConnectionError:
            print(f'{Fore.RED}Network is "SUBOPTIMAL" BECAUSE I CAN NOT SAY S**T IN PRODUCTION CODE. Retrying request...{Style.RESET_ALL}')
            response = s.get(url, headers=headers)

    return jsonify(response.json())

@app.route('/query', methods=['POST'])
def query():
    full = 'on'
    simple = None
    query = urllib.parse.quote(request.form['query'])
    filter = urllib.parse.quote(request.form['filter'])
    select = urllib.parse.quote(request.form['select'])
    try:
        full = urllib.parse.quote(request.form['full'])
    except:
        full = None
    try:
        simple = urllib.parse.quote(request.form['simple'])
    except:
        simple = None

    print(f'{Fore.YELLOW}\nQuery = {query}\n' +
        f'Filter = {filter}\nSelect = {select}{Style.RESET_ALL}')

    searchstring = f'&search={query}&$count=true&searchMode=all'
    
   # $select=top_words&search=top_words:(Buckingham)&$count=true&queryType=full

    hasFilter = False
    hasSelect = False
    queryTyoe = full or simple
    if len(filter) > 1:
        hasFilter = True
    if len(select) > 1:
        hasSelect = True
    
    if full:
        queryType = 'full'
    if simple:
        queryType = 'simple'

    if hasFilter:
        searchstring = f'{searchstring}&$filter={filter}&queryType={queryType}'
    if hasSelect:
        searchstring = f'{searchstring}&$select={select}&queryType={queryType}'
    

    url = f'{endpoint}/indexes/{index_name}/docs{api_version}{searchstring}'
    print(url)

    s = requests.Session()
    retries = Retry(total=30, backoff_factor=0.3)
    s.mount('http://', HTTPAdapter(max_retries=retries))
    
    ok = False
    while not ok:
        try:
            response = s.get(url, headers=headers, json=searchstring)
            ok = True
        except ConnectionError:
            print(f'{Fore.RED}Network is "SUBOPTIMAL" BECAUSE I CAN NOT SAY S**T IN PRODUCTION CODE. Retrying request...{Style.RESET_ALL}')
            response = s.get(url, headers=headers, json=searchstring)

    return jsonify(response.json())

    

if __name__ == '__main__':
    app.run()
