# Standard library imports
import hashlib
import os
from datetime import datetime

# Local application imports
from app import create_app, db
from app.models.models import Image

def compute_image_uid(image_path):
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()
    
app = create_app()

IMAGES_DIR = "app/static/images/"

# Get all files from the directory
all_images = [os.path.join(IMAGES_DIR, filename) for filename in os.listdir(IMAGES_DIR) if filename.endswith(('.png', '.jpg', '.jpeg', 'webp'))]  # you can add more image formats if needed

# Now loop through the images and add them to the database
with app.app_context():
    for image_path in all_images:
        db_image_path = image_path.removeprefix(IMAGES_DIR)
        print(db_image_path)
        image_uid = compute_image_uid(image_path)

        # Check if the UID already exists
        existing_image = Image.query.filter_by(uid=image_uid).first()
        if not existing_image:
            new_image = Image(uid=image_uid, filepath=db_image_path)
            db.session.add(new_image)

    # Commit the changes once all images have been processed
    db.session.commit()

# Single example:
# image1_path = "static/images/10339541_876542.jpg"
# image2_path = "static/images/6461861_1314016.jpg"

# image1_uid = compute_image_uid(image1_path)
# image2_uid = compute_image_uid(image2_path)


# with app.app_context():  # <-- Use the app context for the DB operations
#     print(app.config['SQLALCHEMY_DATABASE_URI'])
#     # Check if the UID already exists for image1
#     existing_image1 = Image.query.filter_by(uid=image1_uid).first()
#     if not existing_image1:
#         new_image1 = Image(uid=image1_uid, filepath=image1_path)
#         db.session.add(new_image1)

#     # Check if the UID already exists for image2
#     existing_image2 = Image.query.filter_by(uid=image2_uid).first()
#     if not existing_image2:
#         new_image2 = Image(uid=image2_uid, filepath=image2_path)
#         db.session.add(new_image2)

#     db.session.commit()