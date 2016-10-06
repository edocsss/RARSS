function f = calculateFeature(window, frequency)
% compute the features
window(:,1)=[];
feature =[];

%comput the mean value
feature = [feature mean(window)];

%compute the cov value
temp = cov(window);

%compute the variance and coeff
for k = 1:size(temp,1)
    feature = [feature temp(k,k)];
end
for k = 1:size(temp,1)
    for m = k+1:size(temp,1)
        feature = [feature temp(k,m)];
    end
end

%compute the energy
t = fft(window);
t(1,:) = [];
t = abs(t);
feature = [feature sqrt(sum(t.^2)/size(t,1))];
sumt = sum(t);
for m = 1:size(t,2)
    if sumt(m)>0
        t(:,m) = t(:,m)/sumt(m);
    end
end

for n = 1:size(t,2)
    for m = 1:size(t,1)
        if t(m,n)~= 0
            t(m,n) = -1*t(m,n)*log(t(m,n));
        end
    end
end
feature = [feature sum(t)];

%compute SMA
x=0;
y=0;
z=0;
timeslice = 1000; %1seconds
interval = 1000/frequency; %preprocessed at 10Hz; value in ms
for item = 1:size(window,1)
    fn_x = abs(window(item,1));
    x = x + fn_x*interval;
    fn_y = abs(window(item,2));
    y = y + fn_y*interval;
    fn_z = abs(window(item,3));
    z = z + fn_z*interval;
end
sma= (1/timeslice)*(x+y+z);
feature = [feature sma];

f = feature;