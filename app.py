from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app, Flask

import requests
import json



app = Flask(__name__)

api_key='b105dbabeeabdf41bafb40b2dc0dfea7'
base_url='https://api.themoviedb.org/3'

dummy_fav = [550, 33532, 235234]
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if not session['logged_in']:
        if request.method == 'POST':
            if request.form['username'] != current_app.config['USERNAME']:
                error = 'Invalid username'
            elif request.form['password'] != current_app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                session['user_name'] = 1
                flash('You were logged in')
                return redirect(url_for('/dashboard/{}'.format(session['user_name'])))
        return render_template('login.html', error=error)
    else:
        return redirect(url_for('/dashboard/{}'.format(session['user_name'])))


@app.route("/")
@app.route("/dashboard/<user_id>")
def dashboard(user_id=1):
    latest_movie = requests.get('{}/movie/latest?api_key={}'.format(base_url, api_key))
    movie_list = []
    if user_id is not None:
        for id in dummy_fav:
            r = requests.get('{}/movie/{}?api_key={}'.format(base_url, id, api_key))
            if 'title' in r.json().keys():
                movie_list.append(r.json())
    return render_template('dashboard.html', latest_movie=latest_movie.json(), fav = movie_list)
    

if __name__ == '__main__':
   app.run(debug = True)