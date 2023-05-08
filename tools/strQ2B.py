import sys
'''正常来说，一个汉字占2个字节，一个字母或者数字（半角）占1个字节
   但是存在占用2个字节的字母或者数字(全角)
   全角字符的unicode编码范围为[65281,65374]（不含空格）
   半角的为[33,126]，顺序一致，相差12288'''
#path.= '/mnt/ser011_data1/yinhengxin/data_set/feature_align/49_input_eng/train.trans.seg.utf8'
path = sys.argv[1]

with open(path,encoding='utf-8') as f:
    lst = f.read().splitlines()
def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:          #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):   #全角字符（除空格)根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring

with open(path+'.banjiao','w',encoding='utf-8') as f:
    for i in lst:
        # print(i)
        f.write(strQ2B(i)+'\n')