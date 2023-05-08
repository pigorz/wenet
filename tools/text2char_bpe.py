# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import itertools
from optparse import OptionParser 
import json
import sentencepiece as spm 

not_in_lexicon = {}

def read_vocab(vocab_file): 
    lst = []
    with open(vocab_file) as f:
        ff = f.read().splitlines()
    for i in ff:
        lst.append(i.split()[0]) 
    return lst


def split_eng_chi(s):
    ss = ''
    pre_i = ''
    for i in s:
        if i.encode('utf-8').isalpha() or i == '\'':
            if pre_i in ['','\''] or pre_i.encode('utf-8').isalpha():
                ss = ss +i
            else: 
                ss = ss + ' ' + i
        else:
            ss = ss + ' ' + i 
        pre_i = i 
    print('yhxyhx')
    print(ss.split()) 
    return ss.split()




def main():
    usage = "python %prog trans_file(utf-8) vocab_file sentencepiece_model out_label_file(w)" 
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args) != 4:
        print(usage)
        sys.exit()
    trans_file = args[0]
    vocab_file = args[1]
    spm_model = args[2]
    out_label_file = args[3]

    vocab_lst = read_vocab(vocab_file)
    out_label = open(out_label_file, "w", encoding="utf-8")

    sp = spm.SentencePieceProcessor()
    sp.load(spm_model)

    with open(trans_file, "r", encoding="utf-8") as TRANS: 
        for line in TRANS.readlines():
            key, transcript = line.strip().split(" ", 1)
            out_trans = []
            for item in transcript.split(" "):
                item = item.lower()
                #item = item.upperO
                if item.replace("'","").replace('-','').encode('utf-8').isalpha():
                    out_pieces = sp.encode_as_pieces(item) 
                    out_pieces_str = ' '.join(out_pieces)
                    out_trans.append(out_pieces_str)
                else:
                    for char in split_eng_chi(item):
                        if char.replace("'","").replace('-','').encode('utf-8').isalpha():
                            out_pieces = sp.encode_as_pieces(char) 
                            out_pieces_str = ' '.join(out_pieces) 
                            out_trans.append(out_pieces_str) 
                        elif char in vocab_lst:
                            out_trans.append(char)
                        else:
                            out_trans.append('')
            print(out_trans)
            if '' in out_trans: 
                print('-----------------------')
                print('oov: '+ line)
                print(key,out_trans)
                continue
            out_label.write(key + " " + " ".join(out_trans) + "\n")
            out_label.flush()
        out_label.close()
if __name__ == "__main__":
    main()