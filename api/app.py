import json
import time
from datetime import datetime
import requests
from splinter import Browser
from flask import Flask, request, g, session
from flask_cors import CORS, cross_origin
from urllib.parse import quote, urlencode
import re
import inspect
from lib import utils
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import User, SpotifyUser
import selenium
from requests.models import PreparedRequest

requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

class SplinterException(Exception):
    pass

class LoginError(Exception):
    pass


          

class SpotifyForArtistsAPI(object):
    class Auth(object):
        def __init__(self):
            self.client_id = "6cf79a93be894c2086b8cbf737e0796b"  # ID de cliente de la APP Spotify for Artists
            self.redirect_uri = "https://artists.spotify.com"
            self.code_verifier = self._get_code_verifier()
            self.code_challenge = self._get_code_challenge()
            self.scope = "streaming user-read-email user-read-private ugc-image-upload"  # Scope de la APP Spotify for Artists
            self.code_challenge_method = "S256"
            self.auth_code = None
            self.token = None
            self.expires = None
            self.refresh_tkn = None
            self.login_cookies = None
            self.web_client_token = None
            self.web_client_expires = None
            
        class NoAccess(Exception):
            pass
        
        class NoLoginData(Exception):
            pass
            
        class RefreshTokenRevoked(Exception):
            pass

        def login(self, username=None, password=None):
            browser = None
            try:
                browser = Browser(headless=True)  # Se inicia un navegador oculto de splinter
                print("Usando Firefox para login")
            except selenium.common.exceptions.WebDriverException as e:
                try:
                    browser = Browser('chrome', headless=True)  # Se inicia un navegador oculto de splinter
                    print("Usando Chrome para login")
                except selenium.common.exceptions.WebDriverException as e:
                    raise SplinterException(e.text)


            auth_url = 'https://accounts.spotify.com/experimental/authorize'
            auth_parameters = {
                'response_type': 'code',
                'client_id': self.client_id,
                'scope': self.scope.replace(" ", "+"),
                'code_challenge': self.code_challenge,
                'code_challenge_method': self.code_challenge_method,
                'redirect_uri': self.redirect_uri,
                'response_mode': 'web_message',
                'prompt': 'none',
                'state': '-w.M--UAilrUqEroxaLYEgx2NOaxZSoK',
            }
            auth_parameters = "?{}".format(urlencode(auth_parameters)).replace('%2B', '+')
            login_url = 'https://accounts.spotify.com/login?continue={}'.format(quote(auth_url+auth_parameters))

            browser.visit(login_url)  # Se accede con el navegador
            print("Accediendo... ", login_url)
            if self.login_cookies:
                print("El usuario ya esta logueado")
                browser.cookies.add(self.login_cookies)
                browser.visit(login_url)  # Se accede con el navegador
            else:
                print("Se logea al usuario con user y pass")
                browser.find_by_id("login-username").fill(username)
                browser.find_by_id("login-password").fill(password)
                browser.find_by_id("login-button").click()
                time.sleep(1)
                m = re.search(r'role=\"alert\"[\w\s\-\=\"]*\>(<[\w\s\=\"\-\#\.\/]*>)*([\w\s\ñ\.]*)', browser.html)
                if m and m.group(2):
                    browser.quit()
                    raise LoginError(m.group(2))

            while 'login' in browser.url:
                print(browser.url)
                time.sleep(1)

            print("Response: ", browser.html)
            m = re.search(r'\"code\": \"([\w\_\-]+)\"', browser.html)
            self.auth_code = m.group(1)
            print("Auth code: ", m.group(1))
            
            if not self.login_cookies and browser.cookies.all():
                self.login_cookies = browser.cookies.all()

            browser.visit("https://open.spotify.com")
            
            m = re.search(r'\"accessToken\":\"([\w\_\-]+)\"\,\"accessTokenExpirationTimestampMs\":([\d]*)', browser.html)
            self.web_client_token = m.group(1)
            self.web_client_expires = m.group(2)
            
            print("Web Auth token: ", m.group(1))
            print("Web Expires: ", m.group(2))#datetime.fromtimestamp(int(m.group(2))).strftime("%d-%m-%Y %H:%M:%S"))
            
            browser.quit()  # Cerrar navegador

        def _get_code_verifier(self):
            """ Spotify PCKE code verifier - See step 1 of the reference guide below
            Reference:
            https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow-with-proof-key-for-code-exchange-pkce
            """
            # Range (33,96) is used to select between 44-128 base64 characters for the
            # next operation. The range looks weird because base64 is 6 bytes
            import random
            length = random.randint(33, 96)

            # The seeded length generates between a 44 and 128 base64 characters encoded string
            try:
                import secrets
                verifier = secrets.token_urlsafe(length)
            except ImportError:  # For python 3.5 support
                import base64
                import os
                rand_bytes = os.urandom(length)
                verifier = base64.urlsafe_b64encode(rand_bytes).decode('utf-8').replace('=', '')
            return verifier

        def _get_code_challenge(self):
            """ Spotify PCKE code challenge - See step 1 of the reference guide below
            Reference:
            https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow-with-proof-key-for-code-exchange-pkce
            """
            import base64
            import hashlib
            code_challenge_digest = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
            code_challenge = base64.urlsafe_b64encode(code_challenge_digest).decode('utf-8')
            return code_challenge.replace('=', '')

        def get_token(self):
            print("Getting token")
            if self.auth_code:
                token_url = 'https://accounts.spotify.com/api/token'
                payload = {
                    'grant_type': 'authorization_code',
                    'client_id': self.client_id,
                    'code': self.auth_code,
                    'redirect_uri': self.redirect_uri,
                    'code_verifier': self.code_verifier
                }
                r = requests.post(token_url, data=payload)
                data = r.json()  # Se carga el contenido como JSON
                print(data)
                token = data['access_token']  # Token de acceso
                expires_time = data['expires_in']  # Timestamp de caducidad en milisegundos
                refresh_token = data['refresh_token']
                self.token = token
                self.expires = time.time() + expires_time
                self.refresh_tkn = refresh_token
                print("\t[+] New Token expires at {}".format(datetime.fromtimestamp(self.expires).strftime("%d-%m-%Y %H:%M:%S")))

        def refresh_token(self):
            print("Refreshing token")
            if self.refresh_token:
                token_url = 'https://accounts.spotify.com/api/token'
                payload = {
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_tkn,
                    'client_id': self.client_id,
                }
                r = requests.post(token_url, data=payload)
                data = r.json()  # Se carga el contenido como JSON
                print(data)
                if 'error' in data and data["error"] == "invalid_grant":
                    raise self.RefreshTokenRevoked(data["error_description"])
                elif 'error' in data and data["error"] == "invalid_request":
                    raise self.RefreshTokenRevoked(data["error_description"])
                elif 'error' in data and data["error"] == "server_error":
                    raise self.RefreshTokenRevoked(data["error_description"])
                token = data['access_token']  # Token de acceso
                expires_time = data['expires_in']  # Timestamp de caducidad en milisegundos
                self.token = token
                self.expires = time.time() + expires_time
            print(
                "\t[+] New Token expires at {}".format(datetime.fromtimestamp(self.expires).strftime("%d-%m-%Y %H:%M:%S")))

        def check_token_expired(self):
            if self.token is not None and self.expires is not None and time.time() >= self.expires:
                return True
            else:
                return False

    def __init__(self, token=None, refresh_token=None, expires=None, username=None, password=None, login_cookies=None, web_client_token=None):
        self.auth = self.Auth()
        self.url = "https://generic.wg.spotify.com"
        self.public_url = "https://api.spotify.com/v1"

        # Si se pasa usuario y contraseña
        if username and password:
            self.auth.login(username, password)  # Login para obtener auth code
            self.auth.get_token()  # Obtener token con auth code
        # Si se pasa el refresh_token
        elif token and refresh_token and expires:
            # Se introducen los tokens en el objeto
            self.auth.token = token
            self.auth.refresh_tkn = refresh_token
            self.auth.expires = expires
            self.auth.web_client_token = web_client_token
        elif login_cookies:
            self.auth.login_cookies = login_cookies
            self.auth.login()
            self.auth.get_token()  # Obtener token con auth code

        # Si ha caducado el token, actualizarlo
        if self.auth.check_token_expired():
            self.auth.refresh_token()

    def __get_headers__(self, token="artists"):
        if token == "artists":
            authorization = "Bearer {}".format(self.auth.token)
        else:
            authorization = "Bearer {}".format(self.auth.web_client_token)
            print("Auth Web Client ", self.auth.web_client_token)
        return {
            'authorization': authorization,
            'accept': 'application/json',
            'content-type': 'application/json',
            'User-Agent': "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            'app-platform': 'Browser',
            'spotify-app-version': '1.0.0.f628aa6',
            'origin': "https://artists.spotify.com"
        }

    def __make_request__(self, url, debug_name="", token="artists"):
        r = requests.get(url, headers=self.__get_headers__(token), proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}, verify=False)
        if r.status_code != 200:
            print(debug_name, r.status_code, r.text)

        return r.text
        
    def check_access(self):
        me = self.get_me()
        print(me)
        if me["hasAccess"] == "false":
            return False
        else:
            return True
        
    def check_spotify_id(self, artist_id):
        regex = r'[0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]+'
        length = 22
        if artist_id and len(artist_id) == length:
            m = re.search(regex, artist_id)
            if m:
                return True
        return False

    def get_me(self):
        path = "s4x-me/v0/me"
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_initial(self):
        if self.check_access():
            path = "creator-search-service/v0/artists/initial"
            url = "{}/{}".format(self.url, path)
            return json.loads(self.__make_request__(url, inspect.stack()[0][3]))
        else:
            raise self.auth.NoAccess("User has no Spotify for Artists access")

    def get_artist_public(self, artist_id):
        path = "artists/{}".format(artist_id)
        url = "{}/{}".format(self.public_url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))
        
    def get_song_public(self, song_id):
        path = "tracks/{}".format(song_id)
        url = "{}/{}".format(self.public_url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))
        
    def get_song_credits_public(self, song_id):
        url = "https://spclient.wg.spotify.com"
        path = "track-credits-view/v0/experimental/{}/credits".format(song_id)
        url = "{}/{}".format(url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))


    def get_song_lyrics_public(self, track_id):
        song_data = self.get_song_public(track_id)
        image_url = song_data["album"]["images"][0]["url"]
        url = "https://spclient.wg.spotify.com"
        path = "color-lyrics/v2/track/{}/image/{}".format(track_id, quote(image_url, safe=''))
        url = "{}/{}".format(url, path)
        params = {
            "format": "json",
            "vocalRemoval": "false",
            "market": "from_token"
        }
        req = PreparedRequest()
        req.prepare_url(url, params)
        url = req.url
        return json.loads(self.__make_request__(url, inspect.stack()[0][3], "web"))


    def get_manage_team(self):
        path = "marketplace-mgmt/v1/team/manageteam"
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_artists(self):
        path = "s4x-me/v0/artists"
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_settings(self):
        path = "marketplace-mgmt/v0/settings"
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_permissions(self, artist_id):
        path = "s4x-insights-api/v1/artist/{}/permissions".format(artist_id)
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_home(self, artist_id):
        path = "s4x-home-service/v1/artist/{}/home".format(artist_id)
        url = "{}/{}".format(self.url, path)
        payload = """{
          homestats {
            s4xinsightsapi {
              latestDate
              overview {
                followers {
                  delta
                  total
                  deltaPct
                }
                listeners {
                  total
                  deltaPct
                }
                streams {
                  total
                  deltaPct
                }
              }
              playlistCollection {
                dataList {
                  uri
                  listeners
                  followers
                  streams
                  title
                  thumbnailUrl
                  isPersonalized
                }
              }
              recordingStatsTable {
                recordingStatsList {
                  numListeners
                  numStreams
                  trackName
                  trend
                  trackUri
                  pictureUri
                  isDisabled
                }
              }
            }
            cards {
              cardsList {
                uuid
                resourceUri
                cardType
                cardSource
                notificationClass
                clickExpirationBuffer {
                  day
                  hour
                  minute
                  second
                }
                displayCard {
                  header
                  title
                  subtitle
                  callToAction {
                    text
                    url
                  }
                  headerType
                  displayType
                  fallbackImageUrl
                  cardColorList {
                    preset
                    colorHex
                  }
                }
              }
            }
          }
        }"""
        r = requests.post(url, headers=self.__get_headers__(), json={'query': payload, 'variables': {}})
        if r.status_code != 200:
            print(inspect.stack()[0][3], r.status_code, r.text)
        return json.loads(r.text)

    def get_roster_view(self):
        path = "roster-view-service/v1/artists?offset=0"
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_pitch(self, artist_id, album_id):
        path = "nms-form/v1/artist/{}/album/{}/view?utm_source=home".format(artist_id, album_id)
        url = "{}/{}".format(self.url, path)
        data = self.__make_request__(url, inspect.stack()[0][3])
        if data:
            return json.loads(data)
        return None

    def get_music_songs(self, artist_id, type='recording', filter='28day', start_date=None, end_date=None):
        """
        :param type: recording, ... ?
        :param filter: 1day | 7day | 28day | 1year | last5years | all | custom | sincelaunch
        :param start_date: yyyy-MM-dd
        :param end_date: yyyy-MM-dd
        """
        path = "s4x-insights-api/v2/artist/{}/recordings".format(artist_id)
        parameters = {
            "aggregation-level": type,
            "time-filter": filter
        }
        if start_date and end_date:
            parameters["time-filter"] = "custom"
            parameters["start-date"] = start_date
            parameters["end-date"] = end_date

        path = path + "?{}".format(urlencode(parameters))
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_music_releases(self, artist_id, filter='28day', start_date=None, end_date=None):
        """
        :param filter: 1day | 7day | 28day | 1year | last5years | all | custom | sincelaunch
        :param start_date: yyyy-MM-dd
        :param end_date: yyyy-MM-dd
        """
        path = "s4x-insights-api/v1/artist/{}/releases/released".format(artist_id)
        parameters = {
            "time-filter": filter
        }
        if start_date and end_date:
            parameters["time-filter"] = "custom"
            parameters["start-date"] = start_date
            parameters["end-date"] = end_date

        path = path + "?{}".format(urlencode(parameters))
        url = "{}/{}".format(self.url, path)
        return self.__make_request__(url, inspect.stack()[0][3])

    def get_music_playlists(self, artist_id, type="curated", filter='28day', start_date=None, end_date=None):
        """
        :param type: curated (editorial), listener, personalized (algorithmic)
        :param filter: 1day | 7day | 28day | 1year | last5years | all | custom | sincelaunch
        :param start_date: yyyy-MM-dd -> No más de 366 días
        :param end_date: yyyy-MM-dd
        """
        path = "s4x-insights-api/v1/artist/{}/playlists/{}".format(artist_id, type)
        parameters = {
            "time-filter": filter
        }
        if start_date and end_date:
            parameters["time-filter"] = "custom"
            parameters["start-date"] = start_date
            parameters["end-date"] = end_date

        path = path + "?{}".format(urlencode(parameters))
        url = "{}/{}".format(self.url, path)

        print(url)
        return self.__make_request__(url, inspect.stack()[0][3])

    def get_music_upcoming(self, artist_id):
        path = "upcoming-view-service/v1/artist/{}/catalog".format(artist_id)
        url = "{}/{}".format(self.url, path)
        return json.loads(self.__make_request__(url, inspect.stack()[0][3]))

    def get_music_song_canvas(self, artist_id, song_id):
        path = "canvaz-view/v1/artist/{}/canvas?uris=spotify:track:{}".format(artist_id, song_id)
        url = "{}/{}".format(self.url, path)
        return self.__make_request__(url, inspect.stack()[0][3])


    def get_music_song_streams(self, artist_id, song_id, field="graph", type='recording', filter='28day'):
        """
        :param field: graph, summary, source
        :param type: recording, ... ?
        :param filter: 7day | 28day | 1year
        """
        fields = {
            'graph': 'timeline/streams',
            'summary': 'summary-table',
            'source': 'source',
            'country': 'locations/streams',
            'city': 'top-cities/streams',
            'streams': 'realtime',
            'canonical': 'canonical',
            'top-playlists': 'top-playlists',
            'recent-playlists': 'recent-playlists'
        }
        path = "s4x-insights-api/v1/artist/{}/recording/{}/{}".format(artist_id, song_id, fields[field])

        if field == "recent-playlists":
            filter = '7day'

        parameters = {
            "aggregation-level": type,
            "time-filter": filter
        }

        path = path + "?{}".format(urlencode(parameters))
        url = "{}/{}".format(self.url, path)
        
        data = self.__make_request__(url, inspect.stack()[0][3])
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            pass
        return data

    def get_audience(self, artist_id, field="listeners", filter='28day', type='recording'):
        """

        :param artist_id: se puede incluir cualquier artista de Spotify (pensado para hacer comparaciones)
        :param field:
        :param filter:
        :param type:
        :return:
        """
        fields = {
            'listeners': 'timeline/listeners',
            'streams': 'timeline/streams',
            'followers': 'timeline/followers',
            'source': 'source',
            'gender': 'gender',
            'age': 'gender-by-age',
            'country': 'locations',
            'city': 'top-cities',
        }
        path = "s4x-insights-api/v1/artist/{}/audience/{}/{}".format(artist_id, fields[field], artist_id)
        parameters = {
            "aggregation-level": type,
            "time-filter": filter
        }
        path = path + "?{}".format(urlencode(parameters))
        url = "{}/{}".format(self.url, path)
        return self.__make_request__(url, inspect.stack()[0][3])

    def get_related_artists(self, artist_id):
        path = "artists/{}/related-artists".format(artist_id)
        url = "{}/{}".format(url, path)
        return self.__make_request__(self.public_url, inspect.stack()[0][3])

    def get_artist_playlists(self, artist_id):
        """
        NOT WORKING
        :param artist_id:
        :return:
        """
        url = "https://api-partner.spotify.com"
        parameters = {
            "operationName": "queryArtistOverview",
            "variables": {
               "uri": "spotify:artist:{}".format(artist_id)
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "8510bfcfef59a8e59e6ae336b7bf2202cb3154c3b09e397976135e132105d68e"
                }
            }
        }
        path = "pathfinder/v1/query"
        path = path + "?{}".format(urlencode(parameters).replace("%27", "%22").replace("+", ""))
        url = "{}/{}".format(url, path)
        print(url)
        return self.__make_request__(url, inspect.stack()[0][3])


    def get_profile(self, artist_id):
        fields = [
            "artistUri",
            "autobiography",
            "avatar",
            "biography",
            "concertsMetadata",
            "fallbackHeader",
            "gallery",
            "header",
            "isVerified",
            "mergedUserUri",
            "monthlyListeners",
            "name",
            "newRelease",
            "pinnedItem",
            "playlists",
            "relatedArtists",
            "releases",
            "topTracks",
            "isEditable",
            "fanFunding"
        ]
        parameters = {
            "fields": ','.join(fields),
            "application": "s4a",
            "imgSize": "large"
        }
        path = "artist-identity-view/v2/profile/{}".format(artist_id)
        path = path + "?{}".format(urlencode(parameters))
        url = "{}/{}".format(self.url, path)
        return self.__make_request__(url, inspect.stack()[0][3])


