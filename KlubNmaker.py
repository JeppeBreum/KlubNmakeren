from pydub import AudioSegment
import subprocess
import os
import sys
import shutil


print("""
                         Velkommen til KlubNmakeren^TM.
            Læs README.txt før du fortsætter, og hav din playliste klar.

     """)


def change_names():
    i = 0
    path = "downloadedplaylist/"
    for filename in os.listdir(path):
        nyt_navn = path + "sang" + str(i).zfill(4) + ".mp3"
        gammelt_navn = path + filename
        os.rename(gammelt_navn, nyt_navn)
        i += 1

def combine_songs():
    path = 'downloadedplaylist/' 
    path_shoutouts = 'shoutouts/'
    combined_song = AudioSegment.empty()
    shoutout = AudioSegment.empty()
    sixty_secs = 60 * 1000
    j = 0
    for filename in os.listdir(path):
        
        shoutout_exists = os.path.exists((path_shoutouts + 'shoutout' + str(j).zfill(4)+'.mp3').strip())
        
        if shoutout_exists == True:
            print('Fil: shoutout'+str(j).zfill(4)+'.mp3'+' Fundet')
            shoutout = AudioSegment.from_file(((path_shoutouts + 'shoutout' + str(j).zfill(4)+'.mp3').strip()), format="mp4")
            combined_song = combined_song + shoutout
        
        print(str('Tilføjer: ' + filename))
        
        song = AudioSegment.from_mp3(str(path + filename))
        combined_song = combined_song + song[:sixty_secs]
        j += 1
    return combined_song, j

while True:
    
    README_done = input('Har du læst README.txt? (ja/nej):')
    
    if README_done not in ['ja', 'Ja', 'j']:
        break
    
    #subprocess.call(['mkdir downloadedplaylist'], shell = True)
    
    playlist_link = input('Skriv URL på din Soundcloud-playliste: ')
    
    print('Downloader sange, kan tage et par minutter...')
    
    subprocess.call(['youtube-dl.exe', '--extract-audio', '--audio-format', 'mp3', '-o', r'/downloadedplaylist/%(title)s.%(ext)s', playlist_link])
    
    print('Download færdig.')
    
    one_more = input('Flere playlister? (ja/nej): ')
    
    if one_more in ['nej', 'Nej', 'n']:
        break

if README_done not in ['ja', 'Ja', 'j']:
    sys.exit("Gør det først!")

print('Skifter navne på sange...')

change_names()

print('Sammensætter sange...')

A, j = combine_songs()

print('Gemmer sammensat sang som mp3...')

A.export("Klub-"+str(j)+".mp3", format="mp3")

print('Sletter sange...')

shutil.rmtree('downloadedplaylist')

print('Færdig!')