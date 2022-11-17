# LyricGrabber v1.0 for Project Diva MegaMix+
# © 2022 Seán, testsnake
#
# For support, check out
# https://discord.gg/hisokeee

import requests
import pandas as pd
import sys

# Set Lyric Type
# 0 = jp/ro for standard game usage
# 1 = jp/en/ro for usage with Eden Project or English Lyrics
# More types may be added in the future
lyricType = 1

print("---Lyric Grabber---")
print("© 2022 Seán, testsnake\n")

pvNumber = input("input pv number\n> ")

# If the PV number starts with 'r', it will only write romaji and japanese to the output
if pvNumber == "r":
	lyricType = 0
elif pvNumber == "e":
	lyricType = 1


# Loads URL
try:
	url = input("input the url\n> ")
	html = requests.get(url).content
except Exception as e:
	print(e)
	print("Could not read URL")
	input("Press enter to close")
	sys.exit()

# Looks for an HTML table with the English
try:
	df_list = pd.read_html(html, 'English')
except:
	print("No English HTML table found, looking for another table")

	# If no english table is found, it looks for other tables
	# Ignore this giant list of awful code pls 
	# I wanted to make it work better for random users -testsnake
	try:
		df_list = pd.read_html(html, 'Romaji')
	except:
		print("No Romaji HTML table found, looking for another table")
		df_list = pd.read_html(html, 'Japanese')
		try:
			df_list = pd.read_html(html, 'Tagalog')
		except:
			print("No Tagalog HTML table found, looking for another table")
			try:
				df_list = pd.read_html(html, 'Korean')
			except:
				try:
					df_list = pd.read_html(html, 'Chinese')
				except:
					try:
						df_list = pd.read_html(html, 'Spanish')
					except:
						try:
							df_list = pd.read_html(html, 'Russian')
						except:
							try:
								df_list = pd.read_html(html, 'French')
							except:
								try:
									df_list = pd.read_html(html, 'Vietnamese')
								except:
									print("No lyrics found\nContact testsnake#6663 on discord for more info")
									# Crashes the program because haha funi
									input("Press enter to close")
									sys.exit()



df = df_list[-1]
out_file = "pv_" + pvNumber + '_lyrics.txt'

output = []

# Parses Lyrics into something the game can read
def lyric_parse(lyrics,lang='.'):
	lyrics = lyrics.drop(0)
	lyrics = lyrics.dropna().reset_index(drop=True)

	for row_index in range(len(lyrics)):
		lyric = lyrics[row_index]
		index_str = str(row_index + 1).zfill(3)
		line = f'pv_{pvNumber}.lyric{lang}{index_str}={lyric}\n'
		print(line)
		output.append(line)
	

# Lyric type 0
# Japanese lyrics -> lyrics
# Romaji Lyrics -> lyrics_en
if lyricType == 0:
	lyric_parse(df[0])
	lyric_parse(df[1], '_en.')

# Lyric type 1
# Japanese lyrics -> lyrics
# English Lyrics -> lyrics_en
# Romaji Lyrics -> lyrics_ro
elif lyricType == 1:
	lyric_parse(df[0])
	lyric_parse(df[2], '_en.')
	lyric_parse(df[1], '_ro.')

# Writes to file
try:
	with open(out_file, 'w', encoding='utf-8') as f:
			f.writelines(output)

# Error Handling
except PermissionError as e:
	print(e)
	print("\n\nCould got get permissions to write file, move to another directory")
	input("\nPress Enter to close")
except Exception as e:
	print(e)
	print("\n\nUnknown error")
	input("\nPress Enter to close")
