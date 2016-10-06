% % function testScript(frame_size, withLen)
% 
% % lenFeature(frame_size, withLen);
% % data = getAllFeatures;
% % THRESHOLD = 0.9999;
clc;
clear;
frame_size = 6;
withLen=1;

ACC = 0.977;


data = csvread('.\test features NO\61\allFeatures.csv');
data(:,end-1:end)=[];
% 
% 
% %
% % accMeanlog = [];
% % accVarlog = [];
% % accCorlog = [];
% % accEnelog = [];
% % accEntlog = [];
% 
% if isdir('result') == 0;
%     mkdir 'result';
% end
% 
% if isdir(['.\result\' num2str(frame_size) num2str(withLen)]) ==0
%     mkdir(['.\result\' num2str(frame_size) num2str(withLen)]);
% end
% 
C=32;
G=8;
% %Each pocket we are doing it for ten times and then average them
% % temp = data;
minLoss= 0;
% data(:,6) =[];
ReduceDeminLog = [];

while minLoss<0.3
    accLossLog = [];
    [M,N]=size(data);
    for f =1:N-1
        temp = data;
        temp(:,f)=[];
        s = fix(size(temp,1)/5);
        folder =[];
        for i = 1:5
            [file1 temp] = dividefile(temp,s);
            folder(:,:,i) = file1;
        end
        
        %     feaNo = [[1 4];[5 8];[9 14];[15 18];[19 22]];
        
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
        accLossLog = [accLossLog; [f ACC-mean(accLog(1,:))/100]];
    end
    
    [minLoss idx] = min(accLossLog(:,2));
    data(:,idx) =[];
    ReduceDeminLog =[ReduceDeminLog; [idx minLoss] ];
end

%             elseif t==2
%                 file1 = [];
%                 for j=1:5
%                     if j~=i
%                         file1 = [file1; folder(:,:,j)];
%                     end
%                 end
%                 file2 = folder(:,:,i);
%                 file1(:,2:8) = [];
%                 file2(:,2:8) = [];
%                 model = svmtrain(file1(:,size(file1,2)), file1(:,1:size(file1,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
%                 [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)), file2(:,1:size(file2,2)-1), model);
%                 accVarlog = [accVarlog accuracy];
%             elseif t==3
%                 file1 = [];
%                 for j=1:5
%                     if j~=i
%                         file1 = [file1; folder(:,:,j)];
%                     end
%                 end
%                 file2 = folder(:,:,i);
%                 file1(:,9:14) = [];
%                 file2(:,9:14) = [];
%                 model = svmtrain(file1(:,size(file1,2)), file1(:,1:size(file1,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
%                 [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)), file2(:,1:size(file2,2)-1), model);
%                 accCorlog = [accCorlog accuracy];
%             elseif t==4
%                 file1 = [];
%                 for j=1:5
%                     if j~=i
%                         file1 = [file1; folder(:,:,j)];
%                     end
%                 end
%                 file2 = folder(:,:,i);
%                 file1(:,15:18) = [];
%                 file2(:,15:18) = [];
%                 model = svmtrain(file1(:,size(file1,2)), file1(:,1:size(file1,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
%                 [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)), file2(:,1:size(file2,2)-1), model);
%                 accEnelog = [accEnelog accuracy];
%             else
%                 file1 = [];
%                 for j=1:5
%                     if j~=i
%                         file1 = [file1; folder(:,:,j)];
%                     end
%                 end
%                 file2 = folder(:,:,i);
%                 file1(:,19:22) = [];
%                 file2(:,19:22) = [];
%                 model = svmtrain(file1(:,size(file1,2)), file1(:,1:size(file1,2)-1), ['-c ' num2str(C) ' -g ' num2str(G)]);
%                 [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)), file2(:,1:size(file2,2)-1), model);
%                 accEntlog = [accEntlog accuracy];
%         end
%     end
% end
%     csvwrite(['.\result\' num2str(frame_size) num2str(withLen) '\wholebodyPredictLabel' num2str(i) '.csv'], [file2(:,size(file2,2):size(file2,2)) predict_label]);
%     disp(['Accuracy is: ' num2str(fix(accuracy*100)) '%'] );

% csvwrite(['.\result\' num2str(frame_size) num2str(withLen)
% '\wholeBodyAccLog.csv'], accuracylog);

