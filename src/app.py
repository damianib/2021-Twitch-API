from config import connex_app, db


# Create the database
db.create_all()

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


@connex_app.route('/')
def henlo_world():
    return 'Henlo World!'


if __name__ == '__main__':
    connex_app.run(debug=True)
