from training_model import training

#單一參數training
def Network(network,filename,dimension):
    def main():
        training(network,filename,dimension)
    if __name__ == '__main__':
        main()

#大量參數training
def all_training(parameter,dimension):
    for p in parameter:
        Network(p[0],p[1],dimension) 
    else:
        print("Please input the correct dimension !!!")

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './train_data'

########################################################################################################################################

#單一參數 training example
filename = [path, [9,10,9], ["eigenvalue","phase"], ["20190823","G_matrix","6"]] #[路徑, 相態, [數據類型, 答案], [數據生成日期, BA or Gij, N]]
network = [1, 0.001, [1,1] , 2, (36*2, 36, 2)]                                #[epoch, learning rate, [step_size, gamma], batch_size, internet]
Network(network,filename,1)                                                   

#大量參數 training example
#parameter = [[network, filename], [network, filename], [network, filename]......]
parameter =  [[[1000, 0.001, [9,10,9], 50, (25*2, 25, 2)],  [path, [9,10,9], ["eigenvalue","phase"], ["20190823","G_matrix","5"]]],
              [[1000, 0.001, [9,10,9], 50, (36*2, 36, 2)],  [path, [9,10,9], ["eigenvalue","phase"], ["20190823","G_matrix","6"]]],
              [[1000, 0.001, [9,10,9], 50, (49*2, 49, 2)],  [path, [9,10,9], ["eigenvalue","phase"], ["20190823","G_matrix","7"]]],
              [[1000, 0.001, [9,10,9], 50, (64*2, 64, 2)],  [path, [9,10,9], ["eigenvalue","phase"], ["20190823","G_matrix","8"]]]]

all_training(parameter,1)


