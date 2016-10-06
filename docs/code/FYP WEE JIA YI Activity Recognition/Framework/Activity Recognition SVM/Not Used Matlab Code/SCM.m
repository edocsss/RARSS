function scm(frame_size, withLen)

data = csvread(['.\test features\' num2str(frame_size) num2str(withLen) '\allFeatures.csv']);

data = sortrows(data,size(data,2)-1);

i = 1;
while data(i,size(data,2)-1)<=6
    i = i+1;
end

i = i-1;

data = data(1:i,:);

if isdir('SCMC++Data') == 0;
    mkdir('SCMC++Data');
end

%divide the file into 5 folders
temp = data;
s = fix(size(temp,1)/5);
for i = 1:5
    [file1 temp] = dividefile(temp,s);
    folder(:,:,i) = file1;
end
for i = 1:5
    file1 = [];
    for j=1:5
        if j~=i
            file1 = [file1; folder(:,:,j)];
        end
    end
    file2 = folder(:,:,i);


    if isdir(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) ]) ==0
        mkdir(['.\SCMC++Data\' num2str(frame_size) num2str(withLen)]);
    end

    if isdir(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) '\' num2str(i)]) ==0
        mkdir(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) '\' num2str(i)]);
    end

%     csvwrite(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) '\' num2str(i) '\testing.csv'],  file2);
    %file1 is the training dataset; file2 is the testing data set
    
    dim = size(file2,2)-3;
    
    fid = fopen(['.\SCMC++Data\' num2str(frame_size) num2str(withLen) '\' num2str(i) '\testing.txt'],'w');
    
    fprintf(fid, '%d\n%d\n', size(file2,1), dim);
    
    for j = 1: size(file2,1)
        %     if data(i,dim+1)== 1
        %         fprintf(fid,'%d ',1);
        %     else
        %         fprintf(fid,'%d ',-1);
        %     end
        
        fprintf(fid, '%d ', file2(j,dim+1));
        %     fprintf(fid, '%d ', data(i,dim+1));
        for k=1:dim
            fprintf(fid, '%f ', file2(j,k));
        end
        fprintf(fid, '\n');
    end
    
    fclose(fid);
    
    
    temp = file1(:,1:size(file1,2)-2);
    temp = sortRows(temp,size(temp,2));

    while size(temp,1)>1
        tag = temp(1,size(temp,2));
        index = 1;
        while index< size(temp,1) && temp(index+1, size(temp,2)) == tag
            index = index + 1;
        end
        %     index = index-1;

        clusterData = temp(1:index,1:size(temp,2)-1);
        temp(1:index,:)=[];

        TOD_Clustering(clusterData, frame_size, withLen, i, tag);
    end
end