. ./path.sh

model_name=exp/11/1.pt

m=${basename $model_name}
d=${dirname $model_name}

config=$PWD/${d}/train.yaml
dict=$PWD/data/dict/char6611_bpe5000.txt
model=$PWD/${model_name}
output_dir=$PWD/${d}/onnx_cpu_${m%*.*}

python wenet/bin/export_onnx_cpu.py \
            --config $config \
            --checkpoint $model \
            --output_dir $output_dir \
            --chunk_size -1 \
            --num_deocding_left_chunks -1 \
            --symbol_table ${dict}

python wenet/bin/export_onnx_gpu.py \
            --config $config \
            --checkpoint $model \
            --output_onnx_dir $output_dir \
            --ctc_weight 0.3 \
            --streaming