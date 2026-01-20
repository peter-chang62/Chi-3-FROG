%% Generate time and frequency
N = 256/2;
Np = 100;
T = 100;
time = linspace(-T,T,N);
time = time*1e-15;
dt = time(2)-time(1);
F = (-N/2:N/2-1);
F =  fftshift( F/dt/N );
% Load pulse bank, 100 random pulses
load('pulse_set.mat');

%% Make PG FROG trace
    pulse = pulse_set(55, :);              % choose pulse #55. You can choose another pulse from the bank or use your own pulse here
    gate = pulse_set(7, :);                  % choose gate #7. You can choose another gate from the bank or use your own gate here
    DelayStep = 1;                             % choose delay step = DelayStep*dt
    ind = 1:DelayStep:N;                    
    Ns = numel(ind); 
    D = time(ind);
    I = zeros(N, Ns);
    for ik=1:Ns
        gate_tau = ifft( fft(gate).*exp(1i*2*pi*D(ik)*F) );
        I(:, ik) = fftshift( abs(fft(abs(gate_tau).^2.*pulse)/N) );
    end
Inoisy = awgn(I, 15, 'measured');
FreqFilter = 100e13;                                               % Use only frequencies < FreqFilter
Fsupp = (abs(F)<FreqFilter)';
LPF = kron(ones(1,size(I,2)), fftshift(Fsupp));
InoisyLPF = Inoisy.*LPF;
etta = sum(Fsupp)/N;

ref = conj(pulse');
Terror = inf;
%%  Run algorithm
for ni=1:10   % number of random realizations
         PulseGuess = zeros(size(time))';
         FWHM = (max(time)-min(time))*(rand(1,1));
         GateGuess =  exp(-2.77*(time/FWHM).^2)';
        [Obj, Gate, error, Irec] = ePIE_fun_PG_FROG(InoisyLPF, D, PulseGuess, GateGuess, 100, Fsupp, F', time, 1e-3);
            flag = error(find(error, 1, 'last'))<1e-3;
            if flag
                ObjB = best_sol(Obj, ref);
                Aerror = acos(abs(ObjB'*ref)/sqrt( (ObjB'*ObjB)*(ref'*ref) ));
                break
            end
            if Terror > error(find(error, 1, 'last'))
                Terror = error(find(error, 1, 'last'));
                ObjB = best_sol(Obj, conj(pulse'));
                Aerror = acos(abs(ObjB'*ref)/sqrt( (ObjB'*ObjB)*(ref'*ref) ));
            end
 end
%% Plot figures
ObjB = ObjB/sqrt(sum( abs(ObjB).^2 ));
delta = acos(abs(ObjB'*ref)/sqrt( (ObjB'*ObjB)*(ref'*ref) ));
figure(2)

subplot(3, 2, 1); imagesc(time*1e15, fftshift(F)*1e-15, I)
xlabel('Time [fsec]','FontSize',16); ylabel('Freq.[THz]','FontSize',16);
title('Simulated trace')

subplot(3, 2, 2); imagesc(time*1e15, fftshift(F)*1e-15, Inoisy)
xlabel('Time [fsec]','FontSize',16); ylabel('Freq.[THz]','FontSize',16);
title('Simulated noisy trace')

subplot(3,2,3)
plot(time*1e15, abs(ObjB), 'DisplayName','Recovered')
xlabel('Time [fsec]','FontSize',16); ylabel('Amplitude [a.u.]','FontSize',16);
hold all
plot(time*1e15, abs(ref), 'DisplayName','Original')
xlabel('Time [fsec]','FontSize',16); ylabel('Amplitude [a.u.]','FontSize',16);
legend show
subplot(3,2,4)
plot(time*1e15, unwrap(   angle(ObjB)   )/pi, 'DisplayName','Recovered')
xlabel('Time [fsec]','FontSize',16); ylabel('Phase [pi]','FontSize',16);
hold all
plot(time*1e15, unwrap(   angle(ref)   )/pi, 'DisplayName','Original')
xlabel('Time [fsec]','FontSize',16); ylabel('Phase [pi]','FontSize',16);
legend show

subplot(3,2,5)
imagesc(time*1e15, fftshift(F)*1e-15, InoisyLPF)
xlabel('Time [fsec]','FontSize',16); ylabel('Freq.[THz]','FontSize',16);
title('Used trace')

subplot(3, 2, 6); imagesc(time*1e15, fftshift(F)*1e-15, Irec)
xlabel('Time [fsec]','FontSize',16); ylabel('Freq.[THz]','FontSize',16);
title('Reconstructed trace')
suptitle( sprintf('delta = %.3f', delta) )
