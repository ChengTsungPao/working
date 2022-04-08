%Try to transform n-dimensional search to 1-dimensional search  
clear all
global  X FUNC S ndim
ndim=2; %suppose the objective function is 2-dimensional (that is, 2-variable)
S=[1;0];%search direction. You need to change this if you have a different direction
X=[3;4];%starting point. You can start from a different point
FUNC=@myfunc;
[nu,fMin] = goldSearch(@fLine,-10, 10) 
%here the initial interval for golden section is [-10, 10]. Actually you should use some algorithm to get a better initial interval.

X=X+nu*S % the next point
%If you use the Univariate method, the next search direction S=[0;1];
%Anyway, keep searching (by using the while loop) until the stopping criterion is met.