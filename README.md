# Spotify Visualizer

Spotify currently does not have a visualizer, so I plan to try and create an integration. <br/>
Also wrote scripts to grab songs from a user's Discover Weekly playlist, download them, and play them with the visualizer. <br/>
Couldn't figure out how to get the visualizer to work off the mp3 files instead of the speakers, but plan to do so in the future.

## Technologies
- Spotipy
- BeautifulSoup
- PyQtGraph
- Numpy 
- OpenSimplex
- Pyaudio
- Playsound
- Youtube API

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
- Run playlist script and authenticate 
	- `python get_spotify_playlist.py 'username'`
- Run the download script with discover_weekly.txt
	- `python get_youtube_downloads.py -f discover_weekly.txt`
- Run the visualizer and audio
	- `./runVisualizer.sh`
	
## Future ideas
- Visualizer gets input from the microphone audio
	- Eventually want to come back and have it use the Mp3 files directly
- Make a GUI for the app
- Pygame was giving errors playing the Mp3 files but I'd like to figure out why and switch back to it from Playsound
	- Pygame is more heavily used and supported
