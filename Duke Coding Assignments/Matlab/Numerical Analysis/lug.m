function [A,p] = lug(A,pivot)
%lug solves the LU decomposition of A and stores
%   Developed by Samuel Eure 
%   LU in PA where P is the permutation matrix 
%   created from the array p, which stores the row indexes
%   Algorithm from Kincaid & Cheney, Numerical Analysis
%   Last modified 2018, Jan 29, 11:19am

if(size(A,2)~=size(A,1)) %example of error handling (optional)
    error('Matrix must be square!');
end

n = length(A);

for i = 1:n
    p(i) = i;
    s(i) = max(abs(A(i,1:n)));                 %put s(i) has the max 
                                               %element in that row
end

%I have initialized p and s
for piv = 1:(n-1)
   
    if pivot == true                      %if pivoting
  
        maxvalue = abs(A(p(piv),piv))/s(p(piv));
        for r = (piv+1):n
            if maxvalue < abs(A(p(r),piv))/s(p(r))
                maxvalue = abs(A(p(r),piv))/s(p(r));
                oldindex = p(piv);
                p(piv) = p(r);
                p(r) = oldindex;
                
            end
        end
    end
    
    for row = (piv+1):n                   %going down the column
        t = A(p(row),piv)/A(p(piv),piv);
        A(p(row),piv) = t;
        for downrow = (piv+1):n           %going down the row
            A(p(row),downrow) = A(p(row),downrow) - t*A(p(piv),downrow);
        end
    end
end

            


