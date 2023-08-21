from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fashion_elo.db'
db = SQLAlchemy(app)

class ImageComparison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selected_image = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record():
    selected_image = request.json.get('selected_image')
    
    new_record = ImageComparison(selected_image=selected_image)
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify({"message": "Recorded successfully!"})

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()  # This will create the SQLite database
    app.run(debug=True)
