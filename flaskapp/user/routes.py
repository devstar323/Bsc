from flaskapp import app
from flaskapp.user.models import User


@app.route('/user/signup', methods=['POST','GET'])
def signup():
  return User().signup()

@app.route('/user/signout', methods=['POST','GET'] )
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST','GET'])
def login():
  return User().login()
  

# @app.route('/user/login', methods=['POST','GET'])
# def scrape():
#   return scrapped_page()
# @app.route('/dashboard/scrapped', methods=['POST','GET'])
# def scrapped():
#   num =20
#   hashtag = request.form.get('hashtag')
#   date=""
#   return scrape(hashtag,date,num)