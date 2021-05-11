import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask_cors import CORS

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
# Base = automap_base()
# reflect the tables
# Base.prepare(engine, reflect=True)

# Save reference to the table
# Passenger = Base.classes.passenger

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
cors = CORS(app)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/products<br/>"
        f"/api/v1.0/dashboard"
    )


@app.route("/api/v1.0/products")
def products():
    all_products = [ {"id": "123456", "name": "Azucar"} ]

    # code to connect to db
    # ...

    # query all products into all_products
    # ...

    # return all_products as json
    return jsonify(all_products)


@app.route("/api/v1.0/dashboard/<product_id>")
def dashboard(product_id):
    print('Product ID:', product_id)
    dashboard = [{ "name": "Carlos"}]

    # code to connect to db
    # ...

    # query to get dashboard data
    # ...

    # return dashboard data as json
    return jsonify(dashboard)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
