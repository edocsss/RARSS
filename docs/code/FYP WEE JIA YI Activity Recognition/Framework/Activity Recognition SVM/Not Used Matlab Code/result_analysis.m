   result =[];
for frameLen = 10:10:40
    withLen = 1

    %find the number of folders that used in the cross validation
    fileName = ['.\result\' num2str(frameLen) num2str(withLen) '\wholeBodyAccLog.csv'];
    acc = csvread(fileName);
    result = [result; [frameLen mean(acc(1,:)')]];
end

% %FscoreLog is a matrix to measue the f-score for each window size
% % for each column
% 
% FscoreLog = [];
% 
% for frameLen = 1:6
%     withLen = 1
% 
%     %find the number of folders that used in the cross validation
%     fileName = ['.\result\' num2str(frameLen) num2str(withLen) '\wholeBodyAccLog.csv'];
%     acc = csvread(fileName);
%     iterator = size(acc,2);
%     
%     precisionLog = [];
%     recallLog = [];
% 
%     %get the precision and recall for each frame size without
%     %consideration of the pockets, calculate each F-score
%     indiFscoreLog = [];
%     for i = 1:iterator
%         fileName = ['.\result\' num2str(frameLen) num2str(withLen) '\wholebodyPredictLabel' num2str(i) '.csv'];
%         label = csvread(fileName);
%         pLabel=label;
% 
%         crossTable = zeros(7, 7);
%         for i = 1:size(pLabel,1)
%             crossTable(pLabel(i,1), pLabel(i,4)) = crossTable(pLabel(i,1), pLabel(i,4))+1;
%         end
%         precision = [];
%         sumD = sum(crossTable);
%         for i = 1:size(crossTable)
%             precision = [precision crossTable(i,i)/sumD(i)];
%         end
% 
%         recall= [];
%         sumD = sum(crossTable');
%         for i = 1:size(crossTable)
%             recall = [recall crossTable(i,i)/sumD(i)];
%         end
% 
%         precisionLog = [precisionLog; precision];
%         recallLog = [recallLog; recall];
%         indiFscore = 2*(precision.*recall)./(precision+recall);
%         indiFscoreLog = [indiFscoreLog; indiFscore];
%     end
%     FscoreLog = [FscoreLog; mean(indiFscoreLog)];
% end
% figure(1);
% plot(mean(FscoreLog'),'b*-');
% xlabel('frame size (seconds)');
% ylabel('F\_score');
% % print(1, '-djpeg', ['.\figure\F-score4differentFrames.jpg']);
% % plot(FscoreLog(3,:),'k*-')
% % xlabel('Activities');
% % ylabel('F-score');
% % print(1, '-djpeg', ['.\figure\F-score4frame3.jpg']);
% 
