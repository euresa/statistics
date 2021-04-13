%Milstein Scheme and EM
%solves SDEs using the Milstein Scheme
%   Author: Samuel Eure

T = 1;
h = 0.001;
x0 = 20;
mu = 0.1;
sigma = 4;

N = round(T/h);


mystery = abs(N*rand);
randn('state',mystery); %set the state of the randn
dW = zeros(1,N+1);
W  = zeros(1,N+1);
dW(2:N+1) = sqrt(h)*randn(1,(N));
W = cumsum(dW);
X = zeros(2,N+1);
X(1:2,1) = x0; 
for n = 1:(N)
    X(1,n+1) = X(1,n)*(1 + (mu)*h + sigma*(W(n+1)-W(n)));
    X(1,n+1) = X(1,n+1) + X(1,n)*0.5*sigma^2*((W(n+1)-W(n))^2-h);
    X(2,n+1) = X(2,n)*(1 + (mu)*h + sigma*(W(n+1)-W(n)));
end

x = 0:(T/N):(T);
t = 1:(N+1);
Actual = x0*exp((sigma*W(t)+x(t)*(mu-sigma^2/2)));
plot(x,X(2,:), 'black-', 'LineWidth',4)
hold on
plot(x,X(1,:),'b-',x,Actual,'r--', "LineWidth", 2) 
hold off
title('Milstein Solution (h = 0.001): dX = 0.1 X(t)dt + 4 X(t)dW_t, x_0 = 20')
xlabel('time', 'FontSize', 30)
ylabel('X(t)   ','FontSize',30,'Rotation',0)
set(gca,'fontsize',30)
legend('EM Solution','Milstein Solution','Actual Solution','Location','northeast')