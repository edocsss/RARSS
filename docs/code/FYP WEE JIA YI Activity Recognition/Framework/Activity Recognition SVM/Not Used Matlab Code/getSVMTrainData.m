function getSVMTrainData(frame_size, withLen)
% frame_size=4;
% withLen = 1;
data = csvread(['.\test features VARCOR\' num2str(frame_size) num2str(withLen) '\allFeatures.csv']);
% data = getTestCaseSameSize(data);
labels = data(:,size(data,2)-2);
features=data(:,1:size(data,2)-3);
%features = [features data(:,size(data,2)-1)];
fs = sparse(features);

if isdir('parameter training VARCOR') == 0;
    mkdir 'parameter training VARCOR';
end

if isdir(['.\parameter training VARCOR\' num2str(frame_size) num2str(withLen)]) ==0
    mkdir(['.\parameter training VARCOR\' num2str(frame_size) num2str(withLen)]);
end


libsvmwrite(['.\parameter training VARCOR\' num2str(frame_size) num2str(withLen) '\whole.train'], labels, fs);
% 
% for p = 1:6
%     pocData = zeros(size(data));
%     n = 0;
%     for i = 1:size(data,1)
%         if data(i,size(data,2)-1) == p
%             n = n +1;
%             pocData(n,:) = data(i,:);
%         end
%     end
%     pocData = pocData(1:n,:);
%     labels = pocData(:,size(pocData,2)-2);
%     features= pocData(:,1:size(pocData,2)-3);
%     fs = sparse(features);
%     libsvmwrite(['.\parameter training\' num2str(frame_size) num2str(withLen) '\pocket' num2str(p) '.train'], labels, fs);
% end