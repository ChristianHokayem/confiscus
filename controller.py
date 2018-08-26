from flask import Flask, render_template
from random import choice

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('home.html')
	
@app.route('/tickle')
def slider_page():
    return render_template('tickle.html')