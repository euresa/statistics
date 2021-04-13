%Weak Convergence for Euler-Maruyama and Milstein on Geomentric BM 
%   SDE is of form dX = mu(X_t)(dt) + simga(X_t)(dW)
%   Simply uncomment line 25 to switch from EM to Milstein (Change Plot)
%   Author: Samuel Eure
%   Last Modified: 25 April, 2018


%Parameters
mu = 0.8; 
sigma = .1; 
Xzero = 1;     %Initial condition
T = 1;
M = 400000;    %number of samples (Recommended over 100,000)
H = cumprod(zeros(1,12)+0.5);  %Different negative powers of 2
H = H(5:12);
Xem = zeros(length(H),1);

for i = 1:length(H)
    h = H(i);
    N = T/h;
    Xtemp = Xzero*ones(M,1);
    for j = 2:N
        W = sqrt(h)*randn(M,1);
        Xtemp = Xtemp + h*mu*Xtemp + sigma*Xtemp.*W;
        Xtemp = Xtemp + 0.5*sigma^2*(W.^2 - h);     %Milstein
    end
    Xem(i) = mean(Xtemp);
end


%Plotting specifications
X_Error = abs(Xem - exp(mu));
loglog(H, X_Error,'black*-', H, H,'r--', 'LineWidth', 2)
xlabel('h', 'FontSize', 35)
ylabel('abs( E[S(T)] - E[X(T)] )', "FontSize", 35)
set(gca,'fontsize',35)
%legend('Expected error at time T for EM','slope 1','Location','southeast')
%title('Weak Error for EM','FontSize', 30)
legend('Error at time T for Milstein','slope 1','Location','southeast')
%title('Weak Error for Milstein','FontSize', 30)

