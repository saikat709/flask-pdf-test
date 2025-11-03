from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRESQL_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

app.config['STATIC_FOLDER'] = 'static'
app.config['STATIC_URL_PATH'] = '/static'

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

class InformationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100, min=4)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100, min=4)])
    spouse_first_name = StringField('Spouse First Name', validators=[DataRequired(), Length(max=100, min=4)])
    spouse_last_name = StringField('Spouse Last Name', validators=[DataRequired(), Length(max=100, min=4)])

    social_security_number = StringField('Social Security Number', validators=[DataRequired(), Length(max=11, min=9)])
    spouse_social_security_number = StringField('Spouse Social Security Number', validators=[DataRequired(), Length(max=11, min=9)])

    home_address = StringField('Home Address', validators=[DataRequired(), Length(max=200, min=4)])
    apt_no = StringField('Apt No', validators=[Length(max=20)])
    town = StringField('Town/City', validators=[DataRequired(), Length(max=100, min=2)])
    state = StringField('State', validators=[DataRequired(), Length(max=2, min=2)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(max=10, min=5)])

    foreign_country_name = StringField('Foreign Country Name', validators=[Length(max=100)])
    foreign_province = StringField('Foreign Province', validators=[Length(max=100)])
    foreign_postal_code = StringField('Foreign Postal Code', validators=[Length(max=20, min=4)])



class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    spouse_first_name = db.Column(db.String(100), nullable=False)
    spouse_last_name = db.Column(db.String(100), nullable=False)
    social_security_number = db.Column(db.String(11), nullable=False)
    spouse_social_security_number = db.Column(db.String(11), nullable=False)
    home_address = db.Column(db.String(200), nullable=False)
    apt_no = db.Column(db.String(20), nullable=True)
    town = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    foreign_country_name = db.Column(db.String(100), nullable=True)
    foreign_province = db.Column(db.String(100), nullable=True)
    foreign_postal_code = db.Column(db.String(20), nullable=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InformationForm()
    if form.validate_on_submit():
        new_info = Information(
            name=form.name.data,
            price=form.price.data,
            city=form.city.data
        )
        db.session.add(new_info)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            # db.create_all()
            print('\n\n----------- Connection successful !')
        except Exception as e:
            print('\n\n----------- Connection failed ! ERROR : ', e)
    app.run(debug=True)