#!/usr/bin/eny python3
# encoding: utf-8

import sys

# sys.argv[1]: e2e model unit file(lang_char.txt) # sys.argv[2]: raw lexicon file
# sys.argv[3]: output lexicon file
# sys.argv[4]: bpemodel

unit_table = set()
with open(sys.argv[1], 'r', encoding='utf8') as fin: 
    for line in fin:
        unit = line.split()[0]
        unit_table.add(unit)


def contain_oov(units):
    for unit in units:
        if unit not in unit_table: 
            print(unit)
            return True
    return False


bpemode = len(sys.argv) > 4
if bpemode:
    import sentencepiece as spm
    sp = spm. SentencePieceProcessor()
    sp.Load(sys.argv[4])

lexicon_table =set()

with open(sys.argv[2], 'r', encoding='utf8') as fin, \
    open(sys.argv[3], 'w', encoding='utf8') as fout: 
    for line in fin:
        word,lex = line.strip().split(' ',1)
        if word =='SIL' and not bpemode: # `sil` might be a valid piece in bpemodel
            continue
        elif word == '<SPOKEN_NOISE>':
            continue
        else:
            # each word only has one pronunciation for e2e system
            if word in lexicon_table:
                continue
            if bpemode:
                pieces = sp.EncodeAsPieces(word)
                if contain_oov(pieces):
                    print(
                        'Ignoring words {}, which contains oov unit'.format(
                        ''.join(word).strip('_'))
                    )
                    continue 
                chars =' '.join(
                    [p if p in unit_table else '<unk>' for p in pieces])
            else:
                # ignore words with 0oV
                if contain_oov(lex.splitO):
                    print('Ignoring words f, which contains oov unit'.format(word)) 
                    continue
                # Optional, append_ in front of english word
                # we assume the model unit of our e2e system is char now.
                if word.encode('utf8').isalpha() and '_' in unit_table:
                    word='_'+ word
            fout.write('{} {}\n'.format(word, lex))
            lexicon_table.add(word)