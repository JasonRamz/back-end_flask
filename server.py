from flask import Flask, request, abort
from config import me, db
from mock_data import catalog, coupon_codes
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
def fix_id(record):
    record["_id"] = str(record["_id"])
    return record


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
    cursor = db.products.find({})
    results = []

    for prod in cursor:
        results.append(fix_id(prod))
    return json.dumps(results)
# cursor is the result of the reading of the database
# but is a simpler version of list version of the database


# get /api/products/
# return the products dictionary as json
@app.post("/api/catalog")
def save_products():
    product = request.get_json()

    # save product to DB
    db.products.insert_one(product)

    return json.dumps(fix_id(product))

# create a get /api/report/total
# that sends the total value of your catalog(sum of all prices)


@app.get("/api/report/total")
def get_report_total():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        total += prod["price"]

    result = {
        "report": "total",
        "value": total
    }
    return json.dumps(result)


# get all products for a given category
@app.get("/api/products/<cat>")
def get_by_category(cat):
    # print(request.args)
    cursor = db.products.find({"category": cat})
    results = []
    for prod in cursor:
        fix_id(prod)
        results.append(prod)
    return json.dumps(results)

    # get search <term>


@app.get("/api/products/search/<term>")
def product_search(term):
    results = []
    cursor = db.products.find({"title": {"$regex": term, "$options": "i"}})
    for prod in cursor:
        fix_id(prod)
        results.append(prod)

    return json.dumps(results)


# create an endpoint to get all products with a price
# lower or equal than a given number


@app.get("/api/products/lower/<price>")
def product_lower(price):
    results = []
    real_price = float(price)
    cursor = db.products.find({"price": {"$lte": real_price}})

    for prod in cursor:
        fix_id(prod)
        results.append(prod)
    return json.dumps(results)


# get price greater or equal
@app.get("/api/products/greater/<price>")
def product_greater(price):
    results = []
    real_price = float(price)
    cursor = db.products.find({"price": {"$gte": real_price}})

    for prod in cursor:
        fix_id(prod)
        results.append(prod)
    return json.dumps(results)
#########################
######## Coupons##########
#########################
# /api/coupons


@app.get("/api/coupons")
def get_coupons():
    cursor = db.coupons.find({})
    coupons = []
    for coupon in cursor:
        fix_id(coupon)
        coupons.append(coupon)
    return json.dumps(coupons)


@app.post("/api/coupons")
def save_coupons():
    coupon = request.get_json()
    # save the coupon to the DB
    db.coupons.insert_one(coupon)

    return json.dumps(coupon)

# get /api/coupons/<code>
# coupon can be found if applied well


@app.get("/api/coupons/<code>")
def search_coupon(code):
    for coupon in coupon_codes:
        if coupon["code"].lower() == code.lower():
            return json.dumps(coupon)
    return abort(404, "Coupon not found, PLEASE TRY AGAIN!!")

# get /api/coupons/apply/<code>
# return the discount amount


@app.get("/api/coupons/apply/<code>")
def apply_coupon(code):
    coupon = db.coupons.find_one(
        {"code": {'$regex': f"^{code}$", '$options': "i"}})
    if not coupon:
        return abort(404, "Coupon not found, PLEASE TRY AGAIN!!")

    fix_id(coupon)
    return json.dumps(coupon)
# CRUD
# create read update delete

# app.run(debug=True)
