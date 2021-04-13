function [y] = bEuler(t0,b, y0,f, df,h)
%bEuler(t0,b, y0,f, df) solves ODE using the Backwards Euler method
%   Returns a solution on the interval [t0,b]
%   h is set at 0.01, but can be adjusted
%   y0 is the initial condition
%   tol = tol = abs(10^(-12));
%   Author: Samuel Eure
%   MATH 361S, Homework 7
%   Last Modified 1:32pm, 04/14/2018
tol = abs(10^(-10));
steps = (b-t0)/h;
steps = round(steps);
y = zeros(1,1);
y(1) = y0;
t = t0; 
x = t0:h:b;
for i = 1:(steps)
    t = t+h;
    y1 = y(i);
    Error = y1 - y(i)- h*f(t,y1);
    while(abs(Error) > tol)
        yNext = y1 - (y1 - y(i) - h*f(t,y1))/(1-h*df(t,y1));  %1-df since g(y) 
        Error = yNext - y(i) - h*f(t,yNext);  %             = y - const - f
        y1 = yNext;                        %        for constant = y0
    end 
    y(i+1) = y1;
end
if length(x) ~= length(y)
   x(length(y))=b;
end

plot(x,y, x, sol(x))
legend({'Backwards Euler', 'Actual'}, 'FontSize', 20)

end
