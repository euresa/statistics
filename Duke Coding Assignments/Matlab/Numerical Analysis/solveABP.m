function x = lusolve(A,p,b)
%lusolve(A,p,b)
%   Takes outputs A and p from lug, and 
%   solves LUx = Pb 
%   Detailed explanation goes here
%   Developed by Samuel Eure 
%   Algorithm from Kincaid & Cheney, Numerical Analysis
%   Last modified Jan 27, 2018

n = length(A);
%Solving Ly = b
y(1) = b(p(1));                  %obtain first y1 value

for piv = 2:n
    y(piv) = b(p(piv));      %initialize the next y value
    for earlier = 1:(piv-1)     %then subract off the other y*a(i,j) values
        y(piv) = y(piv) - y(earlier)*A(p(piv),earlier);
    end
end

%I have now solved Ly = b
%Now solving Ux = y

x(n) = y(n)/A(p(n),n);
for piv = (n-1):-1:1
    for later = (piv+1):n
        y(piv) = y(piv) - x(later)*A(p(piv),later);
    end
    x(piv) = y(piv)/A(p(piv),piv);
end




end

