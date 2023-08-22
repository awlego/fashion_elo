# app/routes.py

from flask import render_template, jsonify, request
from app.models.models import Image, Comparison, EloDB
import random
from app.views import main  # import the blueprint
from app import db

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/get_two_random_images', methods=['GET'])
def get_two_random_images():
    all_images = Image.query.all()
    random_images = random.sample(all_images, 2) if len(all_images) >= 2 else all_images
    return jsonify([{'uid': img.uid, 'path': img.filepath} for img in random_images])

@main.route('/select_image', methods=['POST'])
def select_image():
    data = request.json
    selected_image_id = data['selected']
    unselected_image_id = data['unselected']

    print(selected_image_id, " selected")
    print(unselected_image_id, " unselected")

    # Create a new instance of the Comparison model with the received data
    comparison = Comparison(
        selected_image_uid=selected_image_id,
        unselected_image_uid=unselected_image_id
    )

    # Add the new record to the current session
    db.session.add(comparison)
    
    # Commit the changes to save the record in the database
    db.session.commit()
    # For simplicity, after selecting, we're just getting two new images.
    # You can modify this part based on what action you want to take after a selection.
    return get_two_random_images()

@main.route('/elo_rankings', methods=['GET'])
def elo_rankings():
    images_ranked = db.session.query(EloDB, Image)\
                   .join(Image, EloDB.uid == Image.uid)\
                   .order_by(EloDB.elo.desc())\
                   .all()
    return render_template('elo_rankings.html', images=images_ranked)

