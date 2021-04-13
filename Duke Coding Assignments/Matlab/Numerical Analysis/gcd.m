function d = gcd(a,b)
%gcd(a,b) takes integers a and b and returns their
%greatest common divisor
d = min(a,b);
while d>1
    ra = rem(a,d);
    rb = rem(b,d);
    if (rb == 0 && ra == 0)
       d
       d= 1;
    end
    d = d - 1;
end
end

    