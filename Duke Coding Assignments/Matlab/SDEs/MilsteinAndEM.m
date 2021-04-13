%Both EM and Milstein

%Strong Error for Milstein

%Modified Error Anlaysis @ T = 0.5

%Error Analysis of the Milstein Scheme for Black-Scholes
%   Plots the expected path of a geometric brownian process
%   The number of sampled paths as well as steps (samples, N) is
%   changeable
%   Author: Samuel Eure

%Variables
%set the state of the randn

A = cumprod(zeros(1,10)+0.5);
H = A(2:10);
T = 1;

samples  = 10;

testT    = [T,T];
x0       = 3;
sigma    = .7;
mu       = 0.75;
Euler  = zeros(length(H),1);
Milstein = zeros(length(H),1);

for k = 1:length(H)
    h = H(k);
    N = round(T/h);
    X = zeros(samples,2);
    A = zeros(samples,2);
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
        M         = zeros(1,N+1);
        EM        = zeros(1,N+1);
        EM(1)      = x0; 
        M(1)      = EM(1);
        Actual    = zeros(1,N+1);
        Actual(1) = x0;
        for n = 1:(N)
            EM(n+1)  =  EM(n)*(1+h*mu+sigma*(W(n+1)-W(n)));
            M(n+1)  =   EM(n+1) + 0.5*sigma*((W(n+1)-W(n))^2-h); 
            Actual(n+1) = x0*exp(sigma*W(n+1)+h*(n)*(mu-(sigma^2)/2));
        end
        X(i,1) = M(round(testT(2)*N));
        X(i,2) = EM(round(testT(2)*N));
        A(i,1) = Actual(round(testT(2)*N));
        A(i,2) = Actual(round(testT(2)*N));
    end
    E        = abs((A-X)./A);
    AverageE = mean(E,1);
    AverageErrorForH(k,:)  = AverageE;
end
%Plotting Errors
loglog(H,AverageErrorForH, '*-', H, H.^(0.5),'m--', H, H,'black--', 'LineWidth', 2)
title('Strong Con. for Milstein vs. EM: dX = 3 X(t)dt + 0.1 X(t)dW_t')
xlabel('h')
ylabel('Expected Error','Rotation',90)
set(gca,'fontsize',30)
legend('t = T/2', 't = T', 'slope 1/2','slope 1','Location','southeast')

