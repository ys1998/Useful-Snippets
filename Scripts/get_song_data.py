import pygn
import json
import os, sys
import eyed3, urllib

clientID = '1739074923-AA8FA8E67DC076CEDF3EC013DBDC0258'
userID = '48232577353955164-7F4EBAB4ED21890DE93F7F658B1375EC'

for root, _, files in os.walk(sys.argv[1]):
	artist = os.path.split(root)[1]
	for f in files:
		if f.endswith('.mp3') or f.endswith('.MP3'):
			track = os.path.splitext(f)[0].replace('_', ' ')
			audioFile = eyed3.load(os.path.join(root,f))
			metadata=pygn.search(clientID=clientID, userID=userID, artist=artist, track=track)
			
			print("Title :", metadata['track_title'])
			print("Artist :", metadata['album_artist_name'])
			print("Album :", metadata['album_title'])
			print("Genre :", ', '.join([x['TEXT'] for _,x in metadata['genre'].items()]))
			print("Year :", metadata['album_year'])
			print("Album art :", metadata['album_art_url'])
			
			audioFile.tag.title = str(metadata['track_title'])
			audioFile.tag.artist = str(metadata['album_artist_name'])
			audioFile.tag.genre = str(', '.join([x['TEXT'] for _,x in metadata['genre'].items()]))
			audioFile.tag.year = str(metadata['album_year'])
			audioFile.tag.album = str(metadata['album_title'])

			if metadata['album_art_url'] != '':
				res = urllib.request.urlopen(metadata['album_art_url'])
				img = res.read()

				audioFile.tag.images.set(3, img, 'image/jpeg', u"%s"%str(metadata['album_title']))

			audioFile.tag.save(version=(1, None, None))
			audioFile.tag.save(version=(2,3,0))
			audioFile.tag.save()
			print('\n')