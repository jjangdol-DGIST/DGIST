import numpy as np
from PIL import Image


def limit2d(arr2d,minv,maxv):
    row,col = arr2d.shape
    for i in range(row):
        for j in range(col):
            if arr2d[i][j]>maxv:
                arr2d[i][j]=maxv
            elif arr2d[i][j]<minv:
                arr2d[i][j]=minv
    return arr2d   

def intlimit(_int):
    if _int > 255:
        _int = 255
    elif _int < 0:
        _int = 0
    return round(_int)

def color3dtogray2d(cimg, gimg):
    gimg[:] = np.dot(cimg[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)

def maskfiltering(img2d, mask):
    buff2d = img2d.copy()
    row, col = img2d.shape
    mask = np.array(mask)
    ms = int(len(mask)/2)  # mask must be square with odd dimension.

    for i in range(ms, row-ms):
        for j in range(ms, col-ms):
            sum = np.sum(buff2d[i-ms:i+ms+1, j-ms:j+ms+1] * mask)
            img2d[i][j] = intlimit(sum)


def mdc(inp, meanp): # inp is a single vector with a dimension of {dim}, and meanp is {cl} by {dim} matrix
    cl,dim = np.shape(meanp)
    dist = np.full(cl,0.0)
    mdist = 10**100 # initialization with a large value 
    for i in range(cl):
        dist[i]=np.sqrt(np.sum(np.square(inp-meanp[i])))
        if dist[i] < mdist:
            mdist = dist[i] 
            mcl = i
    return dist, mcl+1 # class number starts with not 0 but 1

def _main(path, _size):
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
    gimg2d = gimg2d[175 : 175 + _size, 100 : 100 + _size]
    
    return gimg2d