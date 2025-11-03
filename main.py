from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost:5432/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended to disable
db = SQLAlchemy(app)



@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Flask App!"


if __name__ == '__main__':
    app.run(debug=True)