def get_api(username=None, password=None):
    sfa_api = None
    if not check_session():
        print("No hay tokens, auth con user/pass")
        
        if username and password:
            sfa_api = SpotifyForArtistsAPI(
                username=username,
                password=password
            )
            session["login_cookies"] = sfa_api.auth.login_cookies
        else:
            raise SpotifyForArtistsAPI.Auth.NoLoginData("Debes ingresar username y password para hacer login")
    else:
        if session["token"]:
            try:
                sfa_api = SpotifyForArtistsAPI(
                    token=session["token"],
                    refresh_token=session["refresh_token"],
                    expires=session["expires"],
                    web_client_token=session["web_client_token"]
                )
                print("Iniciando con token")
            except SpotifyForArtistsAPI.Auth.RefreshTokenRevoked as e:
                sfa_api = SpotifyForArtistsAPI(
                    login_cookies=session["login_cookies"]
                )
                print("Iniciando con cookie")
        elif session["login_cookies"]:
            sfa_api = SpotifyForArtistsAPI(
                login_cookies=session["login_cookies"]
            )
            print("Iniciando con cookie")
        me = sfa_api.get_me()

        if username and password and username != me["username"] and username != me["loginEmail"]:
            print("Cambiando de usuario")
            sfa_api = SpotifyForArtistsAPI(
                username=username,
                password=password
            )
        elif not username and not password:
            print("Hay tokens")

    session["token"] = sfa_api.auth.token
    session["refresh_token"] = sfa_api.auth.refresh_tkn
    session["expires"] = sfa_api.auth.expires
    session["web_client_token"] = sfa_api.auth.web_client_token
    
    return sfa_api

