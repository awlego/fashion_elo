# app/routes.py

import random
import subprocess
import threading
import traceback

import numpy as np
from flask import jsonify, render_template, request

from app import db
from app.models.models import Comparison, EloDB, Image
from app.views import main  # import the blueprint


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/get_two_random_images', methods=['GET'])
def get_two_random_images():
    all_images = Image.query.all()
    random_images = random.sample(all_images, 2) if len(all_images) >= 2 else all_images
    return jsonify([{'uid': img.uid, 'path': img.filepath} for img in random_images])

@main.route('/get_two_random_matched_images', methods=['GET'])
def get_two_random_matched_images():
    all_images = Image.query.all()
    if len(all_images) < 2:
        return jsonify([{'uid': img.uid, 'path': img.filepath} for img in all_images])
    
    # Select a random image
    selected_image = random.choice(all_images)
    
    # Get the ELO rating of the selected image
    selected_elo = db.session.query(EloDB).filter_by(uid=selected_image.uid).first().elo
    
    # Retrieve all images with their ELO ratings
    images_with_elo = db.session.query(EloDB, Image).join(Image, EloDB.uid == Image.uid).all()
    
    # Create a list of ELO ratings and corresponding images
    elo_ratings = [elo.elo for elo, img in images_with_elo]
    images = [img for elo, img in images_with_elo]
    
    # Perform Gaussian sampling
    matched_image = None
    while not matched_image:
        # Generate a sample from the normal distribution centered around the selected ELO
        sampled_elo = np.random.normal(loc=selected_elo, scale=100)
        
        # Find the image with the closest ELO rating to the sampled value
        closest_image = min(images_with_elo, key=lambda x: abs(x[0].elo - sampled_elo))
        
        # Ensure the selected and matched images are not the same
        if closest_image[1].uid != selected_image.uid:
            matched_image = closest_image[1]
    
    # Return the two images
    return jsonify([
        {'uid': selected_image.uid, 'path': selected_image.filepath},
        {'uid': matched_image.uid, 'path': matched_image.filepath}
    ])

def run_calc_elo():
    python_interpreter = r"C:\\Users\\awlego\\Documents\\Repositories\\fashion_elo\\env\Scripts\\python.exe"
    try:
        result = subprocess.run(
            [python_interpreter, r"C:\Users\awlego\Documents\Repositories\fashion_elo\calc_elo.py"],
            check=True,
            capture_output=True,
            text=True
        )
        print("calc_elo.py output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running calc_elo.py: {e}")
        print("Standard output:", e.stdout)
        print("Standard error:", e.stderr)
        print("Traceback:", traceback.format_exc())

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

    thread = threading.Thread(target=run_calc_elo)
    thread.start()

    # For simplicity, after selecting, we're just getting two new images.
    # You can modify this part based on what action you want to take after a selection.
    return get_two_random_matched_images()

@main.route('/elo_rankings', methods=['GET'])
def elo_rankings():
    images_ranked = db.session.query(EloDB, Image)\
                   .join(Image, EloDB.uid == Image.uid)\
                   .order_by(EloDB.elo.desc())\
                   .all()
    return render_template('elo_rankings.html', images=images_ranked)

