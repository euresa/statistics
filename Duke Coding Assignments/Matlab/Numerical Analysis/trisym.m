function x = trisym(A,b)
%trisys(A,B)
%   Takes in an nx2 matrix and an nx1 vector b and 
%   correctly solves Ax=b from factoring A into A = LL' where
%   L is lower triangular and symmetric

%   Problem 4, HW 4, MATH 361S
%   Author: Samuel Eure
%   Last Modified: Feb 14, 2018

n = length(b);

L = zeros(2,n);        %L first row of L will hold all my "d"s

L(1,1) = sqrt(A(1,1));

%First I will solve A = LL'
for k = (2:n);
    L(2,k) = A(2,k-1)/L(1,k-1); %L second row of L will hold all my "c"s
    L(1,k) = sqrt( A(1,k) - (L(2,k)^2) );
end

%Now I will solve Ly=b where y = L'x

y = zeros(n,1);

y(1) = b(1)/L(1,1);

for k = (2:n)
    y(k) = (b(k) - L(2,k)*y(k-1))/L(1,k);
end

%Now I will solve for L'x = y

x = zeros(n,1);

x(n) = y(n)/L(1,n);

for k = (n-1:-1:1)
    x(k) = (y(k)-L(2,k+1)*x(k+1))/L(1,k);
end
%return x
end


