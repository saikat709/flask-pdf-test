from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, BooleanField
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


class PDFGenerationForm(FlaskForm):
    submit = SubmitField('Generate PDF')

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

    presidential_election_campaign = BooleanField('Presidential Election Campaign', default=False)
    presidential_election_campaign_spouse = BooleanField('Presidential Election Campaign Spouse', default=False)

    submit = SubmitField('Submit')



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
    presidential_election_campaign = db.Column(db.Boolean, default=False)
    presidential_election_campaign_spouse = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Information {self.id}: {self.first_name} {self.last_name}>"


@app.route('/')
def index():
    infos = Information.query.all()
    pdf_generation_form = PDFGenerationForm()
    print(infos)
    return render_template('index.html', infos=infos, pdf_generation_form=pdf_generation_form)


@app.route('/add-info', methods=['GET', 'POST'])
def add_info():
    form = InformationForm()
    if form.validate_on_submit():
        new_info = Information(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            spouse_first_name=form.spouse_first_name.data,
            spouse_last_name=form.spouse_last_name.data,
            social_security_number=form.social_security_number.data,
            spouse_social_security_number=form.spouse_social_security_number.data,
            home_address=form.home_address.data,
            apt_no=form.apt_no.data,
            town=form.town.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            foreign_country_name=form.foreign_country_name.data,
            foreign_province=form.foreign_province.data,
            foreign_postal_code=form.foreign_postal_code.data,
            presidential_election_campaign=form.presidential_election_campaign.data,
            presidential_election_campaign_spouse=form.presidential_election_campaign_spouse.data,
        )
        db.session.add(new_info)
        db.session.commit()
        return redirect(url_for('add_info'))
    return render_template('add-info.html', form=form)



@app.route('/generate-pdf/<int:info_id>', methods=['POST'])
def generate_pdf(info_id):
    info = Information.query.get(info_id)
    if not info:
        return "Information not found", 404

    # PDF generation logic goes here
    return "PDF generation logic goes here"


if __name__ == '__main__':
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            # db.create_all()
            print('----------Connection successful !------------')
        except Exception as e:
            print('[Error] Connection failed ! ', e)
    app.run(debug=True)