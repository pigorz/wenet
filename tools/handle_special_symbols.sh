wav_trans_in=$1
wav_trans=${wav_trans_in}.out

cp ${wav_trans_in} ${wav_trans}.tmp

awk '{$1="";print $0}' ${wav_trans}.tmp > ${wav_trans}
awk '{print $1}' ${wav_trans}.tmp > ${wav_trans}.key

sed -i 's|\x00||g' $wav_trans # ^@
sed -i "s|Wi-Fi|WiFi|g" $wav_trans #
sed -i "s|b0ss|boss|g" $wav_trans # 
sed -i "s|\^O\^|\ |g" $wav_trans # ^O^
sed -i "s|\^o\^|\ |g" $wav_trans # ^o^
sed -i "s|\^0\^|\ |g" $wav_trans # ^O^
sed -i "s|\^_\^|\ |g" $wav_trans # ^_^
sed -i "s|\^ω\^|\ |g" $wav_trans # ^ω^
sed -i "s|，|\ |g" $wav_trans # 全角，
sed -i "s|,|\ |g" $wav_trans # 半角，
sed -i "s|:|\ |g" $wav_trans # 全角：
sed -i "s|：|\ |g" $wav_trans # 半角：
sed -i "s|？|\ |g" $wav_trans # 全角？
sed -i "s|?|\ |g" $wav_trans # 半角?
sed -i "s|！|\ |g" $wav_trans # 全角！
sed -i "s|!|\ |g" $wav_trans # 半角！
sed -i "s|~|\ |g" $wav_trans # ~
sed -i "s|_|\ |g" $wav_trans #_
sed -i "s|-|\ |g" $wav_trans # 减号
sed -i "s|-|\ |g" $wav_trans # 破折号的一半
sed -i "s|\.|\ |g" $wav_trans # 半角，
sed -i "s|\。|\ |g" $wav_trans # 全角。
sed -i 's|\\n|\ |g' $wav_trans # \n 
sed -i 's|\\t|\ |g' $wav_trans # \t
sed -i "s|\/|\ |g" $wav_trans # /
sed -i "s|《|\ |g" $wav_trans # 《
sed -i "s|》|\ |g" $wav_trans # 》
sed -i "s|、|\ |g" $wav_trans # 、
sed -i "s|’|\ |g" $wav_trans # 全角’
sed -i "s|‘|\ |g" $wav_trans # 全角‘
sed -i "s|；|\ |g" $wav_trans # 全角；
sed -i "s|;|\ |g" $wav_trans # 半角;
sed -i "s|”|\ |g" $wav_trans # 全角”
sed -i "s|“|\ |g" $wav_trans # 全角“
sed -i 's|"|\ |g' $wav_trans # 半角"
sed -i "s|\[|\ |g" $wav_trans # [
sed -i "s|\]|\ |g" $wav_trans #]
sed -i "s|【|\ |g" $wav_trans # 【 
sed -i "s|】|\ |g" $wav_trans # 【
sed -i "s|)|\ |g" $wav_trans # 半角）
sed -i "s|(|\ |g" $wav_trans # 半角(
sed -i "s|）|\ |g" $wav_trans # 全角)
sed -i "s|（|\ |g" $wav_trans # 全角
sed -i "s|\*|\ |g" $wav_trans # *
sed -i "s|\^|\ |g" $wav_trans # Λ
sed -i "s|……|\ |g" $wav_trans #
sed -i "s|#|\ |g" $wav_trans # #
sed -i 's|\$|\ |g' $wav_trans # $
sed -i 's|&|\ |g' $wav_trans # & 
sed -i 's|¥|\ |g' $wav_trans # ¥
sed -i 's|{|\ |g' $wav_trans # {
sed -i 's|}|\ |g' $wav_trans # }
sed -i 's|」|\ |g' $wav_trans # 
sed -i 's|「|\ |g' $wav_trans #r
sed -i 's|』|\ |g' $wav_trans # 』
sed -i 's|『|\ |g' $wav_trans # 『
sed -i "s|<|\ |g" $wav_trans # < 
sed -i "s|>|\ |g" $wav_trans #
sed -i 's|\\|\ |g' $wav_trans #\
sed -i 's|[ ][ ]*| |g' $wav_trans # 替换多个空格为一个空格
sed -i "s|. ||g" $wav_trans 
sed -i 's|`||g' $wav_trans
sed -i 's|\xEF\xBB\xBF||g' $wav_trans # <feff>
sed -i "s|^ ||" $wav_trans #开头的空格

paste ${wav_trans}.key $wav_trans > ${wav_trans}.out
mv ${wav_trans}.out $wav_trans
rm ${wav_trans}.key ${wav_trans}.tmp