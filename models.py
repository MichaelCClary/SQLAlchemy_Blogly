from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


default_url = "https://media.istockphoto.com/vectors/man-vector-icon-gender-icon-vector-id1132067376?k=6&m=1132067376&s=612x612&w=0&h=BUCm8AwVk5yoZnW6M5JWy2NLbN93NwFL1Rm8n69pwvw="


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    image_url = db.Column(db.String(300), nullable=False,
                          default=default_url)

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
