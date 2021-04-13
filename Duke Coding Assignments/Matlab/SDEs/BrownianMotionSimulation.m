%Brownian Motion Simulation
%   This script generates M realizations of an N step Wiener process
%   The default interval is from 0 to T = 1, but can be changed
%   Author: Samuel Eure (algorithm adapted from [Higham, 2001])
%   Last modified: 17 April, 2018
%
M = 10;             %Number of realizations
N = 1000;           %Number of steps
T = 1;              %Stop time from zero
dt = T/(N); 
for i = 1:M
    dW = zeros(1,N+1);
    W  = zeros(1,N+1);
    dW(2:N+1) = sqrt(dt)*randn(1,(N));
    W = cumsum(dW);
    X = 0:dt:T;
    plot(X,W)   %plot W against t
    hold on
end
xlabel('time', 'FontSize', 35)
ylabel('W(t)   ','FontSize',35,'Rotation',90)
set(gca,'fontsize',35, 'LineWidth', 2)
set(findall(gca, 'Type', 'Line'),'LineWidth',2);
hold off