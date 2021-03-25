from flask import Flask, render_template, request, redirect, flash,url_for, flash
from flask_sqlalchemy import SQLAlchemy

#define
app = Flask(__name__)

#create secret key
app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///calories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#table model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(50),nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbohydrates = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)

    

    def __init__(self,food,proteins,carbohydrates,fats):
        self.food = food
        self.proteins = proteins
        self.carbohydrates = carbohydrates
        self.fats = fats


@app.route('/')
def index():

        all_data = Data.query.all()

        return render_template('index.html', macro_list = all_data)
        

@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':
        food = request.form['food']
        proteins = request.form['proteins']
        carbohydrates = request.form['carbohydrates']
        fats = request.form['fats']

        my_foods = Data(food,proteins,carbohydrates,fats)
        db.session.add(my_foods)
        db.session.commit()
        
        flash("successfully inputed")

        return redirect(url_for('index'))

@app.route('/update', methods=['GET','POST'])
def update():
    
    if request.method == 'POST':
        my_foods = Data.query.get(request.form.get('id'))

        my_foods.food = request.form['food']
        my_foods.proteins = request.form['proteins']
        my_foods.carbohydrates = request.form['carbohydrates']
        my_foods.fats = request.form['fats']

        db.session.commit()
        flash("updated successfully")

        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_foods = Data.query.get(id)
    db.session.delete(my_foods)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)