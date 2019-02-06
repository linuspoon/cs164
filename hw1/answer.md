# cs164 hw1

## 1

I assume that letters in S are not repeated.

HowManySubseq = NC0 + NC1 + NC2 + ... + NCN = (1+1)^N = 2^N

HowManySubstr = 1 + N + (N-1) + (N-2) + ... + 1 = N\*(N+1)/2 + 1

## 2

> "binary string" means any string consisted only with some "0"s and "1"s.

a. Any binary string whose size > 1 and begins with 0 and ends with 0.

b. Any binary string not starting with "1".

c. Any binary string ends with 000, 001, 010 or 011.

d. Any binary string with exactly 3 "1"s.

e. Any binary string with even number of "1"s and even number of "0"s.

## 3

```
a. r"^[^aeiou]*a[^aeiou]*e[^aeiou]*i[^aeiou]*o[^aeiou]*u[^aeiou]*$"
b. r"^a*b*c*d*e*f*$"
c. r"^\/\*((?![^\"]*\*\/)[^\"]*\"[^\"]*\")*(?!.*\*\/.*\*\/).*\*\/$"
d. r"^(00|11)*((01|10)(00|11)*(01|10)(00|11)*)*1(00|11)*((01|10)(00|11)*(01|10)(00|11)*)*$"
e. r"^1*(0+1)*0*$"
f. r"^1*0*1?0*$"
```

