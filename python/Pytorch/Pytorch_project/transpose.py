import numpy as np

# 16 x 16

dim2 = np.zeros((16,16))


for i in range(len(dim2)):
    for j in range(len(dim2[0])):
        dim2[i][j] = 16*i+j
dim4 = dim2.reshape(4,4,4,4)
#dim4 = dim4.transpose(2,3,0,1)
#print(dim4)
#print("//////////////////////////////")
#print(dim4.transpose(3,0,1,2))
#print("//////////////////////////////")

#print(dim2)
ans2D = np.zeros((4,4))
for i in range(len(dim2)//4):
    for j in range(len(dim2[0])//4):

        for m in range(4):
            for n in range(4):
                if(dim2[i*4+m][j*4+n]>ans2D[i][j]):
                    ans2D[i][j] = dim2[i*4+m][j*4+n]
print(ans2D)

tmp = np.array([[51,55,59,63],[115,119,123,127],[179,183,187,191],[243,247,251,255]])

ans4D = np.zeros((2,2,2,2))

for a in range(len(dim4)//2):
    for b in range(len(dim4[0])//2):
        for c in range(len(dim4[0][0])//2):
            for d in range(len(dim4[0][0][0])//2):

                for i in range(2):
                    for j in range(2):
                        for m in range(2):
                            for n in range(2):
                                if(dim4[a*2+i][b*2+j][c*2+m][d*2+n]>ans4D[a][b][c][d]):
                                    ans4D[a][b][c][d] = dim4[a*2+i][b*2+j][c*2+m][d*2+n]



print("Origin:")
print(dim2)
print(dim4)
print("2D answer:")
print(ans2D)
print(ans4D.reshape(4,4))
print("-----------------------")
print("4D answer:")
print(ans2D.reshape(2,2,2,2))
print(ans4D)
