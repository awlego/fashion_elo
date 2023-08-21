# app/routes.py

from flask import render_template, jsonify, request
from app.models.models import Image
import random
from app.views import main  # import the blueprint

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
    print(data)
    selected_image_id = data['selected']
    unselected_image_id = data['unselected']
    # TODO: Handle the image selection logic if needed.
    # e.g. increment a counter for the selected image or log the choice
    print(selected_image_id, " selected")
    print(unselected_image_id, " unselected")

    # For simplicity, after selecting, we're just getting two new images.
    # You can modify this part based on what action you want to take after a selection.
    return get_two_random_images()