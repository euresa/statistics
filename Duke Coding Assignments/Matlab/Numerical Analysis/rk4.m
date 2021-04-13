function [y] = rk4(t0,b, y0,f,h)
%rk4(t0,b, y0,f) solves IVP for ODEs
%   Solution is from t0 to b
%   The initial condition is y0
%   Author: Samuel Eure
%   MATH 361S, Homework 7
%   Last modified: April 14, 2018
steps = (b-t0)/h;
y = zeros(1,1);
y(1) = y0;
t = t0;
steps = round(steps);
x = t0:h:b;
for i = 1:(steps)
    f1 = h*f(t,y(i));
    f2 = h*f(t + 0.5*h, y(i) + 0.5*f1);
    f3 = h*f(t + 0.5*h, y(i) + 0.5*f2);
    f4 = h*f(t +     h, y(i) +     f3);
    y(i+1) = y(i) + (1/6)*(f1 + 2*f2 + 2*f3 + f4);
    t = t + h;
end
if length(x) ~= length(y)
   x(length(y))=b;
end

z = sol(x,0);

plot(x,y,'LineWidth', 3);

end











