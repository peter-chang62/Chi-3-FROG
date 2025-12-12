%% ePIE function for PG FROG 
function [Obj, Prob, error, Ir] = ePIE_fun_PG_FROG(I, D, PulseGuess, GeteGues, iterMax, Fsupp, F, time, STOPc)
% reconstructs a pulse function (in time) from a PG FROG
%   trace by use of the Ptychographic algorithm.
%
%Usage:
%
%   [Obj, error, Ir] = ePIE_fun_FROG_sp(I, D, iterMax, Fsupp, F, time, STOPc, spec)
%
%%       Output:
%       Obj      =   Reconstructed pulse field (in time).         E(t)
%       Prob      =   Reconstructed Gate intensity (in time) |G(t)|^2.
%       Ir      =   reconstructed FROG trace.
%       error     =   vector of errors for each iteration
%
%%      Input:
%       I       =   Experimental / Simulated SHG FROG Trace
%		D	=	vector of delays which coresponds to trace.
%       iterMax =   Maximum number of iterations allowed (default = 1000).
%       Fsupp = vector of informative frequencies (logical).
%       F = vector of frequencies.
%       time = coresponding vector in time domain (Fourier related to F).
%       STOPc  =   (Optioanl) Tolerence on the error (default = 1e-5).

%%   Set maximum number of iterations
if (~exist('iterMax', 'var')||isempty(iterMax))
    iterMax = 1000;
end

%   Set convergence limit
if (~exist('STOPc', 'var')||isempty(STOPc))
    STOPc = 1e-5;
end


[N, K] = size(I);

Obj = PulseGuess;
Prob = GeteGues;
iterG = 3;
error = zeros(iterMax, 1);
iter = 1;
Ir = zeros(size(I));

while iter <= iterMax
    s = randperm(K);
    alpha = abs( 0.2+randn(1,1)/20 );
    for iterK =1:K
        
        temp = sig_shift(Prob, D(s(iterK)), F);
        psi = Obj.*temp;
        psi_n = fft(psi)/N;
        phase = exp(1i*angle(psi_n));
        amp = fftshift( I(:, s(iterK)) );
        psi_n(Fsupp) = amp(Fsupp).*phase(Fsupp);
        psi_n = ifft(psi_n)*N;
        
            Uo = conj(temp)./max( (abs(temp).^2) );
            Obj = Obj +  alpha.*Uo.*(psi_n - psi) ;
            if iter > iterG
                Up = conj(Obj)./max( (abs(Obj).^2) );
                temp = temp +  alpha.*Up.*(psi_n - psi);
                Prob = real( sig_shift(temp, -D(s(iterK)), F));
            end
            
%         experimental soft thresholding, uncomment 3 following lines for try
%             gamma = 1e-7;
%             Obj = SoftTH(Obj, gamma);
%             Prob = SoftTH(Prob, 2*gamma);
            
        Ir(:, s(iterK)) = abs( fftshift( fft(Obj.*temp)/N ) );
        
        
        
        
            if mod(iterK,K)== 0
                error(iter) = sqrt(sum(sum( abs(Ir(fftshift(Fsupp),:)-I(fftshift(Fsupp),:) ).^2 )))/sqrt(sum(sum( abs(I(fftshift(Fsupp),:) ).^2 )));
                fprintf('Iter:%d   IterK:%d alpha=%d Error=%d\n',iter, iterK, alpha, error(iter));
                
                subplot(3,2,1); 
                p1 = plot(time*1e15, abs(Obj), 'LineWidth',2);
                xlabel('Time [fsec]','FontSize',16); ylabel('Amplitude [a.u.]','FontSize',16);
%                 xlim([-1e-13 1e-13]);
                title('Amplitude Pulse');
                
                subplot(3,2,2)
                p2 = plot(time*1e15, unwrap(angle(Obj))/pi, 'LineWidth',2);
                xlabel('Time [fsec]','FontSize',16); ylabel('Phase [Pi]','FontSize',16);
%                 xlim([-1e-13 1e-13]);
                title('Phase Pulse');
                
                subplot(3,2,3:4); 
                p3 = plot(time*1e15, Prob, 'LineWidth',2);
                xlabel('Time [fsec]','FontSize',16); ylabel('Intensity [a.u.]','FontSize',16);
%                 xlim([-1e-13 1e-13]);
                title('Intensity Gate');

                subplot(3,2,5)
                imagesc(time*1e15, fftshift(F)*1e-12, I.*kron(fftshift(Fsupp), ones(1, K)) );title('Used I');
                xlabel('Time [fsec]','FontSize',16); ylabel('Freq.[THz]','FontSize',16);

                subplot(3,2,6)
                imagesc(time*1e15, fftshift(F)*1e-12, Ir);title('Recovered I');
                xlabel('Time [fsec]','FontSize',16); ylabel('Freq.[THz]','FontSize',16);
                pause(0.01);
            end
        
        
    end
    if error(iter)<STOPc || isnan(error(iter))
        return;
    end

    iter = iter+1;

end


    function [sig_out] = sig_shift(sig_in, d, F)
        sig_out = ifft( fft(sig_in).*exp(1i*2*pi*d*F) );
    end

    function [sig_out] = SoftTH(sig_in, gamma)
        sig_out = ( real(sig_in) - gamma * sign(real(sig_in)) ).*(abs(sig_in) >= gamma)+...
                             1i*( imag(sig_in) - gamma * sign(imag(sig_in)) ).*(abs(sig_in) >= gamma) ;
    end

end