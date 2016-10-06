function TOD_Clustering(data, frame_size, withLen, directory, class)
%TOD_CLUSTERING     cluster data with Threshold Order-dependent algorithm.
temp = data;
THRESHOLD = 0.2;
% for THRESHOLD = 0.2:0.05:0.5
data = temp;
if size(data,1)>1
    labels = zeros(size(data,1),1);
    centers = zeros(size(data));
    centerIdx = 1;
    centers(centerIdx,:) = data(1,:);
    labels(1)=1;
    %clustering begins
    for i = 2:size(data,1)
        %find the minimum distance between this point and all the centers
        minDist = pdist([data(i,:); centers(1,:)]);
        label = 1;
        for j = 2:centerIdx
            len = pdist([data(i,:); centers(j,:)]);
            if len<minDist
                minDist = len;
                label = j;
            end
        end
        %check whether it's a new center or just belong to one cluster
        if minDist < THRESHOLD
            labels(i) = label;
        else
            centerIdx = centerIdx+1;
            centers(centerIdx,:) = data(i,:);
            labels(i) = centerIdx;
        end
    end
    centers =  centers(1:centerIdx,:);
    %output the information for each cluster
    data = [data labels];
    data = sortRows(data,size(data,2));
    
    head = 1;
    tail = 1;
    sta = tabulate(data(:,size(data,2)));
    totalNum = 0;
    centerNum = 0;
    for i=1:size(sta,1)
        if sta(i,2)>1
            totalNum = totalNum + sta(i,2);
            centerNum = centerNum+1;
        end
    end
    
    
    
    %clustering end, start to calcualte the arrays.
    if isdir(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) '\' num2str(directory) ]) ==0
        mkdir(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) '\' num2str(directory)]);
    end

    fid = fopen(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) '\' num2str(directory) '\' num2str(class) '.txt'],'w');
    fprintf(fid, '%d\n', totalNum);
    fprintf(fid, '%d\n', size(centers,2));
    fprintf(fid, '%d\n', centerNum);
    for i = 1:size(sta,1)
        %find the cluster
        tail = head + sta(i,2)-1;
        num = sta(i,2);
        
        clust = data(head:tail,1:size(data,2)-1);
        head = tail+1;
        %output the cluster information
        if num>1
            fprintf(fid, '%f\n', num/totalNum);
            meanV = mean(clust);
            for j = 1:length(meanV)
                fprintf(fid, '%f ', meanV(j));
            end
            fprintf(fid, '\n');
            
            covV = cov(clust);
            for j = 1:size(covV,1)
                %                 for m = 1:size(covV,2)
                fprintf(fid, '%f ', covV(j,j));
                %                 end
            end
            fprintf(fid, '\n');
        end
    end
    fclose(fid);
end
% end


