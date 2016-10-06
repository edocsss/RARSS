function [C G]=gridSearch(f1)
%gridSearch find the best Cost and Gamma for SVM using 5-folder cross validation
%validate input parameters

folder = [];
num = fix(size(f1, 1)/5);
for i = 1:5
    [f2 f1] = dividefile(f1, num);
    folder(:,:,i) = f2;
end
accMax = 0;
CMax = 0;
GMax = 0;
for c = -5:1:5
    for g = -5:1:5
        C=2^c;
        G=2^g;
        accLog =[];
        for i = 1:5
            f1 = [];
            for j=1:5
                if j~=i
                    f1 = [f1; folder(:,:,j)];
                end
            end
            f2 = folder(:,:,i);
            model = svmtrain(f1(:,size(f1,2)-2), f1(:,1:size(f1,2)-3), ['-c ' num2str(C) ' -g ' num2str(G)]);
            [predict_label, accuracy, dec_value] = svmpredict(f2(:,size(f2,2)-2), f2(:,1:size(f2,2)-3), model);
            accLog =[accLog accuracy];
        end
        
        if accMax < mean(accLog(1,:))
            accMax = mean(accLog(1,:));
            CMax = C;
            GMax = G;
        end
        
    end
end
C = CMax;
G = GMax;