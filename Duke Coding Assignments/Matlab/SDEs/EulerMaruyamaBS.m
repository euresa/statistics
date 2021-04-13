%Euler-Maruyama Method for Black-Scholes
%   Author: Samuel Eure

%Variables

N = 100;
T = 1;
x0 = 100;
sigma = 0.2;
mu = 0.8;

%Prepare Wierner Process

mystery = abs(N*rand); %set the state of the randn
randn('state',mystery); %set the state of the randn
dt = T/N;          
dW = zeros(1,N);
W  = zeros(1,N+1);
dW(1:N) = sqrt(dt)*randn(1,(N));
W(2:N+1) = cumsum(dW);
%
%Euler-Maruyama Method
X = zeros(1,N+1);
X(1) = x0; 
for n = 1:(N)
    X(n+1) =  X(n)*(1+dt*mu+sigma*(W(n+1)-W(n)));
end
x = 0:(T/N):(T);
%plot(x,X)
t = 1:(N+1);

Actual = x0*exp((sigma*W(t)+x(t)*(mu-sigma^2/2)));
plot(x,X,'*',x,Actual,'r--')
xlabel('time', 'FontSize', 30)
ylabel('X(t)   ','FontSize',30,'Rotation',90)
set(gca,'fontsize',30)
legend('EM Solution','Actual Solution','Location','southeast')

