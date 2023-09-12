from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Movie('{self.name}')"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@cross_origin()
def search_names():
    user_input = request.form.get('input')
    search_results = Movie.query.filter(
                Movie.name.ilike(f'%{user_input}%')).all()

    movie_list = []
    for movie in search_results:
        movie_dict = {
            'id': movie.id,
            'name': movie.name,
        }
        movie_list.append(movie_dict)

    return jsonify(results=movie_list)

if __name__ == '__main__':
    app.run(debug=True)