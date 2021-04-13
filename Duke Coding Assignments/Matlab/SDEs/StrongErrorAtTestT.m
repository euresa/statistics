%Modified Error Anlaysis @ T = 0.5

%Error Analysis of Euler-Maruyama Method for Black-Scholes
%   Plots the expected path of a geometric brownian process
%   The number of sampled paths as well as steps (samples, N) is
%   changeable
%   Author: Samuel Eure

%Variables
%set the state of the randn

H = cumprod(zeros(1,13)+0.5);
H = H(4:13);
T = 1;

samples  = 5000;

testT    = T;
x0       = 20;
sigma    = 3.5;
mu       = .5;
AverageErrorForH  = zeros(length(H),1);

for k = 1:length(H)
    h = H(k);
    N = round(T/h);
    X = zeros(samples,1);
    A = zeros(samples,1);
    for i = 1:samples
        %Prepare Wierner Process
        mystery = abs(N*rand);
        randn('state',mystery); %set the state of the randn
        dW = zeros(1,N+1);
        W  = zeros(1,N+1);
        dW(2:N+1) = sqrt(h)*randn(1,(N));
        W = cumsum(dW);
        %
        %Euler-Maruyama Method
        R         = zeros(1,N+1);
        R(1)      = x0; 
        Actual    = zeros(1,N+1);
        Actual(1) = x0;
        for n = 1:(N)
            R(n+1)      =  R(n)*(1+h*mu+sigma*(W(n+1)-W(n)));
            Actual(n+1) = x0*exp(sigma*W(n+1)+h*(n)*(mu-(sigma^2)/2));
        end
        X(i,1) = R(round(testT(1)*N));      
        A(i,1) = Actual(round(testT(1)*N));
    end
    E        = abs((A-X)./A);
    AverageE = mean(E,1);
    AverageErrorForH(k)  = AverageE;
end
%Plotting Errors
loglog(H,AverageErrorForH, '*-', 'LineWidth', 3) 
hold on
loglog(H, 10*H.^(0.5),'m--',H,10*H,'black--', 'LineWidth', 2) 
hold off
title('Strong Con. for EM: dX = 0.5 X(t)dt + 3.5 X(t)dW_t, x_0 = 20')
xlabel('h')
ylabel('Expected Error','Rotation',90)
set(gca,'fontsize',35)
legend('Error at time T', 'slope 1/2','slope 1','Location','southeast')

