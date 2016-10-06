function [acc C G] = crossValidation(N_Folder)

name = '20female'; %dataset to cross-validate
windowSize = '1'; %window size of the dataset to cross-validate
temp = csvread(['.\test features ' name '\' windowSize '1\allfeatures.csv']);

%Grid Search to get optimal parameters
[f1 f2]=dividefile(temp,1000);
[C G]=gridSearch(f1);

%split datafile to number of folds 
s = fix(size(temp,1)/N_Folder); %number of data rows in one fold
folder =[];
for ii = 1:N_Folder
    [file1 temp] = dividefile(temp,s); 
    folder(:,:,ii) = file1; %store 10 divisions of dataset
end

%variables to store results statistics
accLog =[];
cf=[];

%perform actual cross validation here
for ii = 1:N_Folder
    file1 = [];
    for j=1:N_Folder
        if j~=ii
            file1 = [file1; folder(:,:,j)];
        end
    end
    file2 = folder(:,:,ii);
	%model training 
    model = svmtrain(file1(:,size(file1,2)-2), file1(:,1:size(file1,2)-3), ['-c ' num2str(C) ' -g ' num2str(G)]);
	%model testing
    [predict_label, accuracy, dec_value] = svmpredict(file2(:,size(file2,2)-2), file2(:,1:size(file2,2)-3), model);
	%store accuracy score
    accLog =[accLog accuracy];
	%retrieve confusion matrix to calculate F-score
    confusionmatrix =  confusionmat(file2(:,size(file1,2)-2), predict_label);
    cf = [cf confusionmatrix];
end
%save an instance of this cross validation run. Can get detailed information like number of SV used.
save(['test' windowSize '_' name]);
acc = mean(accLog(1,:))/100;
%sound signal to tell you cross validation is complete.=
beep on;
beep;