def check_auth():
    try:
        return get_api()
    except SpotifyForArtistsAPI.Auth.NoLoginData as e:
        return None

@app.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    username = request.json["username"]
    password = request.json["password"]
    try:
        sfa_api = get_api(username, password)
        me = sfa_api.get_me()
        return utils.handle_success(me)
    except SplinterException as e:
        return utils.handle_500(e.text)
    except LoginError as e:
        return utils.handle_400(str(e))

@app.route('/me')
def get_me():
    sfa_api = check_auth()
    if sfa_api:
        try:
            return utils.handle_success(sfa_api.get_me())
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")

@app.route('/initial')
def get_initial():
    sfa_api = check_auth()
    if sfa_api:
        try:
            return utils.handle_success(sfa_api.get_initial())
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")


@app.route('/artists')
def get_artists():
    sfa_api = check_auth()
    if sfa_api:
        try:
            return utils.handle_success(sfa_api.get_artists())
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")


@app.route('/manage-team')
@cross_origin(supports_credentials=True)
def get_manage_team():
    sfa_api = check_auth()
    if sfa_api:
        try:
            return utils.handle_success(sfa_api.get_manage_team())
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")


@app.route('/settings')
def get_settings():
    sfa_api = check_auth()
    if sfa_api:
        try:
            return utils.handle_success(sfa_api.get_settings())
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")

