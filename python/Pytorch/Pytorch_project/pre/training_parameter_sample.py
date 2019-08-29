from training_model import training1D,training2D,training4D


def One_dimension_network(network,filename,mode):
    def main():
        training1D(network,filename,mode)
    if __name__ == '__main__':
        main()
def Two_dimension_network(network,filename,mode):
    def main():
        training2D(network,filename,mode)
    if __name__ == '__main__':
        main()
def Four_dimension_network(network,filename,mode):
    def main():
        training4D(network,filename,mode)
    if __name__ == '__main__':
        main()

def all_training(N,NETWORK,FILENAME,mode,dimension):
    if(dimension==1):
        for filename in FILENAME:
            for n,network in enumerate(NETWORK):
                filename[3].append(str(N[n]))
                One_dimension_network(network,filename,mode) 
    elif(dimension==2):
        for filename in FILENAME:
            for n,network in enumerate(NETWORK):
                filename[3].append(str(N[n]))
                Two_dimension_network(network,filename,mode) 
    elif(dimension==4):
        for filename in FILENAME:
            for n,network in enumerate(NETWORK):
                filename[3].append(str(N[n]))
                Four_dimension_network(network,filename,mode) 
    else:
        print("Please input the correct dimension !!!")

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './data'

N        = [5, 6, 7, 8]
NETWORK  = [[800, 0.001, [1,0] , 50, (25*2, 36, 2)],
            [800, 0.001, [1,0] , 50, (36*2, 36, 2)],
            [800, 0.001, [1,0] , 50, (49*2, 36, 2)],
            [800, 0.001, [1,0] , 50, (64*2, 36, 2)]]
FILENAME = [[path, [5,1    ], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [1,3    ], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [3,7    ], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [5,1,3,7], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [6,2    ], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [2,4    ], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [4,8    ], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [6,2,4,8], ["eigenvalue","phase"], ["20190823","G_matrix"]],
            [path, [1,2    ], ["eigenvalue","phase"], ["20190823","G_matrix"]]]


filename = [path, [5,1], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]
network = [1, 0.001, [1,0] , 3, (36*2, 36, 2)]
One_dimension_network(network,filename,False)


filename = [path, [5,1], ["BA","phase"], ["20190804","BA_matrix","6"]]
network = [1, 0.001, [1,0] , 3, [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 512, 2)]]
Two_dimension_network(network,filename,True)


filename = [path, [5,1], ["BA","phase"], ["20190804","BA_matrix","6"]]
network = [1, 0.001, [1,0] , 3, [(6, 16, (3,3,3), 1, (1,1,1)),(16, 32, (2,2,2), 1, (1,1,1)),(32 * 2 * 2 * 2, 128, 2)]]
Four_dimension_network(network,filename,True)

