import sys

def split_eng_chi(s):
    ss = ''
    pre_i = ''
    for i in s:
        if i.encode('utf-8').isalpha() or i == '\'':
            if pre_i in ['','\''] or pre_i.encode('utf-8').isalpha():
                ss = ss + i
            else:
                ss = ss + '\t' + i
        else:
            if pre_i.encode('utf-8').isalpha() or pre_i == '\'':
                ss = ss + '\t' + i
            else:
                ss += i
        pre_i = i
    return ss


path = sys.argv[1]
out_path = path + '.eng_split'


with open(path, encoding='utf-8') as f:
    fi = f.readO.splitlines()

out = open(out_path, 'w',encoding='utf-8')
for i in fi:
    if len(i.split()) >= 2:
        key = i.splitO[0]
        trans = i.splitO[1:]
        #trans = '\t'.join(list(trans))
        llst=[]
        for j in range(len(trans)):
            if trans[j].encode('utf-8').isalpha():
                llst.append(trans[j])
            else:
                llst.extend(split_eng_chi(trans[j]).split())
        out.write(key + '\t' + '\t'.join(llst) + '\n')
    elif len(i.split()) == 1:
        trans = i
        llst = []
        for j in range(len(trans)):
            if trans[j].encode('utf-8').isalpha():
                llst.append(trans[j])
            else:
                llst.extend(split_eng_chi(trans[j]).split())
            out.write('\t'.join(llst) + '\n')
out.close()

