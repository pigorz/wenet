import sys

path = sys.argv[1]
out_path = path + '.single_char'

with open(path,encoding='utf-8') as f:
    fi = f.read().splitlines()
out = open(out_path, 'w')
for i in fi:
    key = i.split()[0]
    trans = i.split()[1:]
    llst = []
    for j in trans:
        if j.replace("'","").replace('-','').encode('utf-8').isalpha():
            llst.append(j)
        else:
            for i in j:
                llst.append(i)
    out.write(key + ''+ ''.join(llst) + '\n')
out.close()