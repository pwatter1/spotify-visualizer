"""
Grab track names off of user's Discover Weekly Playlist.
Save names into a text file to be called by download.py.
"""

import sys
import spotipy
import spotipy.util as util

def show_tracks(results):
		for i, item in enumerate(results['items']):
			track = item['track']
			print "%32.32s %s" % (track['artists'][0]['name'], track['name'])
			f.write((track['artists'][0]['name']).encode('utf-8'))
			f.write(' ')
			f.write((track['name']).encode('utf-8'))
			f.write('\n')

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
				global f
				f = open(str(playlist['name']+'.txt'), 'w')
				results = sp.user_playlist(username, playlist['id'], fields='tracks,next')
				tracks = results['tracks']
				show_tracks(tracks)
				while tracks['next']:
					tracks = sp.next(tracks)
					show_tracks(tracks)
				f.close()
	else:
		print "Can't get token for ", username


if __name__ == '__main__':
	main()

