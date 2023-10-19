from flask import Flask
from config import me
import json

app = Flask(__name__)


@app.get('/')
def index():
    return 'Hello World!'


@app.get('/test')
def anything():
    return "this is another page"


#########################
########### API##########
#########################

@app.get("/api/version")
def version():
    v = {
        "version": "1.0.0",
        "name": "Cacahuate"
    }
    return json.dumps(v)


# get /api/about
# return the me dictionary as json
@app.get("/api/about")
def about():
    return json.dumps(me)


# get /api/catalog
# return the catalog dictionary as json
@app.get("/api/catalog")
def catalog():
    return json.dumps(catalog)


# get /api/products/
# return the products dictionary as json
@app.get("/api/products")
def products():
    return json.dumps(products)


app.run(debug=True)
