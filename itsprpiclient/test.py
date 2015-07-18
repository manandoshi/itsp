import cv2
import numpy as np

img = cv2.imread("cropCircles.jpg",1)
#cv2.imshow("img", img)
#cv2.waitKey(0)
patternsize = (9,9)
corn = cv2.findChessboardCorners( img, patternsize )
print corn
##print len(corn[1])
"""
test = [0,0,0,0,0,0,0,0,0]
row1 = []
row2 = []
row3 = []
print corn[1].shape
for i in corn[1]:
    if int(i[0][1]) in range(195,206):
        test[0]+=1
        row1.append(i[0][0])
    elif int(i[0][1]) in range(457,468):
        test[1]+=1
        row2.append(i[0][0])
    elif int(i[0][1]) in range(722,733):
        test[2]+=1
    elif int(i[0][1]) in range(987,998):
        test[3]+=1
    elif int(i[0][1]) in range(1252,1263):
        test[4]+=1
    elif int(i[0][1]) in range(1517,1528):
        test[5]+=1
    elif int(i[0][1]) in range(1782,1793):
        test[6]+=1
    elif int(i[0][1]) in range(2046,2057):
        test[7]+=1
    elif int(i[0][1]) in range(2312,2323):
        test[8]+=1
        row3.append(i[0][0])
print test
row1.sort()
row2.sort()
row3.sort()
print row1
print row2
print row3
"""
cv2.drawChessboardCorners(img, patternsize, corn[1], corn[0])

cv2.imwrite('testwrite.jpg', img)


