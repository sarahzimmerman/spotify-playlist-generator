""" Specifies routing for the application"""
from flask import render_template, request, jsonify, url_for, redirect, session
from app import app
import json
from app import database as db_helper
import sys
import time

from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
from datetime import datetime

# app = Flask(__name__)

@app.before_first_request
def start_trigger():
    try:
        db_helper.song_trigger()
        print("created trigger")
    except:
        print("trigger failed")

@app.route("/delete/<string:artist_id>", methods=['DELETE'])
def delete(artist_id):
    """ recieved post requests for entry delete """
    print(artist_id, "DELETE ")
    try:
        db_helper.remove_artist_by_id(artist_id)
        result = {'success': True, 'response': 'Removed Artist'}
        return jsonify(result), 200
    except:
        result = {'success': False, 'response': 'Something went wrong'}
        return jsonify(result), 404 


@app.route("/edit/<string:artist_id>", methods=['PATCH'])
def update_artist(artist_id):
    """ recieved post requests for entry updates """
    data = request.get_json()
    print("artist id", artist_id, "popularity", data["popularityRating"], file=sys.stderr)
    try:
        if "popularityRating" in data:
            db_helper.update_artist(artist_id, data["popularityRating"])
            return jsonify({'success': True, 'response': 'Status Updated'}), 200
        else:
            result = {'success': False, 'response': 'No popularity rating'}
            return jsonify(result), 400
    except:
        result = {'success': False, 'response': 'Something went wrong'}
        return jsonify(result), 404


@app.route("/create_artist", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    try:
        db_helper.insert_new_artist(data['name'], data['followers'], data['image'], data['popularityRating']) 
        result = {'success': True, 'response': 'Done'}
        return jsonify(result), 200
    except:
        result = {'success': False, 'response': 'Could not insert into table'}
        return jsonify(result), 404

@app.route("/insert_song", methods = ['PUT']) #insert new song for trigger
def insert_song():
    data = request.get_json() 
    try:
        print("routes", data)
        #db_helper.insert_new_song("x", "x", 1, 1)
        db_helper.insert_new_song(str(data["name"]), str(data["genre"]), int(data["popularity"]), float(data["totalDuration"]), "6kZ42qRrzov54LcAk4onW9")
        result = {'success': True, 'response': 'Done'}
        return jsonify(result), 200
    except:
        result = {'success': False, 'response': 'Could not insert into table'}
        return jsonify(result), 404

@app.route("/above_avg") #adv query 1
def above_avg():
    try:
        items = db_helper.above_avg_playtime()
        return render_template("above_avg.html", items=items)
    except:
        return render_template("index.html"), 404

@app.route("/songs", methods = ['POST']) #adv query 2
def fetch_songs_advanced():
    print("here in songs")

    data = request.get_json() 
    try:
        items = db_helper.fetch_songs_advanced(data["genre"], data["start_date"], data["end_date"])
        session['items'] = items
        return (redirect(url_for("playlist")))
    except:
        return render_template("index.html"), 404

@app.route("/playlist")
def playlist():
    print("here ")

    items = session['items']
    #session.pop('items', default = None)
    print("hi ", items)
    return render_template("songs.html", items = items), 200


@app.route("/plot", methods = ['POST']) #adv query 2
def fetch_songs_advanced_plots():
    print("here in plots")

    data = request.get_json() 
    try:
        items = db_helper.fetch_songs_advanced_graph(data["genre"], data["start_date"], data["end_date"])
        session['items'] = items
        return (redirect(url_for("playlist_plots")))
    except:
        print("exception")
        return render_template("index.html"), 404

@app.route("/playlist_plots")
def playlist_plots():
    print("here ")

    items = session['items']
    # #session.pop('items', default = None)
    # print("in plots ", items)
    # return render_template("hist_plot.html", items = items), 200
    # year = datetime.date.today().year
    dict_data = {"name": [],"album_popularity": [],"releaseDate":[],"s_popularity": [],"genre":[]}
    for item in items:
        dict_data['name'].append(item['name'])
        dict_data['album_popularity'].append(item['a_popularity'])
        dict_data['releaseDate'].append(datetime.strptime(item['releaseDate'], '%a, %d %b %Y %H:%M:%S %Z').year)
        dict_data['s_popularity'].append(item['s_popularity'])
        dict_data['genre'].append(item['genre'])

    # print(dict_data)
    df = pd.DataFrame(dict_data)
    fig = px.scatter(df, x="releaseDate", y="album_popularity", color="genre", size='s_popularity', hover_data=['name'])


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # print(min(df.releaseDate))
    header="Scatterplot from {} to {}".format(min(df.releaseDate),max(df.releaseDate))
    description = "Scatterplot created using advanced query 2"
    return render_template('hist_plot.html', graphJSON=graphJSON, header=header,description=description)

@app.route("/search", methods = ['POST']) #search artist name
def fetch_artist_search():
    data = request.get_json()
    try:
        items = db_helper.fetch_artist_name(data["artistName"])
        session['artists'] = items
        if 'artists' not in session:
            return render_template("index.html"), 400
        return (redirect(url_for("search_results")))
    except:
        return render_template("index.html"), 404


@app.route("/search_results")
def search_results():
    items = "x"
    if 'artists' in session:
        items = session['artists']
    #session.pop('artists', default=None)
    print("hi ", items)
    return render_template("search.html", items = items), 200

@app.route("/")
def homepage():
    """ returns rendered homepage """
    if 'artists' in session:
        session.pop('artists')
    if 'items' in session:
        session.pop('items')
    items = db_helper.fetch_artist()
    return render_template("index.html", items=items)

@app.route("/stored_procedure", methods = ["GET"])
def call_procedure():
    items = db_helper.era_stored_procedure()
    return render_template("stored_procedure.html", items = items)
    