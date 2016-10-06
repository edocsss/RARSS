% clc;
% clear;
% frame_size = 6;
% withLen=1;
% THRESHOLD =0.999
% ACC = 0.977;
% 
% ABSPATH = pwd;
% 
% data = csvread([ABSPATH '.\test features\61\allFeatures.csv']);
% 
% temp = data(:,1:(size(data,2)-3));
% [temp dim]=getPrinComp(temp,THRESHOLD);
% data = [temp data(:,size(data,2)-2)];
% 
% minLoss= 0;
% [M, N]=size(data);
% accLossLog =[];
% accLossLog =[19 ACC-0.97568];
% data(:,end-1)=[];
% temp = data
for f =9:N-1 %where to get N??? What is N???
    temp = data(:,[1:f end]);
    %%%find the best parameters
    [f1 f2]=dividefile(temp,3000);
    [C G]=gridSearch(f1);
    s = fix(size(temp,1)/5);
    folder =[];
    for i = 1:5
        [file1 temp] = dividefile(temp,s);
        folder(:,:,i) = file1;
    end
    
    accLog =[];
    for i = 1:5
        file1 = [];
        for j=1:5
            if j~=i
                file1 = [file1; folder(:,:,j)];
            end
        end
        file2 = folder(:,:,i);
        %         file1(:,[feaNo(t,1):feaNo(t,2) feaNo(k,1):feaNo(k,2)]) = [];
        %         file2(:,[feaNo(t,1):feaNo(t,2) feaNo(k,1):feaNo(k,2)]) = [];
        model = svmtrain(file1(:,size(file1,2)), file1(:,1:size(file1,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
        [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)), file2(:,1:size(file2,2)-1), model);
        accLog =[accLog accuracy];
    end
    accLossLog = [accLossLog; [f C G mean(accLog(1,:))/100]];
    disp(['deleting dimension ' num2str(N-f) '. C: ' num2str(C) '. G: ' num2str(G) '. Average accuracy: ' num2str(mean(accLog(1,:))/100)]);
end


