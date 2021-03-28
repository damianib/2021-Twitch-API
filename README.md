# 2021-Twitch-API

Simple RESTFUL API using the Flask Connexion framework , and a SQLite database to register some streamers information like its username, profile picture URL and
streaming page URL. Those information are fetched using the [Official Twitch API](https://dev.twitch.tv/docs/api/).

# Setup

Create a new environment and install required Python modules with :

```pip install -r requirements.txt```

To start the API, run in the `./src/` directory :

```python app.py```

The API will be running on http://localhost:5000/api

### Twitch API Credentials

The `keyring` module is used to store your Twitch API client id and secret. You can set them in a Python console with the following code :

```python
import keyring

keyring.set_password("twitch_api", "client_id", {your_client_id})
keyring.set_password("twitch_api", "client_secret", {your_client_secret})
```

# API Resources

This API implement four basic operations :
* Get the list of all streamers stored in database
* Get the list of all streamers matching a given username (username is apparently unique on Twitch, but adding more streaming platforms to this API could create multiple entries with the same username in the db). If no matching streamer is found in the db, the API will try to fetch it from the official Twitch API.
* Create a new streamer
* Delete a streamer

A summary of all endpoints with detailed inputs and outputs is accessible at http://localhost:5000/api/ui/ when the API is running.

```
GET /streamers/ : returns the list of streamers from the database
GET /streamers/{username} : returns the list of matching streamers from the database
POST /streamers/ : create a new streamer
DELETE /streamers/{username} : remove the matching streamers from the database
```

# Adding new streaming platforms

To fetch from other streaming platforms API, you must :
* Add a new class `FetchXXXAPI` in the `fetch_streaming_api.py` file by respecting the structure of the `FetchStreamingAPI` abstract class. This class must implement a `fetch_streamer` method that returns `None` or a dictionnary with streamer info.
* Instantiate this new class in `config.py` and add it in the `apis_to_fetch` list
* Add a new step corresponding to the new API in the `get_one` function in `streamers.py`
