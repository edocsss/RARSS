function f = getAllFeatures( window_len, withLen, name)
% consolidate all files in test features folder for both SMA and all other training features
test = [];

%Consolidation for SMA feature(for motion transition processing)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dirs = dir(['.\test features ' name '\' num2str(window_len) num2str(withLen) 'sma\*.csv']);
fileList = {dirs.name};

for j = 1: length(fileList)
    fileName = fileList{j};
    feature = csvread(['.\test features ' name '\' num2str(window_len) num2str(withLen) 'sma\' fileName]);
    test = [test; feature];

end
csvwrite(['.\test features ' name '\' num2str(window_len) num2str(withLen) 'sma\allfeatures.csv'],test);

%Consolidation for model training features~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
test = [];
dirs = dir(['.\test features ' name '\' num2str(window_len) num2str(withLen) '\*.csv']);
fileList = {dirs.name};

for j = 1: length(fileList)
    fileName = fileList{j};
    feature=csvread(['.\test features ' name '\' num2str(window_len) num2str(withLen) '\' fileName]);
    test = [test; feature];
end
k = size(test,2)-3;

%When using testScript_separateTrain_Testfile, we need to ensure that the test file is normalised using the same min_max as the train file
%Remember to change the directory to reflect the folder of the train file
normStats=[];
maxi = max(test(:,1:k));
normStats=[normStats; maxi];
mini = min(test(:,1:k));
normStats=[normStats; mini];
csvwrite(['.\test features ' name '\' num2str(window_len) num2str(withLen) '\normalisationStats.csv'],normStats);

%%%comment (ctrl+shift+Q) this section when running cross validation*************
%%%%uncomment this section when running testScript_separateTrain_Testfile***********

%To read training data-set's normalisation base file, and use it to normalise test dataset
% normStats = csvread(['.\test features all\' num2str(window_len) num2str(withLen) '\normalisationStats.csv']);
% maxi=normStats(1, :);
% mini=normStats(2, :);

%%%%

for i = 1:k
    test(:,i) = (test(:,i)-mini(i))/(maxi(i)-mini(i));
end

csvwrite(['.\test features ' name '\' num2str(window_len) num2str(withLen) '\allfeatures.csv'],test);
f = test;
