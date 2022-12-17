from flask import render_template
from flaskapp import app, login_required
from flaskapp.user.routes import *
import pandas as pd

@app.route('/')
def home():
  return render_template('home.html')


@app.route('/login')
def login_page():
  return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
  return render_template('dashboard.html')

@app.route('/scrapped')
def scrapped_page():
  # return render_template('index.html')

  data = pd.read_csv('scraped_tweets.csv')
  return render_template('index.html', tables=[data.to_html()], titles=[''])

@app.route('/collect')
def collect_page():
  return render_template('collect.html') 
  

if __name__ == '__main__':
  app.run(host = "0.0.0.0",debug=True)
  