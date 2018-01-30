"""
Grab track names off of user's Discover Weekly Playlist.
Save names into a text file to be called by download.py.
"""

import sys, os
import spotipy
import spotipy.util as util

def show_tracks(results):
		for i, item in enumerate(results['items']):
			track = item['track']
			print "%32.32s %s" % (track['artists'][0]['name'], track['name'])
			outfile.write((track['artists'][0]['name']).encode('utf-8'))
			outfile.write(' ')
			outfile.write((track['name']).encode('utf-8'))
			outfile.write('\n')

def main():
	if len(sys.argv)<2:
		print 'Usage: python spotify.py username'
		sys.exit(0)

	username = sys.argv[1]
	token = util.prompt_for_user_token(username)

	if token:
		sp = spotipy.Spotify(auth=token)
		playlists = sp.user_playlists(username)
		for playlist in playlists['items']:
			if playlist['owner']['id'] == username:
				global outfile
				playlist_name = str(playlist['name'])
				if not os.path.exists(playlist_name):
                    			os.makedirs(playlist_name)
				outfile = open(os.path.join(('./' + playlist_name), (playlist_name + '.txt')), 'w')
				results = sp.user_playlist(username, playlist['id'], fields='tracks,next')
				tracks = results['tracks']
				show_tracks(tracks)
				while tracks['next']:
					tracks = sp.next(tracks)
					show_tracks(tracks)
				outfile.close()

	else:
		print "Can't get token for ", username


if __name__ == '__main__':
	main()

