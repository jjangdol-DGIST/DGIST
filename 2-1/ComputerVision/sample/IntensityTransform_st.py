# pip install numpy
# pip install pillow
# pip install matplotlib

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

def limit2d(arr2d,minv,maxv):
    row,col = arr2d.shape
    for i in range(row):
        for j in range(col):
            if arr2d[i][j]>maxv:
                arr2d[i][j]=maxv
            elif arr2d[i][j]<minv:
                arr2d[i][j]=minv
    return arr2d   

def readimage(img_name):
    global row,col
    im = Image.open(img_name)
    cimg = np.array(im)
    col,row = im.size
    return cimg,row,col

def saveimage(cimg,name):
    global row,col
    im=Image.fromarray(cimg)
    im.save(name)
    return im

def saveimage2d(img,name):
    row,col = img.shape
    limit2d(img)
    img=np.uint8(img)
    im=Image.fromarray(img)
    im.save(name)
    return im

def histoeq(gimg2d):
    buff2d = np.full((row,col),0)
    histo = np.full(256,0)
    pdf=np.full(256,0.0)
    cdf=np.full(256,0.0)

    for i in range(row):
        for j in range(col):
            histo[gimg2d[i][j]] +=1

    #plt.plot(histo)
    #plt.show()

    for i in range(256):
        pdf[i] = histo[i]/(row*col)
        if i==0:
            cdf[i] = pdf[i]
        else:
           (                                )
        
    for i in range(row):
        for j in range(col):
            buff2d[i][j]=round(255.0*cdf[gimg2d[i][j]])

    return buff2d         

def mmn2dimg(gimg2d,minv,maxv):
    # minv=min(map(min,gimg2d))
    # maxv=max(map(max,gimg2d))
    buff2d = np.full((row,col),0.0)
    
    if minv < 0:
        gimg2d = gimg2d[:,:] - minv
        maxv = maxv - minv
        minv = 0.0
       
    buff2d[:,:] = 255.0*(gimg2d[:,:]-minv)/(maxv-minv)
    buff2d = np.round(buff2d)
    return buff2d

def z_standard(gimg2d):
    buff2d = np.full((row,col),0.0)
    
    mean = gimg2d.mean()
    std = gimg2d.std()

    buff2d[:,:] = (gimg2d[:,:]-mean)/std
        
    # Keeping about 95%
    minv = (        )
    maxv = (        )
    
    limit2d(buff2d,minv,maxv)
    buff2d = mmn2dimg(buff2d,minv,maxv)

    return buff2d


def windowlevel(gimg2d,lv,wd):

    buff2d = np.full((row,col),0.0)

    lowl = lv-wd/2
    upl = lv+wd/2

    if lowl < 0:
        lowl = 0
    if upl > 255:
        upl = 255

    buff2d = limit2d(gimg2d,lowl,upl)
    buff2d = mmn2dimg(buff2d,lowl,upl)

    return buff2d

# main part starts here.
img_name="sample3.png"
cimg,row,col=readimage(img_name)

gimg2d = np.full((row,col),0)
gimg2d[:,:] = 0.299*cimg[:,:,0]+0.587*cimg[:,:,1]+0.114*cimg[:,:,2]

# gimg2d = histoeq(gimg2d)

# gimg2d = windowlevel(gimg2d,228,10)
# gimg2d = z_standard(gimg2d)

cimg[:,:,0] = cimg[:,:,1] = cimg[:,:,2] = gimg2d[:,:]
out_img_name="out_heq_"+img_name
saveimage(cimg,out_img_name)

# For handling color, but may be problematic. Why?
# for i in range(3):
#     gimg2d[:,:] = cimg[:,:,i]
#     gimg2d = histoeq(gimg2d)
#     cimg[:,:,i]=gimg2d[:,:]
