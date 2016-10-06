function testscript_separateTrain_Testfile (window_len)
%Use this file for LOO testing and High Level Motion Transition(HLMT) processing
%window_len represents number of frames in a processing window

name = 'ELDERLY';
testname = 'YOUTH';
windowSize =num2str(window_len);
temp = csvread(['.\test features ' name '\' windowSize '1\allfeatures.csv']);
testfile = csvread(['.\test features ' testname '\' windowSize '1\allfeatures.csv']);

%we use fix C & G parameters here 
C=1;
G=1/22; % (1/no.of.features)


%model training
model = svmtrain(temp(:,size(temp,2)-2), temp(:,1:size(temp,2)-3), ['-c ' num2str(C) ' -g ' num2str(G)]);
%model testing
[predict_label, accuracy, dec_value] = svmpredict(testfile(:,size(testfile,2)-2), testfile(:,1:size(testfile,2)-3), model);

%we store the prediction labels together with the SMA data (to be used for HLMT processing)
sma = csvread(['.\test features ' testname '\' windowSize '1sma\allfeatures.csv']);
sma = [sma predict_label];
csvwrite(['.\test features ' testname '\' windowSize '1sma\SMApredictionLabel.csv'],sma);

%we store the confusion matrix in cf
cf=[];
confusionmatrix =  confusionmat(testfile(:,size(testfile,2)-2), predict_label);
cf = [cf confusionmatrix];

save(['LOO' name '_' windowSize ' _' testname]);
beep on;
beep;
end