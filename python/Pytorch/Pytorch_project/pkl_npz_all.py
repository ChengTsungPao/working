import numpy as np
from glob import glob
import matplotlib.pylab as plt
import copy
import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset
from multiprocessing import Process,Pool
#import plot_npz_4phase
#import plot_npz_2phase1 #mu = 1
#import plot_npz_2phase2 #delta = 0.5
#import plot_npz_2phase3 #delta = -0.5

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './train_data'
dimension = 4
kind_of_data = ["BA","phase"]
particle_data = ["20190823","BA_matrix",""]

start = input("input the start time: ")
end = input("input the end time: ")

def load_filename(start,end):
    data = []
    file = glob("*.pkl")
    for i in file:
        if(int(i.split(",")[0])>=int(start) and int(i.split(",")[0])<=int(end)):
            data.append(i)
    return data
    
def To_npz(pkl):
      classify = pkl.split("[")[1].split("]")[0]
      classify = classify.split(",")
      classify_phase = []

      for i in range(len(classify)):
          classify_phase.append(int(classify[i]))
 
      if(dimension==1): 
          classify_phase_change = copy.copy(classify_phase)
          classify_phase = [5,1,3,7]  # Don't forget to change !!!

      particle_data[2] = pkl.split("N=")[1][0]
      number_of_particle = int(particle_data[2])*int(particle_data[2])

      if(abs(classify_phase[0]-classify_phase[1])==1):
          if(classify_phase[0]==1):
              line = "delta=[0.5, -0.5]" #"mu=1"
          elif(classify_phase[0]==3):
              line = "mu=3"
          elif(classify_phase[0]==7):
              line = "mu=5"
          elif(classify_phase[0]==5):
              line = "mu=-1"
      elif(classify_phase[0]%2==1):
          line = "delta=0.5"
      elif(classify_phase[0]%2==0):
          line = "delta=-0.5"
      else:
          print("please input the correct phase !!!")
  
      def get_test_data(phase):  
          data = []
          file = np.load((path+'/test/{},{}_test,N={},{}.npz').format(particle_data[0],particle_data[1],particle_data[2],line))
          for i in range(len(phase)):
              cut = [len(file[kind_of_data[1]]),0]     
              for j in range(len(file[kind_of_data[1]])):        
                  if(cut[0] > j and int(file[kind_of_data[1]][j])==phase[i]):
                      cut[0] = j
                  if(cut[1] < j and int(file[kind_of_data[1]][j])==phase[i]):
                      cut[1] = j 
              data += file[kind_of_data[0]][cut[0]:cut[1]+1].tolist()        

          return np.array(data)
  
      try:
          model = torch.load(pkl)
      except:
          if(dimension==1):
              class DNN(nn.Module):
                  def forward(self, x):
                      x = x.view(x.size(0), -1)   
                      x = self.layer(x)
                      x = self.out(x)
                      output = nn.functional.softmax(x,dim=1)
                      return output
          elif(dimension==2 or dimension==4):
              class CNN(nn.Module):
                  def forward(self, x):
                      x = self.conv1(x)
                      x = self.conv2(x)
                      x = x.view(x.size(0), -1)   
                      x = self.layer(x)
                      x = self.out(x)
                      output = nn.functional.softmax(x,dim=1)
                      return output
          model = torch.load(pkl)
      

      def Probability(data,target):
          p = []
          for i in range(len(data)):
              if(dimension==1):
                  output = model(torch.tensor(data[i]).reshape(-1,number_of_particle*2).float().cuda())
              elif(dimension==2):
                  output = model(torch.tensor(data[i]).reshape(1,1,number_of_particle,number_of_particle).float().cuda())
              elif(dimension==4):    
                  output = model(torch.tensor(data[i]).reshape(-1,int(particle_data[2]),int(particle_data[2]),int(particle_data[2]),int(particle_data[2])).float().cuda())
              p.append(output[0][target].cpu().data.numpy())           
          return p

      target = []
      if(dimension!=1):
          for i in range(len(classify_phase)):
              target.append(Probability(get_test_data(classify_phase),i)) 
              ##plt.plot(range(len(target[i])),target[i],"o")
          #print(pkl.split(".pkl")[0])
          #plt.savefig(pkl.split(".pkl")[0])
          #plt.show()  
          #plt.clf()  

          if(len(classify_phase)==2):
              np.savez("./BA_npzfile/"+pkl.split(".pkl")[0],phase1 = target[0],phase2 = target[1])
          elif(len(classify_phase)==4):
              np.savez("./BA_npzfile/"+pkl.split(".pkl")[0],phase1 = target[0],phase2 = target[1],phase3 = target[2],phase4 = target[3])
          else:
              print("please input the correct phase !!!")
          
      else:
          for i in range(len(classify_phase_change)-int(classify_phase_change[2]==9)):
              target.append(Probability(get_test_data(classify_phase),i)) 
              #plt.plot(range(len(target[i])),target[i],"o")
          #plt.savefig(pkl.split(".pkl")[0])
          #plt.clf()
          #plt.show()
          #plt.clf()
          
          if(classify_phase_change[2]==9):
              np.savez("./G_npzfile/"+pkl.split(".pkl")[0],phase1 = target[0],phase2 = target[1])
          elif(classify_phase_change[2]==11):
              np.savez("./G_npzfile/"+pkl.split(".pkl")[0],phase1 = target[0],phase2 = target[1],phase3 = target[2])
          else:
              print("please input the correct phase !!!") 
        #if(len(classify_phase)==2):
        #    np.savez("./G_npzfile/"+pkl.split(".pkl")[0],phase1 = target[0],phase2 = target[1])
        #elif(len(classify_phase)==4):
        #    np.savez("./G_npzfile/"+pkl.split(".pkl")[0],phase1 = target[0],phase2 = target[1],phase3 = target[2],phase4 = target[3])
        #else:
        #    print("please input the correct phase !!!")

      #file = np.load("./BA_npzfile/"+pkl.split(".pkl")[0]+".npz")
      #if(line=="mu=1"):
      #    plot_npz_2phase1.phase2(pkl,file)
      #elif(line=="delta=0.5" and len(classify_phase)==2):
      #    plot_npz_2phase2.phase2(pkl,file)
      #elif(line=="delta=-0.5" and len(classify_phase)==2):
      #    plot_npz_2phase3.phase2(pkl,file)
      #else:
      #    plot_npz_4phase.phase4(pkl,file)
      #print(pkl)
      
p = Pool(processes=10)
p.map(To_npz, load_filename(start,end))
p.close()
p.join()