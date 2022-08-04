figure

%% create first plot
subplot(2,2,1);
plot(f,S1);
title('sensor one');
xlabel('Frequency(Hz)');
ylabel('Amplitude');

%% create second plot
subplot(2,2,2);
plot(f,S2,'green');
title('sensor two');
xlabel('Frequency(Hz)');
ylabel('Amplitude');

%% create third plot
subplot(2,2,3);
plot(f,S3,'red');
title('sensor three');
xlabel('Frequency(Hz)');
ylabel('Amplitude');

%% create fourth plot
subplot(2,2,4);
plot(f,S4);
title('sensor four');
xlabel('Frequency(Hz)');
ylabel('Amplitude');

%% create fifth plot
% subplot(2,3,5);
% plot(f,frff);
% title('frf');
% xlabel('frequency(Hz)');
% ylabel('amplitude');
