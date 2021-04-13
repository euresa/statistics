%EM/Milstein Scheme for solving Geometric Brownian Motion for SDEs
%   SDE is of form dX = mu(X_t)(dt) + simga(X_t)(dW)
%   Uncomment line 27 to switch to Milstein
%   Author: Samuel Eure
%   Last Modified: 25 April, 2018

%Parameters
T = 1;
h = 10^-2;
x0 = 100;
mu = 0.8;
sigma = 0.3;
N = round(T/h);

%Prepare Wiener Process
dW = zeros(1,N+1);
W  = zeros(1,N+1);
dW(2:N+1) = sqrt(h)*randn(1,(N));
W = cumsum(dW);

%Milstein Implementation
X = zeros(1,N+1);
X(1) = x0; 
for n = 1:(N)
    X(n+1) = X(n)*(1 + (mu)*h + sigma*(W(n+1)-W(n)));
    %Uncomment below for Milstein
    X(n+1) = X(n+1) + X(n)*0.5*sigma^2*((W(n+1)-W(n))^2-h);
end


%Plotting specifications
x = 0:(T/N):(T);
t = 1:(N+1);
Actual = x0*exp((sigma*W(t)+x(t)*(mu-sigma^2/2)));
plot(x,X,'*',x,Actual,'r', "LineWidth", 1)
%title('Euler-Maruyama Solution (h = 0.01): dX = 0.8 X(t)dt + 0.2 X(t)dW_t')
%title('Milstein Solution (h = 0.001): dX = 0.8 X(t)dt + 0.2 X(t)dW_t')
xlabel('time', 'FontSize', 30)
ylabel('X(t)   ','FontSize',30,'Rotation',90)
set(gca,'fontsize',30)
%legend('EM Solution','Actual Solution','Location','southeast')
legend('Milstein Solution','Actual Solution','Location','southeast')