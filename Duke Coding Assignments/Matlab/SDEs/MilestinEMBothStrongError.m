%Strong Convergence for Milstein vs Euler-Maruyama Method for GBM
%   SDE is of form dX = mu(X_t)(dt) + simga(X_t)(dW)
%   Plots Strong Error for different values of h (time steps) 
%   Author: Samuel Eure
%   Last Modified: 25 April, 2018
%   Author: Samuel Eure

%Parameters
A = cumprod(zeros(1,13)+0.5);   %Different time step values (h)
H = A(7:13);
T = 1;
M  = 1000;
x0       = 100;
sigma    = 0.3;
mu       = 0.8;


AverageErrorForH  = zeros(length(H),2);
for k = 1:length(H)
    h = H(k);
    N = round(T/h);
    X = zeros(M,2);
    A = zeros(M,2);
    for i = 1:M   
        %Prepare Wierner Process
        dW = zeros(1,N+1);
        W  = zeros(1,N+1);
        dW(2:N+1) = sqrt(h)*randn(1,(N));
        W = cumsum(dW);
        %
        Mil         = zeros(1,N+1);
        EM = zeros(1,N+1);
        Mil(1)      = x0; 
        EM(1) = Mil(1);
        Actual    = zeros(1,N+1);
        Actual(1) = x0;
        for n = 1:(N)   
            Mil(n+1)  =  Mil(n)*(1+h*mu+sigma*(W(n+1)-W(n)));
            EM(n+1) =  EM(n)*(1+h*mu+sigma*(W(n+1)-W(n)));
            Mil(n+1)  =  Mil(n+1) + Mil(n)*0.5*sigma^2*((W(n+1)-W(n))^2-h); 
            Actual(n+1) = x0*exp(sigma*W(n+1)+h*(n)*(mu-(sigma^2)/2));
        end
        X(i,1) = Mil(N+1);
        X(i,2) = EM(N+1);
        A(i,1) = Actual(N+1);
        A(i,2) = Actual(N+1);
    end
    E        = abs((A-X)./A);
    AverageE = mean(E,1);
    AverageErrorForH(k,:)  = AverageE;
end
%Plotting Errors
loglog(H,AverageErrorForH, '*-', H, 0.06*H.^(0.5),'m--', H, 0.35*H,'black--', 'LineWidth', 2)
%title('Strong Con. for Milstein: dX = 0.8 X(t)dt + 0 X(t)dW_t ,  x_0 = 20')
xlabel('h')
ylabel('Expected Error','Rotation',90)
set(gca,'fontsize',30)
legend('Milstein Error at T',"EM Error at T", 'slope = 1/2', 'slope 1','Location','southeast')

