import urllib.parse as urlparse
from urllib.parse import parse_qs

# Replace a standard youtube url. i.e: https://www.youtube.com/watch?v=dQw4w9WgXcQ
# to: https://www.youtube.com/embed/dQw4w9WgXcQ
def change_url(old_url):
	parsed = urlparse.urlparse(old_url)
	video_id = parse_qs(parsed.query)
	if 'v' in video_id:
		return 'https://www.youtube.com/embed/{}'.format(video_id['v'][0])
	else:
		return old_url