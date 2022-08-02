figure

%% create first plot
subplot(2,2,1);
plot(f,S1);
title('sensor one');
xlabel('frequency(Hz)');
ylabel('amplitude');

%% create second plot
subplot(2,2,2);
plot(f,S2,'green');
title('sensor two');
xlabel('frequency(Hz)');
ylabel('amplitude');

%% create third plot
subplot(2,2,3);
plot(f,S3,'red');
title('sensor three');
xlabel('frequency(Hz)');
ylabel('amplitude');

%% create fourth plot
subplot(2,2,4);
plot(f,S4);
title('sensor four');
xlabel('frequency(Hz)');
ylabel('amplitude');

%% create fifth plot
% subplot(2,3,5);
% plot(f,frff);
% title('frf');
% xlabel('frequency(Hz)');
% ylabel('amplitude');
