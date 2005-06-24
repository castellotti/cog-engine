import pygame
import pygame.mixer

pygame.init()

pygame.mixer.init()

#pygame.mixer.music.load('output.wav')
pygame.mixer.music.load('/tmp/cogengine_outputtext.wav')

pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
	pass

pygame.mixer.quit()
