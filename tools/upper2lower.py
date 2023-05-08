import sys
path = sys.argv[1]
out_path = path + '.lower'
with open(path) as f:
    fi = f.read()
out = open(out_path, 'w')
out.write(fi.lower())
out.close()