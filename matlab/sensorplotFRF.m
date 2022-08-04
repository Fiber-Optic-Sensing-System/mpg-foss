% This code will plot all 12 variations of the FRFs possible
figure
%% first plot
subplot(3,4,1);
plot(f,S12);
title('FRF of sensor 1&2');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% second plot
subplot(3,4,2);
plot(f,S13);
title('FRF of sensor 1&3');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% thrid plot
subplot(3,4,3);
plot(f,S14);
title('FRF of sensor 1&4');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% fourth plot
subplot(3,4,4);
plot(f,S21);
title('FRF of sensor 2&1');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% fifth plot
subplot(3,4,5);
plot(f,S31);
title('FRF of sensor 3&1');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% sixth plot
subplot(3,4,6);
plot(f,S41);
title('FRF of sensor 4&1');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% seventh plot
subplot(3,4,7);
plot(f,S23);
title('FRF of sensor 2&3');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% eigth plot
subplot(3,4,8);
plot(f,S32);
title('FRF of sensor 3&2');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% ninth plot
subplot(3,4,9);
plot(f,S24);
title('FRF of sensor 2&4');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% tenth plot
subplot(3,4,10);
plot(f,S42);
title('FRF of sensor 4&2');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% first plot
subplot(3,4,1);
plot(f,S12);
title('FRF of sensor 1&2');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% eleventh plot
subplot(3,4,11);
plot(f,S34);
title('FRF of sensor 3&4');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

%% twelth plot
subplot(3,4,12);
plot(f,S43);
title('FRF of sensor 4&3');
ylabel('Amplitude');
xlabel('Frequency(Hz)');

