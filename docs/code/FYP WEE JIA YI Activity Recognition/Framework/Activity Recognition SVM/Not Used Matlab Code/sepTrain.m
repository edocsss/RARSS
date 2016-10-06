clc;
clear;
data = csvread('.\test features\41\allFeatures.csv');

for pos = 1:6
    for neg = (pos+1):6
        posAct = pos;
        negAct = neg;
        
        idx = find(data(:,23)==posAct | data(:,23)==negAct);
        temp = data(idx,1:23);
                
        for i =1:size(temp,1)
            if temp(i,23)==posAct
                temp(i,23)=1;
            elseif temp(i,23)==negAct
                temp(i,23)=-1;
            end
        end
        
        s = fix(size(temp)/5);
        [file1 file2] = dividefile(temp, s);
        
        l = file2(:,23);
        f = file2(:,1:22);
        
        fs = sparse(f);
        
        libsvmwrite(['.\Tmp\' num2str(posAct) num2str(negAct) '.train'], l, fs);
        
        l = file1(:,23);
        f = file1(:,1:22);
        
        fs = sparse(f);
        
        libsvmwrite(['.\Tmp\' num2str(posAct) num2str(negAct) '.test'], l, fs);
        
        system(['bvm_train.exe -c 100 .\Tmp\' num2str(posAct) num2str(negAct) '.train ' num2str(posAct) num2str(negAct) '.mdl']);

        system(['bvm_predict.exe .\Tmp\' num2str(posAct) num2str(negAct) '.test ' num2str(posAct) num2str(negAct) '.mdl result.txt']);
    end
end
