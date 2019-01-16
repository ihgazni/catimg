import spaint.spaint as spaint
import time
import os
import math
import elist.elist as elel
import cv2
import numpy as np
import sys

#
RGB_CLUT = elel.mapv(spaint.ANSI256_COLORS_SHEET,lambda d:(d['rgb']['r'],d['rgb']['g'],d['rgb']['b']))


def winsize():
    sz = os.get_terminal_size()
    print(sz)
    return((sz.columns,sz.lines))


def resize(cw, ch, vw, vh, ref="width"):
    wr = vw / vh
    hr = vh / vw
    if ((vw <= cw) & (vh <= ch)):
        pass
    elif((vw <= cw) & (vh >= ch)):
        vh = ch
        vw = vh * wr
    elif((vw >= cw) & (vh <= ch)):
        vw = cw
        vh = vw * hr
    elif((vw >= cw) & (vh >= ch)):
        if(ref == "width"):
            vw = cw
            vh = vw * hr
            if (vh > ch):
                vh = ch
                vw = vh * wr
            else:
                pass
        else:
            vh = ch
            vw = vh * wr
            if (vw > cw):
                vw = cw
                vh = vw * hr
            else:
                pass
    else:
        pass
    return ({
        "cw":int(cw),
        "ch":int(ch),
        "vw":int(vw),
        "vh":int(vh),
        "left": int((cw - vw) / 2),
        "top": int((ch - vh) / 2)
    })

def resize2win(vw, vh,ref="width"):
    cw,ch = winsize()
    #important,beacuse we use 2 space to build a block
    cw = cw /2
    return(resize(cw, ch, vw, vh, ref))

def creat_empty_line(cw):
    return("\x20"*cw)

def creat_tb_padding(cw,top):
    line = creat_empty_line(cw)
    return([line]*int(top))

def padding_left(lines,left):
    lines = elel.mapv(lines,lambda line:("\x20"*2*left)+line)
    return(lines)

def centerlize(lines,cw,top,left):
    tb_padding = creat_tb_padding(cw,top)
    lines =  padding_left(lines,left)
    return(elel.concat(tb_padding,lines,tb_padding))

######
def pixelarr(img_file):
    img = cv2.imread(img_file)
    vh,vw,vd = img.shape
    d = resize2win(vw, vh)
    vw = int(d["vw"])
    vh = int(d["vh"])
    img = cv2.resize(img,(vw,vh),interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    cv2.waitKey()
    return((img,d))


def npixel2rgb(narr):
    r = narr[0]
    g = narr[1]
    b = narr[2]
    return((r,g,b))


def distance(p1,p2):
    vector1 = np.array(p1)
    vector2 = np.array(p2)
    diff = vector2 - vector1
    squareDistance = np.dot(diff.T, diff)
    return(math.sqrt(squareDistance))


def find_index(p):
    nodes = np.asarray(RGB_CLUT)
    deltas = nodes - p
    dist = np.einsum('ij,ij->i', deltas, deltas)
    return(np.argmin(dist))

####

#####


#####

####


def linefill(line,c):
    def map_func(colorId,c):
        c = spaint.paint_str(c,color_sec=[(0,2,colorId,colorId)])
        return(c)
    line = elel.mapv(line,map_func,[c])
    return(line)

def img2ansi256indexes(img,c):
    lines = elel.init(img.__len__(),[])
    for i in range(lines.__len__()):
        line = img[i]
        line = list(map(find_index,line))
        line = elel.join(linefill(line,c),"")
        lines[i] = line
    return(lines)


##############

def img2txt(img_file,c):
    img,d = pixelarr(img_file)
    cw = d["cw"]
    top = d["top"]
    left = d["left"]
    lines = img2ansi256indexes(img,c)
    lines = centerlize(lines,cw,top,left)
    return(elel.join(lines,"\n"))

def wfile(fn,content):
    fd = open(fn,'w+')
    fd.write(content)
    fd.close()

if(__name__=="__main__"):
    try:
        s = img2txt(sys.argv[1],sys.argv[3])
    except:
        s = img2txt(sys.argv[1],"\x20"*2)
    else:
        pass
    print(s)
    try:
        wfile(sys.argv[2],s)
    except:
        fn = "./_" + os.path.basename(sys.argv[1]) + ".txt"
        wfile(fn,s)
else:
    pass
