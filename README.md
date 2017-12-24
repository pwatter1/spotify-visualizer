# Spotify Visualizer

Spotify currently does not have a visualizer, so I plan to try and create one. <br/>
Also wrote scripts to grab songs from a user's Discover Weekly playlist, download them, and play them with the visualizer.

## Technologies
- Spotipy
- BeautifulSoup
- PyQtGraph
- Numpy 
- OpenSimplex
- Pyaudio

## How to run
- Clone the repo `git clone https://github.com/pwatter1/spotify-visualizer.git && cd spotify-visualizer`
- Install the dependencies
	- `pip install spotipy`

	- `pip install beautifulsoup4`

	- `pip install --upgrade google-api-python-client`

	- `pip install requests`

- Run the spotify credentials script in the terminal
	- `source spotifyCredentialsExport.sh`
	- Use source so it runs in the current process and not the child or else no effect
- Run spotify.py and authenticate 
	- `python get_spotify_playlist.py 'username'`
- Run the download script with discover_weekly.txt
	- `python get_youtube_downloads.py -f discover_weekly.txt`
- Run the visualizer
	- `python visualizer.py`
