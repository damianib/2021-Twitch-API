import keyring
import requests


class FetchStreamingAPI:

    """Abstract class that every API-fetching class must implement"""

    def fetch_streamer(self, username):
        pass


class FetchTwitchAPI(FetchStreamingAPI):

    """Fetch Twitch API results for streamers"""

    def __init__(self):
        # client_id and client_secret must be set first with keyring
        self.client_id = keyring.get_password("twitch_api", "client_id")
        self.client_secret = keyring.get_password("twitch_api", "client_secret")

    def fetch_streamer(self, username):

        """
        Get streamer on Twitch matching with username
        :param username: str
        """

        # OAuth 2 authentication
        token_response = requests.post('https://id.twitch.tv/oauth2/token', params={"client_id": self.client_id,
                                                                                    "client_secret": self.client_secret,
                                                                                    "grant_type": "client_credentials"})
        access_token = token_response.json()['access_token']
        # get response
        streamer_response = requests.get('https://api.twitch.tv/helix/users', params={"login": username},
                                         headers={'Authorization': 'Bearer {}'.format(access_token),
                                                  'client-id': self.client_id})

        if streamer_response.status_code != 200:
            return None
        else:
            streamer_data = streamer_response.json()['data']
            # if no matching streamer found on Twitch
            if len(streamer_data) == 0:
                return None
            else:
                # else get all needed values
                streamer_data = streamer_data[0]
                username = streamer_data['login']
                stream_url = "twitch.tv/{}".format(username)
                profile_picture_url = streamer_data['profile_image_url']
                return {"platform": "Twitch", "username": username, "stream_url": stream_url,
                        "profile_picture_url": profile_picture_url}
