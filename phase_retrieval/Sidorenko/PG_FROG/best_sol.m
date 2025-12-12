function [pulse] = best_sol(obj, ref)
usfac = 100;
[output(1,:), ~] = dftregistration(fft(obj),fft(ref),usfac);
[output(2,:), ~] = dftregistration(fft(-conj(obj)),fft(ref),usfac);
[output(3,:), ~] = dftregistration(fft(obj(end:-1:1)),fft(ref),usfac);
[output(4,:), ~] = dftregistration(fft(-conj(obj(end:-1:1))),fft(ref),usfac);
[~, Imin] = min(output(:,1));

N=size(ref,1);
Nr = ifftshift([-fix(N/2):ceil(N/2)-1]);
Nr = meshgrid(Nr);
Nr = Nr(1,:)';
switch Imin
    case 1
        pulse = ifft(fft( obj ).*exp(1i*2*pi*(output(Imin,3)*Nr/N))).*exp(-1i*output(Imin,2));
    case 2
        pulse = ifft(fft( -conj(obj) ).*exp(1i*2*pi*(output(Imin,3)*Nr/N))).*exp(-1i*output(Imin,2));
    case 3
        pulse = ifft(fft( obj(end:-1:1) ).*exp(1i*2*pi*(output(Imin,3)*Nr/N))).*exp(-1i*output(Imin,2));
    case 4
        pulse = ifft(fft( -conj(obj(end:-1:1)) ).*exp(1i*2*pi*(output(Imin,3)*Nr/N))).*exp(-1i*output(Imin,2));
end


end