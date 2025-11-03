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

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

class InformationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100, min=4)])
    price = StringField('Price', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(max=100, min=2)])
    submit = SubmitField('Submit')


class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)


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