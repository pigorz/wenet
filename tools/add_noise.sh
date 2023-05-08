wav_scp=$1
text=$2
noise_file=$3
snr_min=$4
snr_max=$5
out_dir=$6
nj=$7

split_scps=""
mkdir -p ${out_dir}/split${nj}
mkdir -p ${out_dir}/wav_split${nj}
for n in $(seq ${nj}); do
  split_scps="${split_scps} ${out_dir}/split${nj}/wav.${n}.scp.ori"
done
tools/data/split_scp.pl ${wav_scp} ${split_scps}

for i in $split_scps; do
{
    python tools/add_noise.py $i $noise_file $snr_min $snr_max ${out_dir}/wav_split${nj}
} &
done
wait

find ${out_dir}/wav_split${nj} -name *.wav > ${out_dir}/wav_an.lst
awk -F '/' '{print $NF}' ${out_dir}/wav_an.lst > ${out_dir}/wav_an.key
paste ${out_dir}/wav_an.key ${out_dir}/wav_an.lst > ${out_dir}/wav_an.scp
awk -F '.wav' '{print $1}' ${out_dir}/wav_an.key > ${out_dir}/wav_an.key.1
awk 'NR==FNR{a[$1]=$0}NR>FNR{if ($1 in a) print a[$1]}' ${text} ${out_dir}/wav_an.key.1 > ${out_dir}/train.trans.out
awk '{$1="";print $0}' ${out_dir}/train.trans.out > ${out_dir}/train.trans.out.1
paste ${out_dir}/wav_an.key ${out_dir}/train.trans.out.1 > ${out_dir}/wav_an.txt
sed -i "s|\t\ |\ |" ${out_dir}/wav_an.txt
sed -i "s|\t|\t${out_dir}/|" ${out_dir}/wav_an.scp