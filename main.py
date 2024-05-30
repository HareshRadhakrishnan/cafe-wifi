from flask import Flask,render_template,url_for ,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired,URL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
Bootstrap(app)
db = SQLAlchemy(app)

class Cafes(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True,nullable= False)
    map_url = db.Column(db.String, unique= True, nullable= False)
    img_url = db.Column(db.String, unique=True,nullable=False)
    location = db.Column(db.String,nullable=False)
    has_sockets= db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable= False)
    can_take_calls = db.Column(db.Boolean,nullable=False)
    seats = db.Column(db.String,nullable=False)
    coffee_price = db.Column(db.String,nullable=False)

class AddCafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    map_url = StringField('Location URL', validators=[DataRequired(),URL()])
    img_url = StringField('Cafe Image URL',validators=[DataRequired(),URL()])
    seats = StringField('Number of Seats available', validators=[DataRequired()])
    coffee_price = StringField('Price Per Coffee', validators=[DataRequired()])
    has_sockets = BooleanField('Are There Sockets in Cafe')
    has_toilet = BooleanField('Are There Toilets in Cafe')
    has_wifi = BooleanField('Are There Wifi in Cafe')
    can_take_calls = BooleanField('Can I take Call From Cafe')
    submit = SubmitField('Submit')

@app.route('/')
def home():
    all_cafes = Cafes.query.all()
    return render_template('index.html', cafes = all_cafes)

@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafes(name = form.name.data,
                         location=form.location.data,
                        map_url = form.map_url.data,
                        img_url = form.img_url.data,
                        seats = form.seats.data,
                        coffee_price = form.coffee_price.data,
                        has_sockets = bool(form.has_sockets.data),
                        has_toilet = bool(form.has_toilet.data),
                        has_wifi = bool(form.has_toilet.data),
                        can_take_calls = bool(form.can_take_calls.data))
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)
@app.route('/delete/<cafe_id>')
def delete(cafe_id):
    print(cafe_id)
    cafe_to_delete = Cafes.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)