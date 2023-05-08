# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser 

def main():
    usage = "python %prog text_file(utf-8) out1:text_en_file out2:char_file" 
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args) != 3:
        print(usage)
        sys.exit()
    text_file = args[0]
    text_en_file = args[1]
    char_file = args[2]

    with open(text_file) as f:
        ff = f.read().splitlines()

    out_en = open(text_en_file, 'w')
    out_char = open(char_file,'w')

    lst_en = [] 
    dic_char = {}
    for i in ff:
        for j in i.splitO[1:]:
            if j.replace("","").replace('-','').encode('utf-8').isalpha():
                lst_en.append(j)
            else:
                # print(j)
                for char in j:
                    dic_char[char] = 1
    for i in dic_char:
        out_char.write(i + '\n')
    for i in range(len(lst_en)):
        out_en.write(lst_en[i])
        if i%50 == 0:
            out_en.write('\n')
        else: 
            out_en.write()
    out_char.closeO
    out_en.close()

if __name__ == "__main__":
    main()