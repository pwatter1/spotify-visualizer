import os, signal
import playsound

def play():
	"""
	Plays mp3 files from the DiscoverWeekly playlist.
	"""
	files = []
	file_index = 0
	
	for filename in os.listdir("./DiscoverWeekly"):
		if filename.endswith(".mp3"):
			files.append(filename)
	
	try:
		while file_index < len(files):
			playsound.playsound(files[file_index], True)
			file_index += 1
	
	except KeyboardInterrupt:
		sys.Exit(0)

if __name__ == '__main__':
	play()
