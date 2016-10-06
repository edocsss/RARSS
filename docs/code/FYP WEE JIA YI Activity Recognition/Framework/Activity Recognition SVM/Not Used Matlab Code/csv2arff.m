
for frame_size = 10:10:40
    withlen = 1;
    data = csvread(['.\test features\' num2str(frame_size) num2str(withlen) '\allFeatures.csv']);
    data = data(:,1:23);
    % data = getTestCaseSameSize(data);
    csvwrite(['.\arff\' num2str(frame_size) num2str(withlen)  'arffFeatures.csv'], data)
end