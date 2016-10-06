function [data dim]= getPrinComp(temp, THRESHOLD)

[ U, mu, variances ] = pca(temp');

dim = 1;
while (sum(variances(1:dim))/sum(variances))<THRESHOLD && dim < size(temp,2)
    dim = dim+1;
end
% dim
[ Y, Xhat, pe ] = pca_apply(temp', U, mu, variances, dim );
data = Y';


k = size(data,2);

maxi = max(data(:,1:k));
mini = min(data(:,1:k));

for i = 1:k
    data(:,i) = (data(:,i)-mini(i))/(maxi(i)-mini(i));
end