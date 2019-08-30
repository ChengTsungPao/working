from training_model import training1D,training2D,training4D

#單一參數training
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

#大量參數training
def all_training(parameter,mode,dimension):
    if(dimension==1):
        for p in parameter:
            One_dimension_network(p[0],p[1],mode) 
    elif(dimension==2):
        for p in parameter:
            Two_dimension_network(p[0],p[1],mode) 
    elif(dimension==4):
        for p in parameter:
            Four_dimension_network(p[0],p[1],mode) 
    else:
        print("Please input the correct dimension !!!")

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './data'

########################################################################################################################################

#單一參數 training1D example
filename = [path, [5,1], ["eigenvalue","phase"], ["20190823","G_matrix","6"]] #[路徑, 相態, [數據類型, 答案], [數據生成日期, BA or Gij, N]]
network = [1, 0.001, [1,0] , 3, (36*2, 36, 2)]                                #[epoch, learning rate, [step_size, gamma], batch_size, internet]
One_dimension_network(network,filename,False)                                 #False:mu=1 True:mu=1.0 

#大量參數 training1D example
#parameter = [[network, filename], [network, filename], [network, filename]......]
parameter =  [[[1000, 0.001, [1,1], 50, (25*2, 25, 2)],  [path, [5,1    ], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[1000, 0.001, [1,1], 50, (36*2, 36, 2)],  [path, [5,1    ], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[1000, 0.001, [1,1], 50, (49*2, 49, 2)],  [path, [5,1    ], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[1000, 0.001, [1,1], 50, (64*2, 64, 2)],  [path, [5,1    ], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[1000, 0.001, [1,1], 50, (25*2, 25, 2)],  [path, [1,3    ], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[1000, 0.001, [1,1], 50, (36*2, 36, 2)],  [path, [1,3    ], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[1000, 0.001, [1,1], 50, (49*2, 49, 2)],  [path, [1,3    ], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[1000, 0.001, [1,1], 50, (64*2, 64, 2)],  [path, [1,3    ], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[900 , 0.001, [1,1], 50, (25*2, 25, 2)],  [path, [3,7    ], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[900 , 0.001, [1,1], 50, (36*2, 36, 2)],  [path, [3,7    ], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[900 , 0.001, [1,1], 50, (49*2, 49, 2)],  [path, [3,7    ], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[900 , 0.001, [1,1], 50, (64*2, 64, 2)],  [path, [3,7    ], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[300 , 0.001, [1,1], 50, (25*2, 25, 4)],  [path, [5,1,3,7], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[300 , 0.001, [1,1], 50, (36*2, 36, 4)],  [path, [5,1,3,7], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[300 , 0.001, [1,1], 50, (49*2, 49, 4)],  [path, [5,1,3,7], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[300 , 0.001, [1,1], 50, (64*2, 64, 4)],  [path, [5,1,3,7], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[1000, 0.001, [1,1], 50, (25*2, 25, 2)],  [path, [6,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[1000, 0.001, [1,1], 50, (36*2, 36, 2)],  [path, [6,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[1000, 0.001, [1,1], 50, (49*2, 49, 2)],  [path, [6,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[1000, 0.001, [1,1], 50, (64*2, 64, 2)],  [path, [6,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[1000, 0.001, [1,1], 50, (25*2, 25, 2)],  [path, [2,4    ], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[1000, 0.001, [1,1], 50, (36*2, 36, 2)],  [path, [2,4    ], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[1000, 0.001, [1,1], 50, (49*2, 49, 2)],  [path, [2,4    ], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[1000, 0.001, [1,1], 50, (64*2, 64, 2)],  [path, [2,4    ], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[900 , 0.001, [1,1], 50, (25*2, 25, 2)],  [path, [4,8    ], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[900 , 0.001, [1,1], 50, (36*2, 36, 2)],  [path, [4,8    ], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[900 , 0.001, [1,1], 50, (49*2, 49, 2)],  [path, [4,8    ], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[900 , 0.001, [1,1], 50, (64*2, 64, 2)],  [path, [4,8    ], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[300 , 0.001, [1,1], 50, (25*2, 25, 4)],  [path, [6,2,4,8], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[300 , 0.001, [1,1], 50, (36*2, 36, 4)],  [path, [6,2,4,8], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[300 , 0.001, [1,1], 50, (49*2, 49, 4)],  [path, [6,2,4,8], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[300 , 0.001, [1,1], 50, (64*2, 64, 4)],  [path, [6,2,4,8], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]],

              [[1000, 0.001, [1,1], 50, (25*2, 25, 2)],  [path, [1,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],          
              [[1000, 0.001, [1,1], 50, (36*2, 36, 2)],  [path, [1,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],            
              [[1000, 0.001, [1,1], 50, (49*2, 49, 2)],  [path, [1,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],            
              [[1000, 0.001, [1,1], 50, (64*2, 64, 2)],  [path, [1,2    ], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]]]
all_training(parameter,False,1)


#單一參數 training2D example
filename = [path, [5,1], ["BA","phase"], ["20190804","BA_matrix","6"]]
network = [1, 0.001, [1,0] , 3, [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 512, 2)]]
Two_dimension_network(network,filename,True)


#單一參數 training4D example
filename = [path, [5,1], ["BA","phase"], ["20190804","BA_matrix","6"]]
network = [1, 0.001, [1,0] , 3, [(6, 16, (3,3,3), 1, (1,1,1)),(16, 32, (2,2,2), 1, (1,1,1)),(32 * 2 * 2 * 2, 128, 2)]]
Four_dimension_network(network,filename,True)

