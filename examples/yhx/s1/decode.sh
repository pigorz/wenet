./path.sh || exit 1;
./cmd.sh || exit 1;

model=exp/encoder_1_fusion_add_trainset_train_20220830_cs/format.data.syllable+bpe_gate_0/10_6.zip
fst_dir=data/lm/tlg_20220831_syllable1314+bpe5000
chunk_size=-1

for test_data in test_16k_d1_0204_0209 ; do 
    out_dir=results/${model//\//_}_${test_data}_$(basename ${fst_dir})

    if [-d ${out_dir} ];then
        rm -r ${out_dir}
    fi

    if [ $test_data == "musiccase" ] 11 [ $test_data = "mona_010_badcase" ]; then
        nj=6
    else
        nj=16
    fi

    ./tools/decode.sh --nj $nj \
        --beam 15.0 --lattice_beam 7.5 --max_active 7000 \
        --blank_skip_thresh 0.98 --ctc_weight 0.5 --rescoring_weight 1.0 \ 
        --chunk_size $chunk_size \
        --fst_path ${fst_dir}/TLG.fst \
        --dict_path ${fst_dir}/words.txt \
        data/test/${test_data}/wav.scp data/test/${test_data}/text ${model} \
        ${fst_dir}/units.txt ${out_dir}
    iconv -f utf-8 -t gbk data/test/${test_data}/text -o $fout_dir}/text.ori.gbk 
    iconv -f utf-8 -t gbk $fout_dir}/text -o $fout_dir}/text.out.gbk
    sed -i "s/\ 八\tl" ${out_dir}/text.out.gbksed -i "s/\ 八\tl" ${out_dir}/text.ori.gbk
    tools/wer $fout_dir}/text.ori.gbk ${out_dir}/text.out.gbk $fout_dir}/text.rls.gbk
    echo $model
    echo ${out_dir}/text.rls.gbk 
    tail -n 5 ${out_dir}/text.rls.gbk
done