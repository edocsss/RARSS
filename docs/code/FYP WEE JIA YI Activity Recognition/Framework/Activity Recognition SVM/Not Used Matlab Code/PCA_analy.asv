% function pca(frame_size, withLen)

% lenFeature(frame_size, withLen);
% data = getAllFeatures;
dimLog =[];
THRESHOLD = 0.9

data = csvread(['.\test features All\61\allFeatures.csv']);% nv see this folder leh
temp = data(:,1:(size(data,2)-3));
[ U, mu, variances ] = pca(temp');

dim = 1;
while (sum(variances(1:dim))/sum(variances))<THRESHOLD && dim < size(temp,2)
    dim = dim+1;
end
dim

dimLog = [digLog;[THRESHOLD, dim]];