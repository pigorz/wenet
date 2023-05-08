import sentencepiece as spm 
import sys


lexicon_eng_path = sys.argv[1]
out_lexicon_eng_path = lexicon_eng_path + '.spm'
units_file = sys.argv[2]
spm_model = sys.argv[3]

sp = spm.SentencePieceProcessor()
sp.load(spm_model)

with open(lexicon_eng_path,encoding='utf-8') as f: 
    lexicon_eng_lst = f.read().splitlines()

with open(units_file,encoding='utf-8') as f:
    units = f.read().splitlines()

dic = {}

for i in units:
    dic[i.split()[0]] = 1

out_lexicon_eng = open(out_lexicon_eng_path, 'w') 

for line in lexicon_eng_lst:
    line2 = line.replace("'","").replace('-','')
    if line2.encode('utf-8').isalpha():
        out_lst = sp.encode_as_pieces(line)
        out_lst2 = sp.encode_as_pieces(line2) 
        out_pieces = ' '.join(out_lst)
        out_pieces_2 = ''.join(out_lst2) 
        out_lexicon_eng.write(line+'\t'+out_pieces+'\n')
        out_lexicon_eng.write(line+'\t'+out_pieces_2+'\n') 
        ind = 0
        for i in out_lst:
            ii = i.replace('_','')
            if ii not in dic: 
                ind = 1
        if ind == 0:
            out_pieces_3 = out_pieces.replace('_','')
            #out_lexicon_eng.write(line+'\t'+out_pieces_3+'\n')

        ind=0
        for i in out_lst2:
            ii = i.replace('_','')
            if ii not in dic: 
                ind = 1
            if ind ==0:
                out_pieces_4 = out_pieces_2.replace('_','')
                #out_lexicon_eng.write(line+'\t'+out_pieces_4+'\n')
    else:
        out_lexicon_eng.write(line+'\t'+' '.join([ii for ii in line])+'\n')
        
out_lexicon_eng.close()
