import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask_cors import CORS

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite 
connection_string = "root:root@172.20.0.3:5432/custom_analysis_db"
engine = create_engine(f'postgresql://{connection_string}')
conn = engine.connect()

# reflect an existing database into a new model
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
# Print all of the classes mapped to the Base
Base.classes.keys()

# Save references to each table
Importer = Base.classes.importer
Ports = Base.classes.ports
Transaction = Base.classes.transaction
Product = Base.classes.product

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/importers<br/>"
        f"/api/v1.0/importers/&lt;importer_id&gt;<br/>"
        f"/api/v1.0/dashboard/&lt;product_id&gt;"
    )


@app.route("/api/v1.0/products")
def products():
    all_products = []

    for row in session.query(Product).all():
        product = {
            "hts_code": row.hts_code,
            "hts_code_description": row.hts_code_description,
            "commercial_description": row.commercial_description,
            "description": row.description,
            "description1": row.description1,
            "description2": row.description2,
            "description3": row.description3,
            "description4": row.description4,
            "description5": row.description5,
        }
        all_products.append(product)

    return jsonify({ "products": all_products })

@app.route("/api/v1.0/importers")
def importers():
    all_importers = []

    for row in session.query(Importer).all():
        importer = {
            "tax_id": row.tax_id,
            "name": row.name.strip(),
        }
        all_importers.append(importer)

    return jsonify({ "importers": all_importers })


@app.route("/api/v1.0/importers/<importer_id>")
def importer(importer_id):
    record = session.query(
        Importer
    ).filter(
        Importer.tax_id == importer_id,
    ).one()

    importer = {
        "tax_id": record.tax_id,
        "name": record.name.strip(),
    }

    return jsonify(importer)


@app.route("/api/v1.0/dashboard/<product_id>")
def dashboard(product_id):
    print('Product ID:', product_id)
    dashboard = {}

    # get aggregates
    record = session.query(
        func.sum(Transaction.net_kg),
        func.sum(Transaction.usd_fob_total),
        func.avg(Transaction.net_kg),
        func.avg(Transaction.usd_fob_total),
    ).filter(
        Transaction.hts_code == product_id,
    ).one()
    dashboard['aggregates'] = {
        'net_kg_sum': float(record[0]),
        'usd_fob_total_sum': float(record[1]),
        'net_kg_avg': float(record[2]),
        'usd_fob_total_avg': float(record[3]),
    }

    # get top importers by net_kg
    records = session.query(
        Transaction.importer_name,
        func.sum(Transaction.net_kg),
    ).filter(
        Transaction.hts_code == product_id,
    ).group_by(
        Transaction.importer_name
    ).order_by(
        desc(func.sum(Transaction.net_kg))
    ).limit(5).all()

    dashboard['top_importers_by_net_kg'] = []
    for row in records:
        data = {
            "importer": row[0],
            "value": row[1],
        }
        dashboard['top_importers_by_net_kg'].append(data)


    # get top importers by usd_fob_total
    records = session.query(
        Transaction.importer_name,
        func.sum(Transaction.usd_fob_total),
    ).filter(
        Transaction.hts_code == product_id,
    ).group_by(
        Transaction.importer_name
    ).order_by(
        desc(func.sum(Transaction.usd_fob_total))
    ).limit(5).all()

    dashboard['top_importers_by_usd_fob_total'] = []
    for row in records:
        data = {
            "importer": row[0],
            "value": row[1],
        }
        dashboard['top_importers_by_usd_fob_total'].append(data)


    # get top country_of_origins by net_kg
    records = session.query(
        Transaction.country_of_origin,
        func.sum(Transaction.net_kg),
    ).filter(
        Transaction.hts_code == product_id,
    ).group_by(
        Transaction.country_of_origin
    ).order_by(
        desc(func.sum(Transaction.net_kg))
    ).limit(5).all()

    dashboard['top_country_of_origins_by_net_kg'] = []
    for row in records:
        data = {
            "country_of_origin": row[0],
            "value": row[1],
        }
        dashboard['top_country_of_origins_by_net_kg'].append(data)


    # get top country_of_origins by usd_fob_total
    records = session.query(
        Transaction.country_of_origin,
        func.sum(Transaction.usd_fob_total),
    ).filter(
        Transaction.hts_code == product_id,
    ).group_by(
        Transaction.country_of_origin
    ).order_by(
        desc(func.sum(Transaction.usd_fob_total))
    ).limit(5).all()

    dashboard['top_country_of_origins_by_usd_fob_total'] = []
    for row in records:
        data = {
            "country_of_origin": row[0],
            "value": row[1],
        }
        dashboard['top_country_of_origins_by_usd_fob_total'].append(data)


    # return dashboard data as json
    return jsonify(dashboard)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
