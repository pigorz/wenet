source /nfs/project/luone/env.sh
#KALDI_ROOT=/export/maryland/binbinzhang/kaldi
KALDI_ROOT=/nfs/project/luone/kaldi

[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/tools/sctk/bin:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh

[ ! -d utils ] && ln -s $KALDI_ROOT/egs/wsj/s5/utils
[ ! -d steps ] && ln -s $KALDI_ROOT/egs/wsj/s5/steps

export LC_ALL=C

# NOTE(kan-bayashi): Use UTF-8 in Python to avoid UnicodeDecodeError when LC_ALL=C
export PYTHONIOENCODING=UTF-8
export PYTHONPATH=../../../:$PYTHONPATH

export LD_LIBRARY_PATH=/nfs/project/luone/tools/mkl_lib/lib:$LD_LIBRARY_PATH
export PATH=/nfs/volume-225-4/yinhengxin/anaconda3/bin:$PATH
export LD_LIBRARY_PATH=/nfs/volume-225-4/yinhengxin/anaconda3/lib:$LD_LIBRARY_PATH