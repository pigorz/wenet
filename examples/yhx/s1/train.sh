. ./path.sh || exit 1;
. ./cmd.sh || exit 1;

stage=3
stop_stage=3

export NCCL_IB_DISABLE=1

num_gpus=
master_addr=
master_port=

num_nodes=
node_rank=

dict=

train_set=

train_config=conf/train_unified_conformer_yhx.yaml

cmvn=true

dir=exp/yhx

checkpoint=

. utils/parse_options.sh || exit 1;
if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
    # Training
    mkdir -p $dir
    INIT_FILE=$dir/ddp_init
    #rm -f $INIT_FILE # delete old one before starting
    #init_method=file://$(readlink -f $INIT_FILE)
    init_method=tcp://$master_addr:$master_port
    echo "$0: init method is $init_method"
    #num_gpus=$(echo $CUDA_VISIBLE_DEVICES | awk -F "," '{print NF}')
    # Use "nccl" if it works, otherwise use "gloo"
    dist_backend="nccl"
    #cp ${feat_dir}/${train_set}/global_cmvn $dir
    world_size=`expr $num_gpus \* $num_nodes`
    cmvn_opts=
    $cmvn && cmvn_opts="--cmvn ${dir}/global_cmvn"
    # train.py will write $train_config to $dir/train.yaml with model input
    # and output dimension, train.yaml will be used for inference or model
    # export later
    for ((i = 0; i < $num_gpus; ++i)); do
    {
        gpu_id=$i
        #gpu_id=$(echo $CUDA_VISIBLE_DEVICES | cut -d',' -f$[$i+1])
        rank=`expr $node_rank \* $num_gpus + $i`
        python wenet/bin/train_deprecated.py --gpu $gpu_id \
            --config $train_config \
            --train_data fbank/$train_set/format.data \
            --cv_data fbank/dev/format.data \
            --symbol_table $dict
            ${checkpoint:+--checkpoint $checkpoint} \
            --model_dir $dir \
            --ddp.init_method $init_method \
            --ddp.world_size $world_size \
            --ddp.rank $rank \
            --ddp.dist_backend $dist_backend \
            --num_workers 1 \
            $cmvn_opts
    } &
    done
    wait
fi

