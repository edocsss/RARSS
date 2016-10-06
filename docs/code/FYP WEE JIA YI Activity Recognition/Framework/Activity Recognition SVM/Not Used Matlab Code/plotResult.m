data = textread('result.txt', '', 'delimiter', ' ');
accLog = [];
for a = 1:8
    idx = find(data(:,2)==a);
    temp = data(idx,[1,3]);
    temp = sortrows(temp,1);
    temp(:,2) = 1-temp(:,2);
    accLog =[accLog temp(:,2)];
%     plot(temp(:,1), temp(:,2));
%     hold on;
end