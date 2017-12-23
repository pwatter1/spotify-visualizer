import signal
import time
import os
import threading
import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

  def play(self) :
    """
    Just another name for self.start()
    """
    self.start()

  def stop(self) :
    """
    Stop playback. 
    """
    self.loop = False
    
    
class PlayerLoop(threading.Thread) :
  """
  A simple class based on PyAudio and pydub to play in a loop in the backgound
  """

  def __init__(self,filepath,loop=True) :
    """
    Initialize `PlayerLoop` class.
    PARAM:
        -- filepath (String) : File Path to wave file.
        -- loop (boolean)    : True if you want loop playback. 
                               False otherwise.
    """
    super(PlayerLoop, self).__init__()
    self.filepath = os.path.abspath(filepath)
    self.loop = loop

  def run(self):
    # Open an audio segment
    sound = AudioSegment.from_file(self.filepath)
    player = pyaudio.PyAudio()
    
    stream = player.open(format = player.get_format_from_width(sound.sample_width),
        channels = sound.channels,
        rate = sound.frame_rate,
        output = True)

    # PLAYBACK LOOP
    start = 0
    length = sound.duration_seconds
    volume = 100.0
    playchunk = sound[start*1000.0:(start+length)*1000.0] - (60 - (60 * (volume/100.0)))
    millisecondchunk = 50 / 1000.0
    
    
    while self.loop :
        self.time = start
        for chunks in make_chunks(playchunk, millisecondchunk*1000):
            self.time += millisecondchunk
            stream.write(chunks._data)
            if not self.loop:
                break
            if self.time >= start+length:
                break

    stream.close()
    player.terminate()


  def play(self) :
    """
    Just another name for self.start()
    """
    self.start()

  def stop(self) :
    """
    Stop playback. 
    """
    self.loop = False
    
    
def play_audio_background(audio_file):
    """
    Play audio file in the background, accept a SIGINT or SIGTERM to stop
    """
    killer = GracefulKiller()
    player = PlayerLoop(audio_file)
    player.play()
    print(os.getpid())
    while True:      
        time.sleep(0.5)
        # print("doing something in a loop ...")
        if killer.kill_now:
            break
    player.stop()
    print("End of the program. I was killed gracefully :)")
    return
        


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(add_help=True, description="Play a file continously, and exit gracefully on signal")
    parser.add_argument('audio_file', type=str, help='The Path to the audio file (mp3, wav and more supported)')
    args = parser.parse_args()
    
    play_audio_background(args.audio_file)
    
