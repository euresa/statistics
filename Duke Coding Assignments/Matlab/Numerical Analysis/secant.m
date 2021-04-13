function root = secant(f,x0,x1,tol)
%secant(f,x0,x1,tol) finds a root of f(x) using Newton's Method
%   x0 is the initial guess
%   f and df must be defined for x0
%   finds abs(f(root)) < tol
%   Author: Samuel Eure
%   Last Modified: March 5, 2018

Fx0 = f(x0);
Fx1 = f(x1);

while(abs(Fx0) > tol)
    temp = x1;
    A = ((x1-x0)/(Fx1-Fx0));
    Fx1
    x1 = x0 - Fx1*A;
    x0 = temp;
    Fx0 = Fx1;
    Fx1 = f(x1);
end

root = x0;

end

