
# return img, nested list
from os import X_OK
from sys import setprofile
import sys

sys.setrecursionlimit(1500000)

def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()

# Take filename as an input from the user
filename = input()
# Take the operation number as input
operation = int(input())


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE



img , max_color_value = read_ppm_file(filename)
rows = len(img)
cols = len(img[0])

# Operation 1 applies min-max normalization
if operation == 1:    
    minimum = int(input())
    maximum = int(input())
    for r in range(rows):
        for c in range(cols):
            for i in range(len(img[r][c])):
                img[r][c][i] = float("{:.4f}".format(((img[r][c][i]-0)/(255-0))*(maximum-minimum) + minimum))

    img_printer(img)

# Operation 2 applies z-score normalization  
if operation == 2 : 
    r_toplam = 0
    g_toplam = 0
    b_toplam = 0
    bolum = cols**2
    for r in range(rows):
        for c in range(cols):
            r_toplam += img[r][c][0]
            g_toplam += img[r][c][1]
            b_toplam += img[r][c][2]
    r_mean = r_toplam/bolum
    g_mean = g_toplam/bolum
    b_mean = b_toplam/bolum
    r_dev_toplam = 0
    g_dev_toplam = 0
    b_dev_toplam = 0
    for r in range(rows):
        for c in range(cols):
            r_dev_toplam += (img[r][c][0] - r_mean)**2
            g_dev_toplam += (img[r][c][1] - g_mean)**2
            b_dev_toplam += (img[r][c][2] - b_mean)**2
    r_deviation = (r_dev_toplam/bolum)**(0.5) + 10**-6
    g_deviation = (g_dev_toplam/bolum)**(0.5) + 10**-6
    b_deviation = (b_dev_toplam/bolum)**(0.5) + 10**-6
    for r in range(rows):
        for c in range(cols):
            img[r][c][0] = float("{:.4f}".format((img[r][c][0] - r_mean)/r_deviation))
            img[r][c][1] = float("{:.4f}".format((img[r][c][1] - g_mean)/g_deviation))
            img[r][c][2] = float("{:.4f}".format((img[r][c][2] - b_mean)/b_deviation))
    img_printer(img)           
            
                




# Operation 3 converts image to black and white
if operation == 3 :
    for r in range(rows):
        for c in range(cols):
            mean_ = sum(img[r][c])/len(img[r][c])
            mean = int(mean_)
            for i in range(len(img[r][c])):
                img[r][c][i] = mean

    img_printer(img)

