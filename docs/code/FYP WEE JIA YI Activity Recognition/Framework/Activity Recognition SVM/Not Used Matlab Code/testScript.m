function testScript

% lenFeature(frame_size, withLen);
% data = getAllFeatures;
% THRESHOLD = 0.9999;


data = csvread(['.\test features zhang\11\allfeatures.csv']);
size(data)
% temp = data(:,1:(size(data,2)-3));
% [ U, mu,iances ] = pca(temp');
% 
% dim = 1;
% while (sum(ENERGYiances(1:dim))/sum(ENERGYiances))<THRESHOLD && dim < size(temp,2)
%     dim = dim+1;
% end
% dim
% [ Y, Xhat, pe ] = pca_apply(temp', U, mu,iances, dim );
% data = [Y' data(:, (size(data,2)-2):size(data,2))];
% data = getTestCaseSameSize(data);
accuracylog = [];

if isdir('result NO_ucisvm') == 0;
    mkdir 'result NO_ucisvm';
end

%if isdir(['.\result NO_ucisvm\' num2str(frame_size) num2str(withLen)]) ==0
%  mkdir(['.\result NO_ucisvm\' num2str(frame_size) num2str(withLen)]);
%end

% find the optimized parameter for the wholebody classification
% [N, T, para_body] = xlsread('para_whole.xlsx');
% for i = 1:length(para_body)
%     if para_body{i,1} == withLen && para_body{i,2} == frame_size
%         C = para_body{i,3};
%         G = para_body{i,4};
%         break;
%     end
% end
C=8;
G=128; % why use >1 accuracy increase so much
%Each pocket we are doing it for ten times and then average them
temp = data;
s = fix(size(temp,1)/10);
for i = 1:10
    [file1 temp] = dividefile(temp,s);
    folder(:,:,i) = file1;
end
for i = 1:10
    file1 = [];
    for j=1:10
        if j~=i
            file1 = [file1; folder(:,:,j)];
        end
    end
    file2 = folder(:,:,i); %took out the t loop
     model = svmtrain(file1(:,size(file1,2)-2), file1(:,1:size(file1,2)-3), ['-c ' num2str(C) ' -g ' num2str(G)]);
     [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)-2), file2(:,1:size(file2,2)-3), model);
      accuracylog = [accuracylog accuracy];
    
   
%         csvwrite(['.\result NO\' num2str(frame_size) num2str(withLen) '\wholebodyPredictLabel' num2str(i) '.csv'], [file2(:,size(file2,2)-2:size(file2,2)) predict_label]);
%     disp(['Accuracy is: ' num2str(fix(accuracy*100)) '%'] );
end
save('Zhang1');
%csvwrite(['.\result NO_ucisvm\61\wholeBodyAccLog.csv'], accuracylog);

% find the optimized parameter for the pocket classification
% [N, T, para_pocket] = xlsread('para_pockets.xlsx');
% para_pocket(1,:) = [];
% 
% for p = 1:6
%     
%     for i = 1:length(para_pocket)
%         if para_pocket{i,1}==withLen && para_pocket{i,2}==frame_size && para_pocket{i,3}==p
%             C = para_pocket{i,4};
%             G = para_pocket{i,5};
%             break;
%         end
%     end
%     
%     
%     pdata = zeros(size(data));
%     m =0;
%     for i = 1:size(data,1)
%         if data(i, size(data,2)-1)==p
%             m = m+1;
%             pdata(m,:) = data(i,:);
%         end
%     end
%     pdata = pdata(1:m,:);
% 
%     accuracylog = [];
%     
%     temp = pdata;
%     s = fix(size(temp,1)/5);
%     folder = [];
%     for i = 1:5
%         [file1 temp] = dividefile(temp,s);
%         folder(:,:,i) = file1;
%     end
%     for i = 1:5
%         file1 = [];
%         for j=1:5
%             if j~=i
%                 file1 = [file1; folder(:,:,j)];
%             end
%         end
%         file2 = folder(:,:,i);
%         model = svmtrain(file1(:,size(file1,2)-2), file1(:,1:size(file1,2)-3), ['-c ' num2str(C) ' -g ' num2str(G)]);
%         [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)-2), file2(:,1:size(file2,2)-3), model);
%         accuracylog = [accuracylog accuracy];
%         csvwrite(['.\result\' num2str(frame_size) num2str(withLen) '\pocket' num2str(p) num2str(i) 'PredictLabel.csv'], [file2(:,size(file2,2)-2) predict_label]);
%     end
%     csvwrite(['.\result\' num2str(frame_size) num2str(withLen) '\pocket' num2str(p) 'AccLog.csv'], accuracylog);
% end

