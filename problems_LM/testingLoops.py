# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 12:22:24 2020

@author: coolb
"""


n1 = 3
n2 = 5




sum1 = 0
sum2 = 0
sum3 = 0
sum4 = 0

iterations = 0

for k in range(n1):
    sum1 += 1
    for i in range(n2):
        sum2 += 1
        for j in range(i+1):
#            print('j =',j)
            sum3 += 1
            if 1<= j < i:
                sum4 += 1