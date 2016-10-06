function featureExtractionBaro(name, data, window_len, frequency)
%This function will be triggered by lenFeatureBaro
%for Barometer readings feature extraction only

num = window_len*frequency; %number of data rows in a window
allFeature =[];

syms feature;
while size(data,1)>(num-1)

    window = data(1:num,:);
    data(1:(num/2),:)=[]; %50percent overlap
    feature = vpa(std(window),10); %extract standard deviation
    actual = cast(feature, 'double');
    allFeature = [allFeature; actual];
    
end
fileID = fopen(['.\test features ' name '\' num2str(window_len) '1\allfeatures.csv'],'w');
fprintf(fileID,'%12.6f\n',allFeature);
fclose(fileID);
