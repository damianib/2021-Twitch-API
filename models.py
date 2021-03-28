from config import db, ma


# Streamer model to store streamers informations
class Streamer(db.Model):
    __tablename__ = "streamer"
    streamer_id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String)
    username = db.Column(db.String)
    stream_url = db.Column(db.String)
    profile_picture_url = db.Column(db.String)


# Streamer schema
class StreamerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Streamer
        load_instance = True
