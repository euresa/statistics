function [x] = Gspecial(A, b, xO, times )
%gs(A,b,x0,rtol) solves Ax=b using Gauss-Seidel to relative tolerance
%   Author: Samuel Eure
%   MATH 361S Spring 2018
%   Homework 4 Code

n = length(b);
x = xO;       %I did this since I don't like typing out xO

sub = 0;
old = x;
for k = (1:n)
    sub = A(k,1:n)*x - x(k)*A(k,k) ;    %I add the dot product and then 
    x(k) = ( b(k)-sum(sub) )/A(k,k) ;   %subtract x(k)*A(k,k)
end
x
C = 1;
while(C<=times)
    C= C+1;
    old = x;
    sub = 0;
    for k = (1:n)
        sub = A(k,1:n)*x - x(k)*A(k,k) ;
        x(k) = ( b(k)-sum(sub) )/A(k,k) ;  
    end

    x
end

end
