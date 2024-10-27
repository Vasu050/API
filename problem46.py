'''import requests
import json

response=requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
# print(response)  status if succssful response 200
for data in response.json()['items']:
    print(data['title'])
'''

from flask import Flask,jsonify,request,redirect,render_template
app= Flask(__name__)
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dabta.db'
db=SQLAlchemy(app)

class Drink(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    description=db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name},{self.description}"
    
with app.app_context():
    db.create_all()  # This line will create the 'test.db' file if it doesn't exist
    print("Database and tables created!")

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        action = request.form['action']
        if action=='add':
            name = request.form['drink']
            description=request.form['description']
            drink=Drink(name=name,description=description)
            db.session.add(drink)
            db.session.commit()
            return redirect('/')
        else:
            name = request.form['drink']
            description=request.form['description']
            drink=Drink(name=name,description=description)
            db.session.add(drink)
            db.session.commit()
            return redirect('/drinks')
    else:
            return render_template('api.html')

@app.route('/drinks')
def get_drinks():
    drinks=Drink.query.all()

    output=[]
    for drink in drinks:
        drink_data={'name':drink.name,'description':drink.description}
        output.append(drink_data)
    return {'drinks':output} 

@app.route('/drinks/<id>')
def get_drink(id):
    drink=Drink.query.get_or_404(id)
    return jsonify({"name":drink.name,"description":drink.description})

@app.route('/drinks',methods=['POST'])
def add_drink():
    drink=Drink(name=request.json['name'],description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id':drink.id}

@app.route('/drinks/<id>',methods=['DELETE'])
def delete_drink(id):
    drink=Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return redirect('/drinks')
app.run(debug=True)