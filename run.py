from flask import render_template
from flaskapp import app, login_required
from flaskapp.user.routes import *
import pandas as pd
import json

# for annotation
import urllib.request
from inscriptis import get_annotated_text, ParserConfig
from inscriptis.annotation.output.html import HtmlExtractor

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/login')
def login_page():
  return render_template('login.html')

@app.route('/profile')
def profile():
  return render_template('profile.html')

@app.route('/dashboard')
@login_required
def dashboard():
  return render_template('dashboard.html')

@app.route('/scrapped')
def scrapped_page():
  data = pd.read_csv('scraped_tweets.csv')
  return render_template('index.html', tables=[data.to_html()], titles=[''])

@app.route('/search')
def search_page():
  return render_template('search.html')

@app.route('/annotate')
def annotate_page():
  with open('test.html', 'r') as f:
    html_string = f.read()
  with open('annotation-profile.json', 'r') as f:
    rules = json.load(f) 
  output = get_annotated_text(html_string, ParserConfig(annotation_rules=rules))
  # HtmlExtractor.__call__(HtmlExtractor, output)
  # HtmlExtractor._get_label_colors('heading', 'red')
  return render_template('annotate.html', output=[output])

if __name__ == '__main__':
  app.run(host = "0.0.0.0",debug=True)