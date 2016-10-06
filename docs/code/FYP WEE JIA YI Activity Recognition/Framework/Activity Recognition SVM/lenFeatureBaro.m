function lenFeatureBaro(frame_len, withLen,frequency)
%Run this file to extract standard deviation feature from barometer readings
%this information will be used to do high level motion processing

name = '7b'; %data file name

dirs = dir(['.\test cases_' name '\*.csv']);
if isdir(['test features ' name]) == 0;
    mkdir (['test features ' name]);
end

if isdir(['.\test features ' name '\' num2str(frame_len) num2str(withLen)]) ==0
    mkdir(['.\test features ' name '\' num2str(frame_len) num2str(withLen)]);
end

fileList = {dirs.name};
for j = 1: length(fileList)
    fileName = fileList{j};
    activity = str2num(fileName(1));
    fileName = strrep(fileName,'txt', 'csv');
    data=csvread(['.\test cases_' name '\' fileName]);
    data = data(:,2);
    %calculate the feature
    featureExtractionBaro( name, data,frame_len,frequency);
   
end
beep on;
beep;


