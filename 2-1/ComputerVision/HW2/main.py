from functions import *
import glob
import os
import numpy as np
import re
from PIL import Image
import time

### _main func
### 넘파이 array 반환
def _main(path):
    ## sharpening
    laplacian_mask2 = [[1, 1, 1],[1,-8,1],[1,1,1]] 

    # main
    im = Image.open(path)

    im = im.resize((256, 256))

    col, row = im.size

    cimg3d = np.array(im)
    gimg2d = np.full((row,col),0)

    # 이미지를 흑백으로 변환
    color3dtogray2d(cimg3d,gimg2d)    
    
    maskfiltering(gimg2d, laplacian_mask2) 
    
    # 배열을 인덱싱 해서 일부 feature을 추출
    gimg2d = gimg2d[175 : 200, 100 : 125]
    
    return gimg2d

def classifier(o_mean, p_mean, obj):
    if abs(o_mean - obj) > abs(p_mean - obj):
        return False # 귤
    else:
        return True # 감


# ================================================================================
path = "/home/dgist/2-1/ComputerVision/HW2/Project2_images"
file_list = sorted(glob.glob(os.path.join(path, "*.png")))

o_dict = {}
p_dict = {}
pattern_o = r'o[0-9]*.png'

for _path in file_list:
    name = _path[51:]

    if re.search(pattern_o, name):
        o_dict[name] = _path
    else:
        p_dict[name] = _path

name_list = list(o_dict.keys()) + list(p_dict.keys())

# print("Start park's")
###------------park's------------------
start_time = time.time()
o_result = [_main(path).flatten() for path in o_dict.values()]
p_result = [_main(path).flatten() for path in p_dict.values()]

o_result = np.array(o_result)
p_result = np.array(p_result)

for i in range(15):
    front = list(range(i))
    rear = list(range(i+1,15))
    
    obj = o_result[i]
    _obj = name_list[i]
    
    meanp = np.array([np.mean(o_result[front+rear], axis=0), np.mean(p_result, axis=0)])

    df, decide = mdc(obj, meanp)
    if decide == 1:
        decide = 'orange'
    else:
        decide = 'persimmon'
    print(f"{_obj}'s pattern is {decide} by MDC {df}, the number of orange's sample : {o_result[front+rear].shape[0]}, the number of persimmon's sample : {p_result[front+rear].shape[0]}")

for i in range(15):
    front = list(range(i))
    rear = list(range(i+1,15))
    
    obj = p_result[i]
    _obj = name_list[15 + i]
    
    meanp = np.array([np.mean(o_result[front+rear], axis=0), np.mean(p_result, axis=0)])

    df, decide = mdc(obj, meanp)
    if decide == 1:
        decide = 'orange'
    else:
        decide = 'persimmon'
    print(f"{_obj}'s pattern is {decide} by MDC {df}, the number of orange's sample : {o_result[front+rear].shape[0]}, the number of persimmon's sample : {p_result[front+rear].shape[0]}")
end_time1 = time.time()
# 오차 : 오랜지 14, 15, 5, 8 = 4개

# print("Start Mine")
# ### --------------Mine-----------------
# for obj in name_list:
#     o_result = [_main(path).flatten() for path in o_dict.values()]
#     p_result = [_main(path).flatten() for path in p_dict.values()]

#     if obj in o_dict:
#         _obj = _main(o_dict[obj]).flatten()
#     else:
#         _obj = _main(p_dict[obj]).flatten()
    
#     o_result = [x for x in o_result if not np.array_equal(x, _obj)]
#     p_result = [x for x in p_result if not np.array_equal(x, _obj)]
    
#     # print([ret.shape for ret in o_result])
#     # print([ret.shape for ret in p_result])
    
#     if len(o_result) > len(p_result):
#         o_result.pop()
#     else:
#         p_result.pop()
    
#     meanp = np.array([np.mean(o_result, axis=0), np.mean(p_result, axis=0)])

#     df, decide = mdc(_obj, meanp)
#     if decide == 1:
#         decide = 'orange'
#     else:
#         decide = 'persimmon'
#     print(f"{obj}'s pattern is {decide} by MDC {df}, the orange's number of sample is {len(o_result)}, the persimmon's number of sample is {len(p_result)}")
# end_time2 = time.time()
#     # 오차 : 오랜지 14, 15, 5, 8

elapsed_time1 = end_time1 - start_time # 첫 번째 함수 경과 시간
# elapsed_time2 = end_time2 - end_time1 # 두 번째 함수 경과 시간
# total_elapsed_time = end_time2 - start_time # 총 경과 시간
print("Elapsed time: %.6f seconds" % elapsed_time1)
# print("Mine's elapsed time: %.6f seconds" % elapsed_time2)
# print("Total elapsed time: %.6f seconds" % total_elapsed_time)