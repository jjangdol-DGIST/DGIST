import numpy as np

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

def color3dtogray2d(cimg,gimg): 
    row,col=gimg.shape
    for i in range(row):
        for j in range(col): 
            gimg[i][j]=int(0.299*cimg[i][j][0]+0.587*cimg[i][j][1]+0.114*cimg[i][j][2])
    # gimg[:,:] = 0.299*cimg[:,:,0]+0.587*cimg[:,:,1]+0.114*cimg[:,:,2]
    # cimg[:,:,0] = cimg[:,:,1] = cimg[:,:,2] = gimg[:,:]

            
def gray2dtocolor3d(gimg,cimg): 
    row,col=gimg.shape
    for i in range(row):
        for j in range(col): 
            for k in range(3):
                cimg[i][j][k]=gimg[i][j]

def maskfiltering(img2d,mask):
    buff2d=img2d.copy()
    row,col=img2d.shape
    ms=int(len(mask)/2) # mask must be square with odd dimension.
    
    for i in range(ms,row-ms):
        for j in range(ms,col-ms):
            sum=0.0
            for p in range(-ms,ms+1):
                for q in range(-ms,ms+1):
                    sum+=buff2d[i+p][j+q]*mask[p+ms][q+ms]
            img2d[i][j]=intlimit(sum)

def maskfiltering2(img2d,maskx,masky):
    buff2d=img2d.copy()
    #global row, col
    row,col=img2d.shape
    ms=int(len(maskx)/2) # maskx and masky must be square with odd dimension.
    
    for i in range(ms,row-ms):
        for j in range(ms,col-ms):
            sumx=sumy=0.0
            for p in range(-ms,ms+1):
                for q in range(-ms,ms+1):
                    sumx+=buff2d[i+p][j+q]*maskx[p+ms][q+ms]
                    sumy+=buff2d[i+p][j+q]*masky[p+ms][q+ms]
            img2d[i][j]=intlimit(abs(sumx)+abs(sumy))

def medianfiltering(img2d,ms):
    buff2d=img2d.copy()
    row,col=img2d.shape
    hs=int(ms/2) # mask must be square with odd dimension.
    
    for i in range(hs,row-hs):
        for j in range(hs,col-hs):
            temp = []
            for p in range(-hs,hs+1):
                for q in range(-hs,hs+1):
                    temp.append(buff2d[i+p][j+q])
            temp.sort()
            img2d[i][j]=temp[int(ms*ms/2)]

def minmaxnorm(img2d): 
    maxv = np.max(img2d) 
    minv = np.min(img2d) 
    xl, yl = img2d.shape 
    n = maxv - minv
    for i in range(xl): 
        for j in range(yl):
            img2d[i][j] = intlimit((img2d[i][j] - minv)/n*255)
            
def histonorm(img2d):
    x1, y1 = img2d.shape
    cnt_array = np.unique(img2d, return_counts=True)
    for i in range(x1):
        for j in range(y1):
            idx = int(np.where(cnt_array[0]==img2d[i][j])[0])
            s = np.sum(cnt_array[1][:idx])
            img2d[i][j] = 255/(x1*y1)*s

def windowlevel(gimg2d,lv,wd):
    row,col=gimg2d.shape
    buff2d = np.full((row,col),0.0)

    lowl = lv-wd/2
    upl = lv+wd/2

    if lowl < 0:
        lowl = 0
    if upl > 255:
        upl = 255

    gimg2d = limit2d(gimg2d,lowl,upl)
    gimg2d = minmaxnorm(gimg2d)

    return gimg2d

def binarization(img2d, threshold): 
    xl, yl = img2d.shape
    for i in range(xl):
        for j in range(yl):
            if img2d[i][j] > threshold:
                img2d[i][j] = 255 
            else:
                img2d[i][j] = 0