function lenFeature(window_len, withLen, frequency)
%Run this file to extract features for accelerometer readings
%window_len --- frame size in sec
%withLen--- with magnitude or not 1 yes, 0 no

name = '20female'; % datafile to process for feature extraction
dirs = dir(['.\test cases_' name '\*.csv']);

%create test features folder to store extracted features
%set up file directory for processing
if isdir(['test features ' name]) == 0;
    mkdir (['test features ' name]);
end
%to store features for model training
if isdir(['.\test features ' name '\' num2str(window_len) num2str(withLen)]) ==0
    mkdir(['.\test features ' name '\' num2str(window_len) num2str(withLen)]);
end
%to store SMA feature for High Level Motion processing later on. (SMA is not used for model training. Hence, must be separated.)
if isdir(['.\test features ' name '\' num2str(window_len) num2str(withLen) 'sma']) ==0
    mkdir(['.\test features ' name '\' num2str(window_len) num2str(withLen) 'sma']);
end

fileList = {dirs.name};
for j = 1: length(fileList)
    %process all data files in the directory folder
    fileName = fileList{j};
    activity = str2num(fileName(1));
    fileName = strrep(fileName,'txt', 'csv');
    data=csvread(['.\test cases_' name '\' fileName]); 
	%remove magnitude dimension if required
    if withLen == 0
        data(:,5) = [];
    end

    %calculate the features
    feature = featureExtraction(data,window_len,frequency);
    if size(feature,1) == 0
        continue;
    end

    %read the activity type information from the configure file
    pocket = str2num(fileName(2));
    posture = str2num(fileName(3));
	
    row = size(feature,1);
	
    %remove and add SMA to a separate file. SMA not used for model training. 
    SMA = feature(:,size(feature,2));
    csvwrite(['.\test features ' name '\' num2str(window_len) num2str(withLen) 'sma\' fileName],SMA);
    feature(:,size(feature,2))= [];
	
	%add the data tags to the data rows
    feature = [feature ones(row,1)*activity];
    feature = [feature ones(row,1)*pocket];
    feature = [feature ones(row,1)*posture];
    csvwrite(['.\test features ' name '\' num2str(window_len) num2str(withLen) '\' fileName],feature);

end
done = 'feature extraction done'

%consolidate and normalise extracted features
getAllFeatures( window_len, withLen, name);
beep on;
beep;