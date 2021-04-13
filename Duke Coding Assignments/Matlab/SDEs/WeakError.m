%Error Analysis of Euler-Maruyama Method for Black-Scholes
%   Plots the expected path of a geometric brownian process
%   The number of sampled paths as well as steps (samples, N) is
%   changeable
%   Author: Samuel Eure

%Variables
%set the state of the randn
N = 10;
T = 1;
x0 = 100;
sigma = 0.2;
mu = 0.8;

samples = 1000;
S = zeros(samples,N+1);
A = zeros(samples,N+1);
for i = 1:samples
    %Prepare Wierner Process
    randn('state',abs(round(12000*rand*rand))) %set the state of the randn
    mystery = abs(N*rand);
    randn('state',mystery); %set the state of the randn
    dt = T/(N); 
    dW = zeros(1,N+1);
    W  = zeros(1,N+1);
    dW(2:N+1) = sqrt(dt)*randn(1,(N));
    W = cumsum(dW);
    %
    %Euler-Maruyama Method
    X = zeros(1,N+1);
    X(1) = x0; 
    Actual = zeros(1,N+1);
    Actual(1) = x0;
    for n = 1:(N)
        X(n+1) =  X(n)*(1+dt*mu+sigma*(W(n+1)-W(n)));
        Actual(n+1) = x0*exp(sigma*W(n+1)+dt*(n)*(mu-(sigma^2)/2));
    end
    S(i,:) = X;
    A(i,:) = Actual;
end

x = 0:(T/N):(T);
S = sum(S,1);
S = S/samples;
A = sum(A,1);
A = A/samples;
y = (1:(N+1))*dt;
plot(x,(A-S)./A*100)%Standard relative error
xlabel('t', 'FontSize', 20)
ylabel('Percent Relative Error','FontSize',20,'Rotation',90)
set(gca,'fontsize',20)
legend('Weak Error','Location','southeast')