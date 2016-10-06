% clc;
% clear;
% frame_size = 6;
% withLen=1;
THRESHOLD =0.999
% ACC = 0.977;
% 
ABSPATH = pwd;

data = csvread([ABSPATH '.\test features\61\allFeatures.csv']);

load FV_Log;
FV_PCA_Log(1,:) =[];
temp = data(:,1:(size(data,2)-3));
[temp dim]=getPrinComp(temp,THRESHOLD);
data = [temp data(:,size(data,2)-2)];

minLoss= 0;
[M, N]=size(data);
model_size_Log = [];
for f =1:size(FV_PCA_Log,1)
    temp = data(:,[1:FV_PCA_Log(f,1) end]);
    %%%find the best parameters
    C = FV_PCA_Log(f,2);
    G = FV_PCA_Log(f,3);
    model = svmtrain(temp(:,size(temp,2)), temp(:,1:size(temp,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
    model_size_Log = [model_size_Log; [FV_PCA_Log(f,1) model.totalSV]];
end