import sys
import os 
import numpy as np
import soundfile as sf
import math
import random
from optparse import OptionParser

def check_snr(min, clean):
    noise_power = np.sum((mix - clean) ** 2)
    clean_power = np.sum(clean ** 2)
    snr = 10 * math.log10(clean_power / (noise_power + 1e-8))
    return snr

def generate_noisy(noise_file, wav_file, snr, if_norm=False, avoid_clipping=True, random_index=True):
    speech, sfs = sf.read(wav_file)
    noise, nfs = sf.read(noise_file)
    assert sfs == nfs
    if if_norm:
        speech = speech / np.sqrt(np.sum(speech ** 2) + 1e-8) * 100
        noise = noise / np.sqrt(np.sum(noise ** 2) + 1e-8) * 100
        s_len = len(speech)
        n_len = len(noise)
        if s_len <= n_len:
            if random_index and n_len > s_len + 1:
                random_index = random.randint(0, n_len -s_len -1)
                noise = noise[random_index: random_index + s_len]
            else:
                noise = noise[:s_len]
        else:
            num_repeat = s_len // n_len
            res = s_len - num_repeat * n_len
            noise = np.concatenate([np.concatenate([noise] * num_repeat), noise[:res]])
        speech_power = np.sum(speech ** 2)
        noise = noise / np.sqrt(np.sum(noise ** 2) + 1e-8) * np.sqrt(speech_power + 1e-8)
        noise = noise / np.power(10,snr / 20.)
        noisy = speech + noise
        if avoid_clipping:
            max_scale = max(np.max(np.abs(speech)), np.max(np.abs(noise)),np.max(np.abs(noisy)))
            noisy = noisy / max_scale * 0.9
            speech = speech / max_scale * 0.9
            noise = noise / max_scale * 0.9
        return noisy, speech, noise

if __name__ == '__main__':
    usage = 'python %prog wav_scp noise_file snr_min snr_max out_dir'
    parser = OptionParser(usage=usage)
    (options, args) = parser.parser_args()
    if len(args) !=5:
        print(usage)
        sys.exit()
    wav_scp = args[0]
    noise_file = args[1]
    snr_min = args[2]
    snr_max = args[3]
    out_wav_dir = args[4]

    with open(wav_scp) as f:
        wav_scp_lst = f.read().splitlines()
    with open(noise_file) as f:
        noise_lst = f.read().splitlines()
    
    r = np.random.randint(0, len(noise_lst), size=len(wav_scp_lst))
    for i,wav_file in enumerate(wav_scp_lst):
        speech_file = wav_file.split()[1]
        noise_file = noise_lst[r[i]]
        snr = np.random.randint(snr_min, snr_max+1)
        mix, clean, _ = generate_noisy(noise_file, speech_file, snr)
        out_file = out_wav_dir + '/' + speech_file.split('/')[-1] + '_an_snr{}.wav'.format(snr)
        sf.write(out_file, mix, 16000)
