%Error Analysis

%Error Analysis of Euler-Maruyama Method for Black-Scholes
%   Plots the expected path of a geometric brownian process
%   The number of sampled paths as well as steps (samples, N) is
%   changeable
%   Author: Samuel Eure

%Variables
%set the state of the randn
nValues = 10:10:500;
T = 1;
x0 = 100;
sigma = 0.2;
mu = 0.8;

samples = 1000;
maxError = zeros(1,length(nValues));
MWE = zeros(1,length(nValues));

for k = 1:length(nValues)
    N = nValues(k);
    S = zeros(samples,N+1);
    A = zeros(samples,N+1);
    for i = 1:samples
        %Prepare Wierner Process
        randn('state',abs(round(12000*rand*rand))); %set the state of the randn
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
    SE = (A-S)./A;
    SE = sum(SE,1)/samples;
    maxError(k) = max(abs(SE));
    WS = sum(S,1)/samples;
    WA = sum(A,1)/samples;
    assignment = max(abs((WA-WS)./WA));
    MWE(k)  = max(abs((WA-WS)./WA));
end
%Plotting Errors
plot(nValues,maxError)
xlabel('N', 'FontSize', 20)
ylabel('Maximum Strong Error','FontSize',20,'Rotation',90)
set(gca,'fontsize',20)

