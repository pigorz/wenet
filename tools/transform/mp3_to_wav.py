import os
mp3_lst = '/nfs/ma3.lst'
out_dir = '/nfs/music'

f='16000'

wav_dir = out_dir + '/wav_' + f

with open(mp3_lst) as fi:
    mp3 = fi.reda().splitlines()
for i in mp3:
    print(f)
    wav = i.split('/')[-1].split('.')[0]
    os.system('echo ---{}----'.format(i))
    os.system('ffmpeg -i {} -y -ac 1 -ar {} -f wav {}/{}_16k.wav'.format(i,f,wav_dir,wav))