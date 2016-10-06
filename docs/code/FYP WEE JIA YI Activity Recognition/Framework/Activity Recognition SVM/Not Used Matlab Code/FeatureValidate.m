% clc;
% clear;
% load ax;
% x =[x a];
% x = fliplr(x);
% frame_size = 6;
% withLen=1;
% THRESHOLD = 0.999
% ACC = 0.977;
% clc
% clear;
load FV_DimRed_log;
ABSPATH = pwd;
data = csvread([ABSPATH '\test features\61\allFeatures.csv']);
% temp = data(:,x);
% temp = [temp data(:, end-2)];
data(:, end-1:end) =[];

acc = flipud(FV_DimenReduce_Log);
acc = [acc zeros(size(acc,1),1)];
for loop = 2:size(acc,1)
    temp = data(:, [1:2 acc(1:loop,1)' end]);
    C = acc(loop,2);
    G = acc(loop,3);
    model = svmtrain(temp(:,end), temp(:,1:end-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
    acc(loop,end) = model.totalSV;
end

% %%%%code for fv
% data = [1:size(data,2); data];
% % N = size(temp,2);
% 
% FV_DimenReduce_Log =[];
% while size(data,2) > 2
%     [M, N] = size(data);
%     FV_Log = [];
%     for f =1:N-1
%         temp = data;
%         temp(1,:) =[];
%         temp(:,f)=[];
%         %%%find the best parameters
%         [acc_f C G] = crossValidation(temp, 5);
%         FV_Log = [FV_Log; [data(1,f) C G acc_f]];
%     end
%     [MaxAcc idx]=max(FV_Log(:,4));
% %     disp(['deleting dimension ' num2str(N-f) '. C: ' num2str(C) '. G: ' num2str(G) '. Average accuracy: ' num2str(mean(accLog(1,:))/100)]);
%     data(:,idx) =[];
%     FV_DimenReduce_Log = [FV_DimenReduce_Log; FV_Log(idx,:)];
% end
% %%%%%%%%%%%%%%%end code for FV


%
% clc;
% clear;
% frame_size = 6;
% withLen=1;
%
% ACC = 0.977;
% data = csvread(['.\test features\61\allFeatures.csv']);
% data(:,end-1:end)=[];
%
% C=32;
% G=8;
%
% minLoss= 0;
% data(:,6) =[];
% ReduceDeminLog = [6,0.00700000000000000;5,0.00679861285200978;7,0.00686546335756655;
%     6,0.00694902648951279;6,0.00718300325896204;5,0.00758410629230377;
%     6,0.00780137043536400;5,0.00823589872148411;5,0.00882084064510746;
%     10,0.00974003509651533;];
% % ReduceDeminLog= [];
% for i = 1:size(ReduceDeminLog,1)
%     data(:,ReduceDeminLog(i,1))=[];
% end
% while minLoss<0.3
%     accLossLog = [];
%     [M,N]=size(data);
%     for f =1:N-1
%         temp = data;
%         temp(:,f)=[];
%         s = fix(size(temp,1)/5);
%         folder =[];
%         for i = 1:5
%             [file1 temp] = dividefile(temp,s);
%             folder(:,:,i) = file1;
%         end
%
%         %     feaNo = [[1 4];[5 8];[9 14];[15 18];[19 22]];
%
%         accLog =[];
%         for i = 1:5
%             file1 = [];
%             for j=1:5
%                 if j~=i
%                     file1 = [file1; folder(:,:,j)];
%                 end
%             end
%             file2 = folder(:,:,i);
%             %         file1(:,[feaNo(t,1):feaNo(t,2) feaNo(k,1):feaNo(k,2)]) = [];
%             %         file2(:,[feaNo(t,1):feaNo(t,2) feaNo(k,1):feaNo(k,2)]) = [];
%             model = svmtrain(file1(:,size(file1,2)), file1(:,1:size(file1,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
%             [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)), file2(:,1:size(file2,2)-1), model);
%             accLog =[accLog accuracy];
%         end
%         accLossLog = [accLossLog; [f ACC-mean(accLog(1,:))/100]];
%     end
%
%     [minLoss idx] = min(accLossLog(:,2));
%     data(:,idx) =[];
%     ReduceDeminLog =[ReduceDeminLog; [idx minLoss] ];
% end
%
