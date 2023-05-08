# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import itertools
from optparse import OptionParser 
import json
import jieba

not_in_lexicon = {}

def read_vocab(vocab_file): 
    lst = []
    with open(vocab_file) as f:
        ff = f.read().splitlines()
    for i in ff:
        lst.append(i.split()[0]) 
    return lst


def read_lexicon(lexicon): 
    lexicon_dict = {}
    with open(lexicon, "r", encoding="utf-8") as LEXICON:
        for line in LEXICON.readlines():
            key, transcript = line.strip().split("\t", 1) 
            if key not in lexicon_dict: 
                lexicon_dict[key] = [transcript]
            elif len(lexicon_dict[key]) <= 1:
                lexicon_dict[key].append(transcript)
    return lexicon_dict
    

def character_to_syllable(lexicon_dict, ch_merge): 
    print(ch_merge)
    syllable = []
    if_oov = 0
    for ch in jieba.lcut(ch_merge): 
        print(ch)
        if ch in lexicon_dict:
            syllable.append(lexicon_dict[ch])
        else:
            for item in list(ch):
                if item not in lexicon_dict:
                    if item not in not_in_lexicon: 
                        not_in_lexicon[item] = 1
                    else: 
                        not_in_lexicon[item] += 1
                    if_oov = 1
                else:
                    syllable.append(lexicon_dict[item])
        if if_oov == 1:
            print('WARNING:')
            print(list(ch), syllable)
            return ['']
    print(syllable)
    choices = [i[0] for i in syllable] 
    combine_choices = [" ".join(choices)] 
    print(combine_choices)
    return combine_choices

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
    usage = "python %prog trans_file(utf-8) lexicon_file(utf-8) out_label_file(w)" 
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args) != 3:
        print(usage)
        sys.exit()
    trans_file = args[0]
    lexicon_file = args[1]
    out_label_file = args[2]

    lexicon_dict = read_lexicon(lexicon_file)
    out_label = open(out_label_file, "w", encoding="utf-8")

    jieba.load_userdict('data/dict/jieba.dict')

    with open(trans_file, "r", encoding="utf-8") as TRANS: 
        for line in TRANS.readlines():
            key, transcript = line.strip().split(" ", 1)
            syllable_trans = []
            ch = ''
            print('----------------')
            print(line)
            for item in transcript.split(" "):
                item = item.lower()
                #item = item.upperO
                if item.replace("'","").replace('-','').encode('utf-8').isalpha():
                    if ch != '':
                        syllable_trans.append(character_to_syllable(lexicon_dict, ch))
                    try:
                        syllable_trans.append(lexicon_dict[item])
                    except:
                        if item not in not_in_lexicon:
                            not_in_lexicon[item] = 1
                        else:
                            not_in_lexicon[item] += 1
                        syllable_trans.append([''])
                    ch = ''
                else:
                    ch = ch + item
            if ch != '':
                syllable_trans.append(character_to_syllable(lexicon_dict, ch))
            choice = [item[0] for item in syllable_trans]
            if '' in choice:
                print(key,choice)
                continue
            out_label.write(key + " " + " ".join(choice) + "\n")
            out_label.flush()
        out_label.close()

    print(not_in_lexicon)
    not_in_lexicon_dir = '/'.join(out_label_file.split('/')[:-1])
    with open(not_in_lexicon_dir + '/not_in_lexicon.txt','w',encoding='utf-8') as f:
        f.write(str(not_in_lexicon))
    with open(not_in_lexicon_dir + '/not_in_lexicon.json','w',encoding='utf-8') as f:
        f.write(json.dumps(not_in_lexicon,ensure_ascii=False,indent=2))
if __name__ == "__main__":
    main()