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
def Three_dimension_network(network,filename,mode):
    def main():
        training4D(network,filename,mode)
    if __name__ == '__main__':
        main()


path = 'D:/program/vscode_workspace/private/data/project_data'
#path = './data'
filename = [path, [5,1], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]
network = [1, 0.001, [1,0] , 3, (36*2, 36, 2)]
One_dimension_network(network,filename,False)


filename = [path, [5,1], ["BA","phase"], ["20190804","BA_matrix","6"]]
network = [1, 0.001, [1,0] , 3, [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 512, 2)]]
Two_dimension_network(network,filename,True)

filename = [path, [5,1], ["BA","phase"], ["20190804","BA_matrix","6"]]
network = [1, 0.001, [1,0] , 3, [(6, 16, (3,3,3), 1, (1,1,1)),(16, 32, (2,2,2), 1, (1,1,1)),(32 * 2 * 2 * 2, 128, 2)]]
Three_dimension_network(network,filename,True)

