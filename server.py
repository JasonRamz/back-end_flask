from flask import Flask, request
from config import me
from mock_data import catalog
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
# TODO: create a catalog dictionary


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
def get_catalog():
    return json.dumps(catalog)


# get /api/products/
# return the products dictionary as json
@app.post("/api/catalog")
def save_products():
    product = request.get_json()

    product["_id"] = len(catalog)
    catalog.append(product)

    return json.dumps(product)

# create a get /api/report/total
# that sends the total value of your catalog(sum of all prices)


@app.get("/api/report/total")
def get_report_total():
    total = 0
    for prod in catalog:
        total += prod["price"]
    return json.dumps(total)


# get all products for a given category
@app.get("/api/products/<cat>")
def get_products_by_category(cat):
    # print(request.args)
    results = []
    for prod in catalog:
        if (prod["category"] == cat):
            results.append(prod)
    return json.dumps(results)


app.run(debug=True)