@app.route('/permissions')
def get_permissions():
    sfa_api = check_auth()
    artist_id = request.args.get('id')
    if sfa_api:
        try:
            if sfa_api.check_spotify_id(artist_id):
                return utils.handle_success(sfa_api.get_permissions(artist_id))
            else:
                return utils.handle_400("Parámetro id debe contener un ID de artista válido")
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")


@app.route('/home')
@cross_origin(supports_credentials=True)
def get_home():
    sfa_api = check_auth()
    artist_id = request.args.get('id')
    if sfa_api:
        try:
            if sfa_api.check_spotify_id(artist_id):
                return utils.handle_success(sfa_api.get_home(artist_id))
            else:
                return utils.handle_400("Parámetro id debe contener un ID de artista válido")
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")

@app.route('/artist/public')
@cross_origin(supports_credentials=True)
def get_artist_public():
    sfa_api = check_auth()
    artist_id = request.args.get('id')
    if sfa_api:
        try:
            if sfa_api.check_spotify_id(artist_id):
                return utils.handle_success(sfa_api.get_artist_public(artist_id))
            else:
                return utils.handle_400("Parámetro id debe contener un ID de artista válido")
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")

@app.route('/roster-view')
@cross_origin(supports_credentials=True)
def get_roster_view():
    sfa_api = check_auth()
    if sfa_api:
        try:
            return utils.handle_success(sfa_api.get_roster_view())
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")

