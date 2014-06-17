#coding:gbk
#!/usr/bin/env python

__author__ = 'SAF'
#!/usr/bin/env python



import time

import winsound

def play():

    print "播放声音"
    filename = ''

#winsound.PlaySound('SystemExit', winsound.SND_ALIAS)

    # winsound.PlaySound(r'C:\Users\SAF\Music\Music\windancer.mp3', winsound.SND_ALIAS) #立即返回，支持异步播放

    winsound.PlaySound(
    file,
    winsound.SND_FILENAME|winsound.SND_NOWAIT,
    )
    while(True):

        time.sleep(0.2)

        print "s",



if __name__ == '__main__':

    play()