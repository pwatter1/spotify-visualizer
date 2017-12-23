import json, requests, argparse, subprocess
from bs4 import BeautifulSoup as bs
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY = 'AIzaSyBzSh1STNMh7fwFfWbQ_upJrYqRjomFEoY'

def youtube_search(options):
	"""
	Query Youtube and download result as mp3 file.
	"""
	youtube = build(YOUTUBE_API_SERVICE_NAME,
					YOUTUBE_API_VERSION,
					developerKey=DEVELOPER_KEY)
	
	search_response = youtube.search().list(
    	q=options.q,
    	part='id,snippet',
    	maxResults=options.max_results
  	).execute()

	videos = []
	video_ids = []
	video_names = [] 

	for search_result in search_response.get('items', []):
		if search_result['id']['kind'] == 'youtube#video':
			videos.append('%s (%s)' % (search_result['snippet']['title'], search_result['id']['videoId']))
			video_ids.append(search_result["id"]["videoId"])
			video_names.append(search_result["snippet"]["title"])
				
	if len(videos):
		print 'Videos:', '\n'.join(videos), '\n'
	else:
		print 'Error: Search returned nothing! Request must not have gone configured correctly.'
		return

	first_result = video_ids[0]
	link = 'http://convertmp3.io/download/?video=http://www.youtube.com/watch?v=%s' % first_result 
	request = requests.get(link)
	
	try:
		data = json.loads(request.text)
		download_link = data['link']
		print download_link

	except ValueError:
		soup = bs(request.text, "lxml")
		download_link = 'http://convertmp3.io%s' % soup.find(id='download')['href']	

	command = ['wget', '-c', '-q', '--show-progress', '--output-document=%s.mp3' % video_names[0], download_link]
	output = subprocess.call(command)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--q', help='Search term', default='Google')
	parser.add_argument('--f', help='Text file from Spotify API', default='')
	parser.add_argument('--max-results', help='Max results', default=1)
	args = parser.parse_args()
	
	try:
		if not args.f:
			youtube_search(args)
		else:
			with open(args.f, 'r') as infile:
				lines = infile.readlines()
			for line in lines:
				args.q = line
				youtube_search(args)

	except HttpError, e:
	    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)

