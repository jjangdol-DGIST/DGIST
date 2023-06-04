def binarySearch_1(list_in: list, value, offset=0):
    mid = int(len(list_in) / 2)
    left = list_in[:mid]
    right = list_in[mid:]
    
    if mid > len(list_in):
        return -1
    
    if list_in[mid] == value:
        return offset + mid
    elif list_in[mid] > value:
        return binarySearch_1(left, value, offset)
    else:
        return binarySearch_1(right, value, offset + mid + 1)
    

def binarySearch_2(list_in, value, offset, length):
    # FILL IN HERE
    return 0 

