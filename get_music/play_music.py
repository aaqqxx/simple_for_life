# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import pygame

pygame.mixer.init()
# print("播放音乐1")
# track = pygame.mixer.music.load("tkzc.wav")
# pygame.mixer.music.play()

# print("播放音乐2")
# track1=pygame.mixer.music.load(ur"f:\kafei.mp3")
# pygame.mixer.music.play()

print("播放音乐3")
track2=pygame.mixer.Sound(r"f:\kafei.mp3")
track2.play()