@app.route('/pitch')
def get_pitch():
    sfa_api = check_auth()
    artist_id = request.args.get('id')
    album_id = request.args.get('album')
    if sfa_api:
        try:
            if sfa_api.check_spotify_id(artist_id):
                if sfa_api.check_spotify_id(album_id):
                    data = sfa_api.get_pitch(artist_id, album_id)
                    if data:
                        return utils.handle_success(data)
                    return utils.handle_404("No encontrado")
                else:
                    return utils.handle_400("Parámetro album debe contener un ID de album válido")
            else:
                return utils.handle_400("Parámetro id debe contener un ID de artista válido")
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")
        

@app.route('/music/songs')
@cross_origin(supports_credentials=True)
def get_songs():
    sfa_api = check_auth()
    artist_id = request.args.get('id')
    song_filter = 'last5years'
    if 'filter' in request.args.items():
        song_filter = request.args.get('filter')
    if sfa_api:
        try:
            if sfa_api.check_spotify_id(artist_id):
                return utils.handle_success(sfa_api.get_music_songs(artist_id, filter='last5years'))
            else:
                return utils.handle_400("Parámetro id debe contener un ID de artista válido")
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")

@app.route('/music/releases')
def get_releases():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    # ToDo: Filter
    return sfa_api.get_music_releases(artist_id, start_date='2021-01-01', end_date='2020-01-01')


