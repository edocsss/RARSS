function [file1 file2] = dividefile(data, num)
%divide the data into two equal sized files randomly
%data----data to be divided
%num----number of data rows to split and store in file1

rows = size(data,1);
s = num;
index =zeros(rows,1);
for i = 1:s
    r = fix(rand(1)*size(data,1));
    while (r ==0 || index(r)== 1) && r<size(data,1) 
            r = r+1;
    end
    if index(r) ==1
        while  r>1 && index(r)==1
            r = r-1;
        end
    end
    
    index(r) = 1;
end

file1 =zeros(sum(index),size(data,2));
file2 =zeros(size(data));
m = 0;
n = 0;
for i = 1:length(index)
    if index(i) == 1
        m = m+1;
        file1(m,:)= data(i,:);
    else
        n = n+1;
        file2(n,:) = data(i,:);
    end
end
file1 = file1(1:m,:);
file2 = file2(1:n,:);       