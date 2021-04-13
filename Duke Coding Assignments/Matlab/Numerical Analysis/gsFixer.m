function [A,b] = gsFixer(n)
%Prepared Matrices for Gauss-Seidel
%   Author: Samuel Eure
%   Last Modified: Feb 17, 2018
b = 1:n;
b = b';
b = b/(n^3);

A = zeros(n,n);
A(1,1) = 2;
for i = (2:(n))
    A(i,i) = 2;
    A(i,i-1) = -1;
    A(i-1,i) = -1;
end

end