@app.route('/music/playlists')
def get_playlists():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    # ToDo: Filter
    return sfa_api.get_music_playlists(artist_id, filter='sincelaunch')

@app.route('/music/upcoming')
def get_upcoming():
    sfa_api = check_auth()
    artist_id = request.args.get('id')
    if sfa_api:
        try:
            if sfa_api.check_spotify_id(artist_id):
                return utils.handle_success(sfa_api.get_music_upcoming(artist_id))
            else:
                return utils.handle_400("Parámetro id debe contener un ID de artista válido")
        except SpotifyForArtistsAPI.Auth.NoAccess as e:
            return utils.handle_401(str(e))
    else:
        return utils.handle_401("Inicia sesión para acceder a esta información")

@app.route('/song/canvas')
def get_song_canvas():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    song_id = request.args.get('song')
    # ToDo: Filter
    return sfa_api.get_music_song_canvas(artist_id, song_id)


@app.route('/song')
@cross_origin(supports_credentials=True)
def get_song_streams():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    song_id = request.args.get('song')
    field = request.args.get('field')
    # ToDo: Filter
    return utils.handle_success(sfa_api.get_music_song_streams(artist_id, song_id, field, filter='28day'))


@app.route('/song/public')
@cross_origin(supports_credentials=True)
def get_song_public():
    sfa_api = get_api()
    song_id = request.args.get('id')
    # ToDo: Filter
    return utils.handle_success(sfa_api.get_song_public(song_id))


