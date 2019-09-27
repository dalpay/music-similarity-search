import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyInterface:

    def __init__(self):
        
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.sp = sp

    def get_albums(self, num_items=10, num_tracks=50):
        
        new_releases = self.sp.new_releases(limit=num_items)
        new_albums = new_releases['albums']['items']
        
        track_data = []
        for album_item in new_albums:
            
            album_id = album_item['id']
            album = self.sp.album(album_id)
            tracks = album['tracks']['items']

            for track in tracks:
                
                track_id = track['id']
                new_track_data = self.process_track(track_id)
                track_data.append(new_track_data)

                if (len(track_data) >= num_tracks):
                    return track_data
                
        return track_data

    def get_playlists(self, num_items=10, num_tracks=50):

        featured_playlists = self.sp.featured_playlists(limit=num_items)
        new_playlists = featured_playlists['playlists']['items']
               
        track_data = []
        for playlist_item in new_playlists:

            playlist_id = playlist_item['id']
            playlist = self.sp.user_playlist_tracks(user=None, playlist_id=playlist_id)
            playlist_items = playlist['items']

            for item in playlist_items:

                track_id = item['track']['id']
                new_track_data = self.process_track(track_id)
                track_data.append(new_track_data)

                if (len(track_data) >= num_tracks):
                    return track_data

        return track_data

    def process_track(self, track_id):

        track_info = self.extract_track_info(track_id)
        track_feats = self.extract_track_features(track_id)
        track_data = {'id': track_id, **track_info, **track_feats}
        
        return track_data

    def extract_track_info(self, track_id):

        track = self.sp.track(track_id)
        track_name = track['name']
        track_year = track['album']['release_date'].split('-')[0]
        artist_name = track['artists'][0]['name']
        track_info = {'name': track_name, 'artist': artist_name, 'year': track_year}
        return track_info

    def extract_track_features(self, track_id):

        analysis = self.sp.audio_analysis(track_id)
        segments = analysis['segments']
        
        timbre = []*len(segments)
        chroma = []*len(segments)
        for segment in segments:

            timbre.append(segment['timbre'])
            chroma.append(segment['pitches'])

        track_features = {'timbre': timbre, 'chroma': chroma}
        return track_features


def main():

    si = SpotifyInterface()
    songs = si.get_playlists(num_items=1, num_tracks=1)
    # print(songs)
    print(len(songs))
    print(songs[0].keys())

if (__name__ == '__main__'):
    
    main()
