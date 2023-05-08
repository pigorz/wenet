lst=$1
cat $line | while read line;
do
  out_wav=/nfs/wav/$(basename ${line}).wav
  sox -r 16000 -t raw -b 16 -e signed-integer -c 1 $line -r 16000 -t wav -b 16 -c 1 ${out_wav}
done