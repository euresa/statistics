%Strong Convergence Euler-Maruyama/Milstein for Geometric Brownian Motion
%   SDE is of form dX = mu(X_t)(dt) + simga(X_t)(dW)
%   Plots Strong Error for different values of h (time steps) 
%   Uncomment line 36 to switch to Milstein
%   Author: Samuel Eure
%   Last Modified: 25 April, 2018


A = cumprod(zeros(1,13)+0.5);   %Creates an array of negative powers of 2
H = A(2:13);                    %Leaves out 1/2 for better presentation
T = 1;                          %Stop time from zero
M  = 1000;                      %Number of realizations
x0       = 100;                   %Initial condition
sigma    = 0.3;                 
mu       = 0.8;
AverageErrorForH  = zeros(length(H),1);

for k = 1:length(H)
    h = H(k);
    N = round(T/h);
    X = zeros(M,1);   %Numerical Approximation
    A = zeros(M,1);   %Analytical Solution
    for i = 1:M
        %Prepare Wierner Process
        dW = zeros(1,N+1);
        W  = zeros(1,N+1);
        dW(2:N+1) = sqrt(h)*randn(1,(N));
        W = cumsum(dW);
        %
        R         = zeros(1,N+1);
        R(1)      = x0; 
        Actual    = zeros(1,N+1);
        Actual(1) = x0;
        for n = 1:(N)
            R(n+1)  =  R(n)*(1+h*mu+sigma*(W(n+1)-W(n))); 
            %R(n+1)  =  R(n+1) + R(n)*0.5*sigma^2*((W(n+1)-W(n))^2-h);
            %Uncomment above for Milstein
            Actual(n+1) = x0*exp(sigma*W(n+1)+h*(n)*(mu-(sigma^2)/2));
        end
        X(i) = R(N+1);
        A(i) = Actual(N+1);
    end
    E        = abs((A-X)./A);
    AverageE = mean(E,1);
    AverageErrorForH(k)  = AverageE;
end

%Plotting specifications
loglog(H,AverageErrorForH, '*-', H, H.^(0.5),'m--', H, H,'black--', 'LineWidth', 2)
%title('Strong Con. for EM: dX = 0.8 X(t)dt + 0.2 X(t)dW_t ,  x_0 = 4')
%title('Strong Con. for Milstein: dX = 0.8 X(t)dt + 0.2 X(t)dW_t ,  x_0 = 4')
xlabel('h')
ylabel('Expected Error','Rotation',90)
set(gca,'fontsize',30)
legend('Error at time T', 'slope = 1/2', 'slope 1','Location','southeast')

