
%% select the newest csv file
filename = fileNames("./",".csv");
lastof = filename.size();

%% create data length based off seconds sampled and sample frequency
fs = 19230;
sec = 5;
L = sec*fs;

A = readmatrix(filename(1));  %read csv

%% split up the data
x = A(:,1);
s1 = A(:,2);
s2 = A(:,3);
s3 = A(:,4);
s4 = A(:,5);

%% change data from 25x1 double to 1x25 double
s1 = s1';
s2 = s2';
s3 = s3';
s4 = s4';


%% fft + absolte value to get rid of complex numbers
f = fs*(0:(L/2))/L;
S1 = abs(fft(s1));
S2 = abs(fft(s2));
S3 = abs(fft(s3));
S4 = abs(fft(s4));
f = f(1,1:25);

%% FRFs that are possible
% S12 = S1/S2;
% S13 = S1/S3;
% S14 = S1/S4;
% S21 = S2/S1;
% S31 = S3/S1;
% S41 = S4/S1;
% S23 = S2/S3;
% S32 = S3/S2;
% S24 = S2/S4;
% S42 = S4/S2;
% S34 = S3/S4;
% S43 = S4/S3;


%% plot 
sensorplot

