import pygame


class SoundFuncs:
    def playSound(path):
        pygame.mixer.init()
        pygame.mixer.music.load(path) #loads sound from path given
        pygame.mixer.music.play() #plays sound