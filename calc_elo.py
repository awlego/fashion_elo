
import pprint

from elo.elo import Elo

from app import create_app, db
from app.models.models import Comparison, Image, EloDB

app = create_app()

def add_items_to_elo_league():
    DEFAULT_ELO = 1200
    elo_league = Elo(k = 20, homefield=0)

    with app.app_context():
        images = Image.query.all()
        for image in images:
            elo_league.addPlayer(image.uid, rating = DEFAULT_ELO)

    return elo_league

def run_league(elo_league):
    with app.app_context():
        comparisons = Comparison.query.all()
        for comp in comparisons:
            elo_league.gameOver(winner = comp.selected_image_uid, loser = comp.unselected_image_uid, winnerHome=True)

def print_elos(elo_league):
    pprint.pprint(elo_league.ratingDict)


def save_league_to_db(elo_league):
    with app.app_context():
        for uid, rating in elo_league.ratingDict.items():
            elo_entry = EloDB.query.filter_by(uid=uid).first()
            
            if elo_entry:
                # Update the existing record
                elo_entry.elo = rating
            else:
                # Create a new record
                new_elo_entry = EloDB(uid=uid, elo=rating)
                db.session.add(new_elo_entry)

        db.session.commit()


elo_league = add_items_to_elo_league()
# print_elos(elo_league)
run_league(elo_league)
# print_elos(elo_league)
save_league_to_db(elo_league)


# with app.app_context():
#     for image_path in all_images:
#         db_image_path = image_path.removeprefix(IMAGES_DIR)
#         print(db_image_path)
#         image_uid = compute_image_uid(image_path)

#         # Check if the UID already exists
#         existing_image = Image.query.filter_by(uid=image_uid).first()
#         if not existing_image:
#             new_image = Image(uid=image_uid, filepath=db_image_path)
#             db.session.add(new_image)

#     # Commit the changes once all images have been processed
#     db.session.commit()