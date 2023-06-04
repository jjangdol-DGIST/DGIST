from functions import _main, mdc
import glob
import os
import numpy as np
import re
import time

# make {name : path} dictionary
path = "/home/dgist/2-1/ComputerVision/HW2/Project2_images"
file_list = sorted(glob.glob(os.path.join(path, "*.png")))
o_dict = {}
p_dict = {}
pattern_o = re.compile(r'o[0-9]*\.png')
for file_path in file_list:
    name = file_path[51:]
    target_dict = o_dict if pattern_o.search(name) else p_dict
    target_dict[name] = file_path
name_list = list(o_dict.keys()) + list(p_dict.keys())

start_time = time.time()

# size (when the size is 8, 12, 16, 20, mdc makes the best result)
_size = 20

# make preprocessed numpy array
o_result = [_main(path, _size).flatten() for path in o_dict.values()]
p_result = [_main(path, _size).flatten() for path in p_dict.values()]

o_result = np.array(o_result)
p_result = np.array(p_result)

# do classify
wrong_list = []
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
        wrong_list.append(_obj)
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
        wrong_list.append(_obj)
        decide = 'orange'
    else:
        decide = 'persimmon'
    print(f"{_obj}'s pattern is {decide} by MDC {df}, the number of orange's sample : {o_result[front+rear].shape[0]}, the number of persimmon's sample : {p_result[front+rear].shape[0]}")

end_time1 = time.time()
elapsed_time1 = end_time1 - start_time # 첫 번째 함수 경과 시간
print("Elapsed time: %.6f seconds" % elapsed_time1)
print(f"Wrong classified images are {', '.join(str(x) for x in wrong_list)}")
error_rate = len(wrong_list) / 30 * 100
print(f"Error rate: {error_rate:.2f}%")