# Opeartion 4 applies convolution to the image
if operation == 4 : 
    filtre = input()
    stride = int(input())
    new_list = []

    with open(filtre) as f:
        filter_list = []
        for line in f:
            filter_list.append(list(map(float, line.split(" "))))
    filtre_boyu = len(filter_list)

    count=-1
    for r in range(0,rows - filtre_boyu + 1,stride):
        new_list.append([])
        count += 1
        for c in range(0,rows - filtre_boyu + 1,stride):
            new_list[count].append([])

    for x in range(0,rows - filtre_boyu + 1,stride):
        for y in range(0,rows - filtre_boyu + 1,stride):
            r_toplam = 0
            g_toplam = 0
            b_toplam = 0
            for r in range(filtre_boyu):
                for c in range(filtre_boyu):
                    r_toplam += img[r+x][c+y][0]*float(filter_list[r][c])
                    g_toplam += img[r+x][c+y][1]*float(filter_list[r][c])
                    b_toplam += img[r+x][c+y][2]*float(filter_list[r][c])
            if r_toplam > 255:
                r_toplam = 255
            if r_toplam < 0: 
                r_toplam = 0
            if g_toplam > 255:
                g_toplam = 255
            if g_toplam < 0: 
                g_toplam = 0
            if b_toplam > 255:
                b_toplam = 255
            if b_toplam < 0: 
                b_toplam = 0

            new_list[x//stride][y//stride].append(int(r_toplam))
            new_list[x//stride][y//stride].append(int(g_toplam))
            new_list[x//stride][y//stride].append(int(b_toplam))
    img_printer(new_list)




# Operation 5 applies convolution to the image, padding zeros to the edges
# so that the ouput image has the same size as the input
if operation == 5 : 
    filtre = input()
    stride = int(input())
    new_list = []

    with open(filtre) as f:
        filter_list = []
        for line in f:
            filter_list.append(list(map(float, line.split(" "))))
    filtre_boyu = len(filter_list)

    zeroth_row = [[0,0,0] for k in range(len(img) + 2*(filtre_boyu//2))]
    for g in range(len(img)):
        for i in range(filtre_boyu//2):
            img[g].append([0,0,0])
            img[g].insert(0,[0,0,0])
    for i in range(filtre_boyu//2):
        img.insert(0,zeroth_row)
        img.append(zeroth_row)

    rows = len(img)
    cols = len(img[0])

    count=-1
    for r in range(0,rows - filtre_boyu + 1,stride):
        new_list.append([])
        count += 1
        for c in range(0,rows - filtre_boyu + 1,stride):
            new_list[count].append([])

    for x in range(0,rows - filtre_boyu + 1,stride):
        for y in range(0,rows - filtre_boyu + 1,stride):
            r_toplam = 0
            g_toplam = 0
            b_toplam = 0
            for r in range(filtre_boyu):
                for c in range(filtre_boyu):
                    r_toplam += img[r+x][c+y][0]*float(filter_list[r][c])
                    g_toplam += img[r+x][c+y][1]*float(filter_list[r][c])
                    b_toplam += img[r+x][c+y][2]*float(filter_list[r][c])
            if r_toplam > 255:
                r_toplam = 255
            if r_toplam < 0: 
                r_toplam = 0
            if g_toplam > 255:
                g_toplam = 255
            if g_toplam < 0: 
                g_toplam = 0
            if b_toplam > 255:
                b_toplam = 255
            if b_toplam < 0: 
                b_toplam = 0

            new_list[x//stride][y//stride].append(int(r_toplam))
            new_list[x//stride][y//stride].append(int(g_toplam))
            new_list[x//stride][y//stride].append(int(b_toplam))
    img_printer(new_list)




# Operation 6 applies color quantization to the image
if operation == 6 : 
    quant_range = int(input())
    def color_quantization(img,r=0,c=0):
        global quant_range
        if c%2 == 0:
            if img[r] != img[rows-1]:
                if abs(img[r][c][0]-img[r+1][c][0]) < quant_range and abs(img[r][c][1] - img[r+1][c][1]) < quant_range and abs(img[r][c][2] - img[r+1][c][2]) < quant_range :
                    img[r+1][c] = img[r][c]
                return color_quantization(img,r+1,c)
            elif img[r][c] != img[r][cols-1]:
                if abs(img[r][c][0] - img[r][c+1][0]) < quant_range and abs(img[r][c][1] - img[r][c+1][1]) < quant_range and abs(img[r][c][2] - img[r][c+1][2]) < quant_range :
                    img[r][c+1] = img[r][c]
                return color_quantization(img,r,c+1)
        else:
            if img[r] != img[0]:
                if abs(img[r][c][0] - img[r-1][c][0]) < quant_range and abs(img[r][c][1] - img[r-1][c][1]) < quant_range and abs(img[r][c][2] - img[r-1][c][2]) < quant_range :
                    img[r-1][c] = img[r][c]
                return color_quantization(img,r-1,c)
            elif img[r][c] != img[r][cols-1]:
                if abs(img[r][c][0] - img[r][c+1][0]) < quant_range and abs(img[r][c][1] - img[r][c+1][1]) < quant_range and abs(img[r][c][2] - img[r][c+1][2]) < quant_range :
                    img[r][c+1] = img[r][c]
                return color_quantization(img,r,c+1)
        if img[r][c] == img[rows-1][cols-1] or img[r][c] == img[0][cols-1]:
            return
    color_quantization(img)
    img_printer(img)

# Operation 7 applies color quantiation, if the channel values are in the range
if operation == 7 : 
    quant_range = int(input())
    def color_quantization(img,r=0,c=0,f=0):
        global quant_range
        if f == 0 :
            if c%2 == 0:
                if img[r] != img[rows-1]:
                    if abs(img[r][c][0]-img[r+1][c][0]) < quant_range:
                        img[r+1][c][0] = img[r][c][0]
                    return color_quantization(img,r+1,c,f)
                elif img[r][c] != img[r][cols-1]:
                    if abs(img[r][c][0] - img[r][c+1][0]) < quant_range:
                        img[r][c+1][0] = img[r][c][0]
                    return color_quantization(img,r,c+1,f)
            else:
                if img[r] != img[0]:
                    if abs(img[r][c][0] - img[r-1][c][0]) < quant_range :
                        img[r-1][c][0] = img[r][c][0]
                    return color_quantization(img,r-1,c,f)
                elif img[r][c] != img[r][cols-1]:
                    if abs(img[r][c][0] - img[r][c+1][0]) < quant_range :
                        img[r][c+1][0] = img[r][c][0]
                    return color_quantization(img,r,c+1,f)
            if img[r][c] == img[rows-1][cols-1] or img[r][c] == img[0][cols-1]:
                f += 1
                return color_quantization(img,r,c,f)
        if f == 1:
            if c%2 == 0 :
                if img[r][c] == img[rows-1][cols-1] :
                    if abs(img[r][c][0] - img[r][c][1]) < quant_range : 
                        img[r][c][1] = img[r][c][0]
                    if abs(img[r][c][1]-img[r-1][c][1]) < quant_range:
                        img[r-1][c][1] = img[r][c][1]
                    return color_quantization(img,r-1,c,f)
                if img[r] != img[0]:
                    if abs(img[r][c][1]-img[r-1][c][1]) < quant_range:
                        img[r-1][c][1] = img[r][c][1]
                    return color_quantization(img,r-1,c,f)
                elif img[r][c] != img[r][0]:
                    if abs(img[r][c][1] - img[r][c-1][1]) < quant_range:
                        img[r][c-1][1] = img[r][c][1]
                    return color_quantization(img,r,c-1,f)
            else:
                if img[r][c] == img[0][cols-1]:
                    if abs(img[r][c][0] - img[r][c][1]) < quant_range : 
                        img[r][c][1] = img[r][c][0]
                    if abs(img[r][c][1]-img[r+1][c][1]) < quant_range:
                        img[r+1][c][1] = img[r][c][1]
                    return color_quantization(img,r+1,c,f)
                if img[r] != img[rows-1]:
                    if abs(img[r][c][1]-img[r+1][c][1]) < quant_range:
                        img[r+1][c][1] = img[r][c][1]
                    return color_quantization(img,r+1,c,f)
                elif img[r][c] != img[r][0]:
                    if abs(img[r][c][1] - img[r][c-1][1]) < quant_range:
                        img[r][c-1][1] = img[r][c][1]
                    return color_quantization(img,r,c-1,f)  
            if img[r][c] == img[0][0]:
                f += 1
                return color_quantization(img,r,c,f)
        if f == 2 : 
            if img[r][c] == img[0][0] :
                if abs(img[r][c][2] - img[r][c][1]) < quant_range : 
                    img[r][c][2] = img[r][c][1]
                if abs(img[r][c][2]-img[r+1][c][2]) < quant_range:
                    img[r+1][c][2] = img[r][c][2]
                return color_quantization(img,r+1,c,f)
            if c%2 == 0:
                if img[r] != img[rows-1]:
                    if abs(img[r][c][2]-img[r+1][c][2]) < quant_range:
                        img[r+1][c][2] = img[r][c][2]
                    return color_quantization(img,r+1,c,f)
                elif img[r][c] != img[r][cols-1]:
                    if abs(img[r][c][2] - img[r][c+1][2]) < quant_range:
                        img[r][c+1][2] = img[r][c][2]
                    return color_quantization(img,r,c+1,f)
            else:
                if img[r] != img[0]:
                    if abs(img[r][c][2] - img[r-1][c][2]) < quant_range :
                        img[r-1][c][2] = img[r][c][2]
                    return color_quantization(img,r-1,c,f)
                elif img[r][c] != img[r][cols-1]:
                    if abs(img[r][c][2] - img[r][c+1][2]) < quant_range :
                        img[r][c+1][2] = img[r][c][2]
                    return color_quantization(img,r,c+1,f)
            if img[r][c] == img[rows-1][cols-1] or img[r][c] == img[0][cols-1]:
                return 

    color_quantization(img)
    img_printer(img)

    


def img_writer(img):
        f=open("outjaconde.ppm","w")
        row = len(img)
        col = len(img[0])
        cha = len(img[0][0])
        f.write("P3\n")
        f.write(str(cols)+" "+str(rows)+"\n")
        f.write("255\n")
        for i in range(row):
            for j in range(col):
                for k in range(cha):
                    f.write(str(img[i][j][k])+" ")
                f.write(" ")
            f.write("\n")
        f.close()
                               
img_writer(img)
   
#/Users/damlakayikci/Downloads/TP21_Joconde_Original.ppm
