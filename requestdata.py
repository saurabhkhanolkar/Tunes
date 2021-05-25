import pandas as pd
import requests
import json 
from pandas.io.json import json_normalize 
import base64 


spotify_ids=pd.DataFrame(['859d1825fc2b4fcab7269fdface7e8ff' , '725966bfe74344eb9554f9529fdc9f24'])


# Defining base64 encoding of the IDs
def base64_encode(client_id,client_secret):
    encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    authorization_header_string = f"{encodedData}"
    return(authorization_header_string)
    
def accesstoken(client_id, client_secret):
    header_string= base64_encode(client_id,client_secret)
    headers = {
        'Authorization': 'Basic '+header_string,
    }
    
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    access_token = json.loads(response.text)
    access_token = access_token['access_token']
    return(access_token)
    
access_token = accesstoken(str(spotify_ids[0][0]),str(spotify_ids[0][1]))

def get_album(album_id,ns):
    headers = {
        'Authorization': 'Bearer '+access_token,
    }
    album_response = requests.get('https://api.spotify.com/v1/albums/'+album_id+'/tracks?limit='+ns, headers=headers)
    
    album_response = json.loads(album_response.text)
    album_response = album_response['items']
    album_response = pd.DataFrame.from_dict(json_normalize(album_response), orient='columns')
    return(album_response)

def get_albums_tracks(playlist_df):
    
    track_ids = list(playlist_df['id'])
    track_ids = ','.join(track_ids)
    
    headers = {
        'Authorization': 'Bearer '+access_token,
    }
    track_response = requests.get('https://api.spotify.com/v1/audio-features/?ids='+track_ids, headers=headers)
    track_response = json.loads(track_response.text)
    track_response = track_response['audio_features']
    track_response = pd.DataFrame.from_dict(json_normalize(track_response), orient='columns')
    
    playlist_df = pd.merge(playlist_df, track_response, left_on='id', right_on='id', how='inner')
    return(playlist_df)
    
    
def get_playlist(playlist_id,ns):
    headers = {
        'Authorization': 'Bearer '+access_token,
    }
    playlist_response = requests.get('https://api.spotify.com/v1/playlists/'+playlist_id+'/tracks?limit='+ns, headers=headers)
    
    playlist_response = json.loads(playlist_response.text)
    playlist_response = playlist_response['items']
    playlist_response = pd.DataFrame.from_dict(json_normalize(playlist_response), orient='columns')
    return(playlist_response)
    
    
    
def get_playlists_tracks(playlist_df):
    
    track_ids = list(playlist_df['track.id'])
    track_ids = ','.join(track_ids)
    
    headers = {
        'Authorization': 'Bearer '+access_token,
    }
    track_response = requests.get('https://api.spotify.com/v1/audio-features/?ids='+track_ids, headers=headers)
    track_response = json.loads(track_response.text)
    track_response = track_response['audio_features']
    track_response = pd.DataFrame.from_dict(json_normalize(track_response), orient='columns')
    
    playlist_df = pd.merge(playlist_df, track_response, left_on='track.id', right_on='id', how='inner')
    return(playlist_df)


#pora_id = input('Enter Album ID')
def pora_idalbum(pora_id):
    pora_id = str(pora_id)
    myplaylist_df = get_album(pora_id,"1")
    myplaylist_df = get_albums_tracks(myplaylist_df)
    myplaylist_df.rename(columns = {'duration_ms_x':'duration_ms'}, inplace = True)
    final=myplaylist_df[['acousticness','danceability','duration_ms','energy','instrumentalness','liveness','loudness','speechiness','tempo','valence']]
    return(final)
    
    
def pora_idplaylist(pora_id):
    pora_id = str(pora_id)
    myplaylist_df = get_playlist(pora_id,"1")
    myplaylist_df = get_playlists_tracks(myplaylist_df)
    myplaylist_df.rename(columns = {'duration_ms_x':'duration_ms'}, inplace = True)
    final=myplaylist_df[['acousticness','danceability','duration_ms','energy','instrumentalness','liveness','loudness','speechiness','tempo','valence']]
    return(final)
