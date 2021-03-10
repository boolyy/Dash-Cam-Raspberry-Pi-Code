# importing vlc module
import vlc
 
# creating vlc media player object
media = vlc.MediaPlayer("Videos\Clock_Face_2Videvo.mov")
 
# start playing video
media.play()

while True:
    pass