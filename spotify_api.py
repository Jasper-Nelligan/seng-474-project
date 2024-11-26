import requests
import base64
import time

access_token = None
token_expires_at = None

def get_spotify_access_token(client_id, client_secret):
    global access_token, token_expires_at

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    access_token = response_data['access_token']
    token_expires_at = response_data['expires_in'] + int(time.time())

    return access_token

def get_track_id(artist, track, album):
    query = f'artist:"{artist}" track:"{track}" album:"{album}"'
    url = f'https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit=1'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        raise Exception("Rate limited by Spotify API")

    try:
        response_data = response.json()
        items = response_data['tracks']['items']
        if items:
            return items[0]['id']
        else:
            return None
    except ValueError:
        return None
    except KeyError:
        return None

def get_multiple_track_features(track_ids):
    url = f'https://api.spotify.com/v1/audio-features/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'ids': ','.join(track_ids)
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 429:
        print("Rate limited by Spotify API")
        retry_after = response.headers.get('Retry-After')
        print(f"Rate limited by Spotify API. Retry after {retry_after} seconds.")
        raise Exception("Rate limited by Spotify API")
    
    try:
        response_data = response.json()
        if 'error' in response_data:
            print(f"Error in response: {response_data['error']}")
            return None
        elif not response_data:
            print("No response data")
            return None
        return response_data.get('audio_features', [])
    except ValueError:
        print("Error: Response is not in JSON format")
        return None