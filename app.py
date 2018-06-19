# import necessary libraries

import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc

from flask import Flask, jsonify, render_template

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///db/wine.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

Wine = Base.classes.wine
Coordinate = Base.classes.coordinate


session = Session(engine)

#################################################
# Routes
#################################################

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/variety')
def varieties():

    stmt = session.query(Wine).statement
    wine_df = pd.read_sql_query(stmt, session.bind)
    wine_unique = wine_df.variety.unique()
    
    cleanedList = [x for x in wine_unique if str(x) != 'None']
    return jsonify(cleanedList)
    
@app.route('/country')
def counts():

    stmt = session.query(Wine).statement
    con_df = pd.read_sql_query(stmt, session.bind)
    con_unique = con_df.country.unique()
    
    con_cleanedList = [x for x in con_unique if str(x) != 'None']
    return jsonify(con_cleanedList)

@app.route("/varieties/<variety>")
@app.route("/varieties/<variety>/<country>")
def varcon(variety=None, country=None):
    

    # Select statement
    sel = [Wine.title, Wine.price, Wine.country, Wine.winery]

    if not country:
        # Get top 10 wine variety based on variety
        results = session.query(*sel).\
            filter(Wine.variety == variety).order_by(desc(Wine.points)).limit(10)
        
        wine_data = []
        for result in results:
            cur_dic = {}
            cur_dic["Title"] = result[0]
            cur_dic["Price"] = result[1]
            cur_dic["Country"] = result[2]
            cur_dic["Winery"] = result[3]
            wine_data.append(cur_dic)
            
        return jsonify(wine_data)

    # Get top 10 wine variety based on variety and country
    results = session.query(*sel).\
        filter(Wine.variety == variety).\
        filter(Wine.country == country).order_by(desc(Wine.points)).limit(10)
    
    wine_data = []
    for result in results:
        cur_dic = {}
        cur_dic["Title"] = result[0]
        cur_dic["Price"] = result[1]
        cur_dic["Winery"] = result[3]
        wine_data.append(cur_dic)
            
    return jsonify(wine_data)
    
@app.route('/wine/<variety>')
@app.route('/wine/<variety>/<country>')
def winevarcon(variety=None, country=None):
  
    if not country:
    # Select statement
        sel = [Wine.country, Wine.points, Wine.price, Wine.title]

        # Get data based on variety
        results = session.query(*sel).\
            filter(Wine.variety == variety).all()

    
        country = [result[0] for result in results]
        points = [result[1] for result in results]
        price = [result[2] for result in results]
        title = [result[3] for result in results]
    
        variety_data = [{
            "country": country,
            "points": points,
            "price": price,
            "title": title
        }]
    return jsonify(variety_data)
        
    # Get data based on variety and country
    sel = [Wine.points, Wine.price, Wine.title]
  
    results = session.query(*sel).\
        filter(Wine.variety == variety).\
        filter(Wine.country == country).all()
    points = [result[0] for result in results]
    price = [result[1] for result in results]
    title = [result[2] for result in results]
    
    data = [{
        "points": points,
        "price": price,
       "title": title
       }]
    return jsonify(data)

# route for pie chart data (country count)
@app.route("/country_count/<variety>")
def country_count(variety):
    
    stmt = session.query(Wine).statement
    df = pd.read_sql_query(stmt, session.bind)
    variety_df = df.loc[df["variety"] == variety]
    country_count = variety_df["country"].value_counts().sort_values(ascending=False).astype(float).reset_index()
    country_count.columns = ["country", "count"]

    if variety not in df.variety.unique():
        return jsonify(f"Error: Variety: {variety} Not Found!"), 400

    data = [{
        "country": country_count["country"].values.tolist(),
        "country_count": country_count["count"].values.tolist(),
    }]
    return jsonify(data)

@app.route("/mapWine/<variety>")
@app.route("/mapWine/<variety>/<country>")
def mapwinevarcon(variety=None, country=None):
    

    # Select statement
    sel = [Wine.country, Wine.points, Wine.price, Wine.title, Wine.region_1, Wine.winery]

    if not country:
        # Get data based on variety
        results = session.query(*sel).\
            filter(Wine.variety == variety).all()
        wine_df = pd.DataFrame(results, columns=["country", "points","price","title", "region", "winery"])
        wine_df = wine_df[wine_df["region"].notnull()]
        #wine_df["price"].fillna(0, inplace=True);
        data = [{
        "country": wine_df["country"].values.tolist(),
        "points": wine_df["points"].values.tolist(),
        "price": wine_df["price"].values.tolist(),
        "title": wine_df["title"].values.tolist(),
        "region": wine_df["region"].values.tolist(),
        "winery": wine_df["winery"].values.tolist()
        }]
        return jsonify(data)
        

    # Get data based on variety and country
    results = session.query(*sel).\
        filter(Wine.variety == variety).\
        filter(Wine.country == country).all()
    wine_df = pd.DataFrame(results, columns=["country", "points","price","title", "region", "winery"])
    wine_df = wine_df[wine_df["region"].notnull()]
   # wine_df["price"].fillna(0, inplace=True);
    data = [{
        "country": wine_df["country"].values.tolist(),
        "points": wine_df["points"].values.tolist(),
        "price": wine_df["price"].values.tolist(),
        "title": wine_df["title"].values.tolist(),
        "region": wine_df["region"].values.tolist(),
        "winery": wine_df["winery"].values.tolist()
        }]
    return jsonify(data)

@app.route("/coords")
def coordinate():
    stmt = session.query(Coordinate).statement
    region_df = pd.read_sql_query(stmt, session.bind)
    region_df=region_df[region_df["coordinates"].notnull()]
    data = [{
       "region": region_df["region_1"].values.tolist(),
       "country": region_df["country"].values.tolist(),
       "coordinates": region_df["coordinates"].values.tolist()
   }]
    return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)
        