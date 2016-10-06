tempX = csvread(['.\test cases_ucisvm\body_gyro_x_train.csv']);
tempY = csvread(['.\test cases_ucisvm\body_gyro_y_train.csv']);
tempZ = csvread(['.\test cases_ucisvm\body_gyro_z_train.csv']);
labels = csvread(['.\test cases_ucisvm\labels.csv']);
finalX = []; finalY=[]; finalZ=[];
for i=1:128
   linex = horzcat(tempX(:,i), labels);
   finalX = vertcat(finalX,linex);
   liney = horzcat(tempY(:,i), labels);
   finalY = vertcat(finalY,liney);
   linez = horzcat(tempZ(:,i), labels);
   finalZ = vertcat(finalZ,linez);
end
finalX(:,2)=[];
finalY(:,2)=[];
final = horzcat(finalX, finalY, finalZ);
csvwrite(['.\test cases_ucisvm\allFeatures_gyro.csv'], final);