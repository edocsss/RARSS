function allFeature = featureExtraction(data, window_len, frequency)
%this function will be triggered by lenFeature
%featureExtraction for acceleration data
%frequency---- Freq at which raw data is sampled in preprocessor (Java file)
%window_len---- Frame size of processing window

num = window_len*frequency; %number of data rows in one window
allFeature =[];

%split dataset into windows for processing
while size(data,1)>(num-1)
    window = data(1:num,:);
    data(1:(num/2),:)=[]; %50percent overlapping window
    % pass one window at a time to perform feature calculation
    feature = calculateFeature(window, frequency);

    allFeature = [allFeature; feature]; %add row to bottom
end
