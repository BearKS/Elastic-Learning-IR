from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import os
app = Flask(__name__)
es = Elasticsearch('localhost', port=9200)

picFolder = os.path.join('static','img')
app.config['UPLOAD_FOLDER'] = picFolder
 
@app.route('/')
def home():
    GooseGoose = os.path.join(app.config['UPLOAD_FOLDER'], 'GooseGoose.png')
    return render_template('search.html', user_image = GooseGoose)

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index="covid-19", 
        size=20, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "link", 
                        "text", 
                        "title"
                    ] 
                }
            }
        }
    )
    return render_template('results.html', res=res )

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='localhost', port=5000)