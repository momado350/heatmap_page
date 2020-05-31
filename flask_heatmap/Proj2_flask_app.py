import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect,Table, Column, ForeignKey
from flask import Flask, jsonify
from flask_cors import CORS
import geojson

#=======================================================
obesity_df = pd.read_csv('data_proj2.csv')
obesity_df = obesity_df.dropna()
obesity_df =pd.DataFrame(obesity_df)
#=======================================================
# cdc_data_df = pd.read_csv('cdc_data_clean1.csv')
# cdc_data_df = cdc_data_df.dropna()
# cdc_data_df =pd.DataFrame(cdc_data_df)
#=======================================================

rds_connection_string = "postgres:postgres@localhost:5432/obesity_db"
engine = create_engine(f'postgresql://{rds_connection_string}')
#https://github.com/cid-harvard/pandas-to-postgres/issues/8
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
obesity = Base.metadata.tables['obesity_study']
#cdc_data = Base.metadata.tables['cdc_data']
#cdc_data = Base.metadata.tables['census_data']
session = Session(engine)

obesity_df.to_sql(name='obesity_study',con=engine, if_exists='replace',index=False)
#cdc_data_df.to_sql(name='cdc_data',con=engine, if_exists='replace',index=False)

#https://geoffboeing.com/2015/10/exporting-python-data-geojson/
def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

#======================================================
# Flask app
#======================================================
app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def Home():
    print("Server received request for 'Home' page...")
    return("<div ><p><h1> Welcome to Obesity Study Api!</h1></p>"
  "</ol><li><strong font color ='blue'>Obesity study for 500 cities in the US: </strong><font color='orange'> /api/v1.0/over45percent</font></li>"
  "<li><strong>List of station:</strong><font color='orange'> /api/v1.0/bygender</font></li></ol></div>")

#===================================================
@app.route("/api/v1.0/over45percent")
def main():
    obesity_query =session.query(obesity)
    obesity_query = pd.read_sql(obesity_query.statement, obesity_query.session.bind)
    obesity_query = pd.DataFrame(obesity_query.loc[obesity_query["obesitypercentage"] >=45, :]) 
    cols = obesity_query.columns
    #print(cols)
    #obesity_query = obesity_query.to_dict()
    geojson = df_to_geojson(obesity_query,cols)
   
    return  geojson#jsonify(obesity_query)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route("/api/v1.0/bygender")
def cdcmain():
    cdc_data =session.query(cdc_data)
    cdc_data = pd.read_sql(cdc_data.statement, cdc_data.session.bind)
    #obesity_query = pd.DataFrame(obesity_query.loc[obesity_query["obesitypercentage"] >=45, :]) 
    cdc_data = cdc_data.to_dict()
    return jsonify(cdc_data)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    app.run(debug=True)
