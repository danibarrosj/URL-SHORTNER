from flask import Flask, request, jsonify, redirect,render_template
from flask_sqlalchemy import SQLAlchemy
import string,random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db' 
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column (db.String(10), unique=True, nullable=False)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length)) 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    try:
        print("Request received:", request.headers)  

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form  

        long_url = data.get("long_url")
        print("Received long_url:", long_url)  

        if not long_url:
            return jsonify({'error': 'Missing URL'}), 400  

        # Check if URL already exists
        existing = URL.query.filter_by(long_url=long_url).first()
        if existing:
            return jsonify({'short_url': request.host_url + existing.short_code}), 200  

        short_code = generate_short_code()
        new_url = URL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()

        return jsonify({'short_url': request.host_url + short_code}), 200  

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500  


@app.route('/<short_code>')
def redirect_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return redirect(url_entry.long_url)
    if not url_entry:
        return jsonify({'error': 'URL not found'}), 404
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
