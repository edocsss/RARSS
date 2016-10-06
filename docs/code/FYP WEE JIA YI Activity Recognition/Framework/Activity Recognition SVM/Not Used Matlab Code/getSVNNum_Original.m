ABSPATH = pwd;
data = csvread([ABSPATH '.\test features\61\allFeatures.csv']);
load FV_Log;
data(:,end-1:end) = [];
[M, N]=size(data);
model_size_Log = [];
for f =1:size(FV_Log,1)
    f
    temp = data(:,[1:FV_Log(f,1) end]);
    %%%find the best parameters
    C = FV_Log(f,2);
    G = FV_Log(f,3);
    model = svmtrain(temp(:,size(temp,2)), temp(:,1:size(temp,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
    model_size_Log = [model_size_Log; [FV_Log(f,1) model.totalSV]];
end