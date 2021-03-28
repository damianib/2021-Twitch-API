from flask import make_response, abort
from config import db, twitch, app
from models import Streamer, StreamerSchema


def get_all():

    """Get all streamers from db"""

    # Get all streamers from db
    streamers = Streamer.query.all()

    # Serialize the data for the response
    streamer_schema = StreamerSchema(many=True)
    data = streamer_schema.dump(streamers)
    return data


def get_one(username):

    """Get all streamers matching with username"""

    # Get matching streamers (if multiple platforms there could be more than one result)
    streamers = Streamer.query.filter(Streamer.username == username).all()

    # If no streamer found
    if len(streamers) == 0:
        # ADD NEW APIS HERE
        # Try to fetch streamer from Twitch API
        streamer = twitch.fetch_streamer(username)
        # If found with Twitch API, create it
        if streamer is not None:
            create(streamer)
        else:
            abort(
                404,
                "Streamer not found for username : {}".format(username),
            )

    # Serialize list of matching streamers
    streamers = Streamer.query.filter(Streamer.username == username)
    streamer_schema = StreamerSchema(many=True)
    data = streamer_schema.dump(streamers)
    return data


def create(streamer):

    """Create streamer"""

    username = streamer['username']
    platform = streamer['platform']
    # Check for existing streamer with same username on same platform
    existing_streamer = Streamer.query.filter(Streamer.username == username).filter(Streamer.platform == platform).one_or_none()

    # If no existing streamer, create it
    if not existing_streamer:
        schema = StreamerSchema()
        new_streamer = schema.load(streamer, session=db.session)

        # Add the person to the database
        db.session.add(new_streamer)
        db.session.commit()

        return make_response(
            "{} successfully created".format(username), 201
        )
    else:
        abort(
            406,
            "Streamer with username {} already exists".format(username),
        )


def delete(username):

    """Delete streamers with matching username"""

    # Find matching streamers
    existing_streamers = Streamer.query.filter(Streamer.username == username).all()

    if existing_streamers is not None:
        # Delete streamer for all platforms
        for streamer in existing_streamers:
            db.session.delete(streamer)
        db.session.commit()

        return make_response(
            "{} successfully deleted".format(username), 201
        )
    else:
        abort(
            406,
            "Streamer with username {} not found".format(username),
        )