@app.route('/song/public/credits')
@cross_origin(supports_credentials=True)
def get_song_credits_public():
    sfa_api = get_api()
    song_id = request.args.get('id')
    # ToDo: Filter
    return utils.handle_success(sfa_api.get_song_credits_public(song_id))


@app.route('/song/public/lyrics')
@cross_origin(supports_credentials=True)
def get_song_lyrics_public():
    sfa_api = get_api()
    song_id = request.args.get('id')
    # ToDo: Filter
    return utils.handle_success(sfa_api.get_song_lyrics_public(song_id))


@app.route('/audience')
def get_audience():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    field = request.args.get('field')
    # ToDo: Filter
    return sfa_api.get_audience(artist_id, field, filter='28day')


@app.route('/related-artists')
def get_related_artists():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    # ToDo: Filter
    return sfa_api.get_related_artists(artist_id)


@app.route('/profile')
def get_profile():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    # ToDo: Filter
    return json.loads(sfa_api.get_profile(artist_id))

@app.route('/profile/playlists')
def get_artist_playlists():
    sfa_api = get_api()
    artist_id = request.args.get('id')
    # ToDo: Filter
    return json.loads(sfa_api.get_artist_playlists(artist_id))

@app.route('/users/register', methods = ['POST'])
def register_user():
    data = request.get_json()
    if "username" in data.keys() and "password" in data.keys():
        existing_user = User.query.filter_by(username=data["username"])
        if not existing_user:
            hashed_password = generate_password_hash(data["password"], method='sha256')
            user = User(username=data["username"], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return utils.handle_success(user.to_dict())
        else:
            return utils.handle_409("User already exists")
    else:
        return utils.handle_400("You must provide an username and a password")

@app.route('/youtube')
@cross_origin(supports_credentials=True)
def youtube_video():
    sfa_api = get_api()
    song_id = request.args.get('id')
    song_data = sfa_api.get_song_public(song_id)
    
    from youtubesearchpython import VideosSearch
    videosSearch = VideosSearch("{} {}".format(song_data["name"], " ".join(list(artist["name"] for artist in song_data["album"]["artists"]))), limit = 2)

    from youtube_transcript_api import YouTubeTranscriptApi

    data = YouTubeTranscriptApi.get_transcript(videosSearch.result()["result"][0]["id"])
    return(data)


"""
@app.route('/users/delete', methods = ['DELETE'])
def delete_user():
    data = request.get_json()
    # ToDo: Filter
    return 
"""

def check_session():
    # Is auth
    print(session)
    if "token" in session and "refresh_token" in session and "expires" in session:
        if session["token"] and session["refresh_token"] and session["expires"]:
            return True
    if 'login_cookies' in session:
        if session["login_cookies"]:
            return True
    return False
        

if __name__ == "__main__":
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
