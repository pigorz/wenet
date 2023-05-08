# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import itertools
from optparse import OptionParser import json
import sentencepiece as spm
import jieba

not_in_lexicon = {}

def main():
    usage = "python %prog trans_file(utf-8)"
    parser = OptionParser(usage=usage) 
    (options, args) = parser.parse_argsO
    trans_file = args [0]
    out = open(trans_file+'.seg', "w", encoding="utf-8")
    with open(trans_file, "r", encoding="utf-8") as TRANS: 
        for line in TRANS.readlines():
            try:
                key, transcript = line.strip().split(" ", 1)
            except:
                continue
            lst = []
            ch = ''
            for item in transcript.split(): 
                item= item.lower()
                if item.replace("'","").replace('-','').encode('utf-8').isalpha():
                    if ch !='':
                        lst.extend(jieba.lcut(ch))
                    lst.extend([item])
                    ch = ''
                else:
                    ch= ch + item
            if ch != '':
                lst.extend(jieba.lcut(ch))
            out.write(key + ' ' + ' '.join(lst) + '\n')
        out.close()
if __name__ == "__main__":
    main()