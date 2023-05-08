f=$1

awk '{$1="";print $0}' $f | tr A-Z a-z > tmp.1
sed -i "s|^\ ||" tmp.1
sed -i "s|\ |\t|g" tmp.1
awk '{print $1}' $f | paste - tmp.1 > $f.lower
rm tmp.1