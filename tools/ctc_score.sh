./path.sh || exit 1;
./cmd.sh || exit 1;
decoding_chunk_size=8
decode_checkpoint=exp/20220919_conformer_exp8/25.pt

test_format=format.data.char+bpe
dict=data/dict/char6639_bpe5000.txt
decode_modes="ctc_score"
#ff=/nfs/volume-225-8/yinhengxin/data/audio/tmp/cac105e6-f017-4528-8574-1d0f080aa6e5.pcm
#ff=/nfs/volume-225-8/yinhengxin/data/audio/tmp/21f20003-4a40-459b-88a1-478e03632513.pcm

average_checkpoint=false
average_num=10

if echo ${ff} | grep -q-E 'lst$'; then
    awk '{print NR" "$1}' $ff > fbank/test/tmp/wav.scp
    awk '{print NR" tmp"}' $ff > fbank/test/tmp/text
elif echo ${ff} | grep -q -E 'scp$'; then
    cp $ff fbank/test/tmp/wav.scp
    awk '{print $1" tmp"}' $ff > fbank/test/tmp/text
else
    if echo ${ff} | grep -q-E 'pcm$'; then
    sox -r 16000 -t raw -b 16 -e signed-integer -c 1 $ff -r 16000 -t wav -b 16 -c 1 ${ff}.wav
    wav=${ff}.wav
    elif echo "$ff" | grep -q -E 'wav$';then
        wav=$ff
    fi
    echo "11 $fwav}" > fbank/test/tmp/wav.scp
    echo "11 tmp" > fbank/test/tmp/text
fi

steps/make_fbank.sh--cmd "train_and" --nj 1--write_utt2num_frames true --fbank_config conf/fbank.conf --compress true fbank/test/tmp > nohup.make_fbank_tmp
tools/format_data.sh --nj 1--feat fbank/test/tmp/feats.scp --bpecode data/dict/bpe5000.model --trans_type cn_char_en_bpe fbank/test/tmp ${dict} > fbank/test/tmp/format.data.char+bpe

dir=$(dirname ${decode_checkpoint})
for test_data in tmp; do
    mkdir -p $dir/test
    # Specify decoding_chunk size if it is a unified dynamic chunk trained model
    ctc weight-0.5
    for mode in ${decode_modes}; do
    {
        test_dir=$dir/test_${mode}
        out_dir=results_inference/${decode_checkpoint//\//_}_${test_data}_$mode
        mkdir -p $out_dir
        python wenet/bin/am_score_debug_s1.py --gpu 0 \
            --mode $mode \
            --config $dir/train.yaml \
            --test_data fbank/test/${test_data}/${test_format} \ 
            --checkpoint $decode_checkpoint \
            --beam_size 10 \
            --batch_size 1 \
            --penalty 0.0 \
            --dict $dict \
            --ctc_weight $ctc_weight \
            --result_file $out_dir/text \
            --symbol_table ${dict} \
            ${decoding_chunk_size:+--decoding_chunk_size $decoding_chunk_size}
        echo ${out_dir}/text
    }
    done
done