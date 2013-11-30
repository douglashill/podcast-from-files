#!/usr/bin/python
# coding: utf-8

import sys
import os
import urllib
import time
import subprocess

feed_title = 'My Videos'
feed_description = ''
root_url = 'http://mac.local/~douglas/videos/'
root_path = '/Users/Douglas/Sites/videos'
media_dir = 'media'
duration_executable = '/Users/Douglas/Development/Local files podcast/durationmetadata'
feed_image_url = 'http://mac.local/~douglas/videos/cover.png'
feed_filename = 'feed.xml'



def split_title(title):
	separators = [' - ', '—', ',', ': ']
	index = 10000
	chosen_separator = None
	
	for separator in separators:
		if title.find(separator) < index and title.find(separator) != -1:
			index = title.find(separator)
			chosen_separator = separator
	
	components = []
	if chosen_separator:
		for component in title.split(chosen_separator, 1):
			components.append(component.strip())
	else:
		components.append(title.strip())
		components.append('')
	
	return components



xml = []

xml.append('<?xml version="1.0" encoding="UTF-8"?>\n<rss xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">\n<channel>\n  <title>')
xml.append(feed_title)
xml.append('</title>\n  <link>')
xml.append(root_url)
xml.append('</link>\n  <description>')
xml.append(feed_description)
xml.append('</description>\n  <itunes:image href="')
xml.append(feed_image_url)
xml.append('" />\n  <atom10:link xmlns:atom10="http://www.w3.org/2005/Atom" rel="self" type="application/rss+xml" href="http://mac.local/~douglas/videos/feed.xml" />\n')

video_files = []
media_dir_path = os.path.join(root_path, media_dir)

for filename in os.listdir(media_dir_path):
	file_path = os.path.join(media_dir_path, filename)
	
	(basename, extension) = os.path.splitext(filename)
	if extension == '.mov' or extension == '.m4v' or extension == '.mp4' or extension == '.mp3' or extension == '.m4a':
		video_files.append(file_path)

for file_path in video_files:
	(path, filename) = os.path.split(file_path)
	(basename, extension) = os.path.splitext(filename)
	(main_title, subtitle) = split_title(basename)
	video_url = os.path.join(root_url, media_dir, urllib.quote(filename))
	
	xml.append('  <item>\n    <title>')
	xml.append(main_title)
	xml.append('</title>\n    <description>')
	xml.append(subtitle)
	xml.append('</description>\n    <guid>')
	xml.append(video_url)
	xml.append('</guid>\n    <pubDate>')
	xml.append(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(os.path.getmtime(file_path))))
	xml.append('</pubDate>\n')
	
	xml.append('    <enclosure url="')
	xml.append(video_url)
	xml.append('" length="')
	xml.append(str(os.path.getsize(file_path)))
	xml.append('" type="')
	if extension == '.mov': xml.append('video/quicktime')
	if extension == '.m4v': xml.append('video/x-m4v')
	if extension == '.mp4': xml.append('video/mp4')
	if extension == '.mp3': xml.append('audio/mpeg')
	if extension == '.m4a': xml.append('audio/x-m4a')
	xml.append('" />\n')
	
	if duration_executable:
		xml.append('    <itunes:duration>')
		xml.append(subprocess.check_output([duration_executable, file_path]).strip())
		xml.append('</itunes:duration>\n')
	
	xml.append('  </item>\n')

xml.append('</channel></rss>')

xml_string = ''.join(xml)

feed_file = os.path.join(root_path, feed_filename)

with open(feed_file, 'w') as f:
	f.write(xml_string)