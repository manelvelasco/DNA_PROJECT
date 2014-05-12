# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/mvelasco/.spyder2/.temp.py
"""
import random
r=random.random

class plasma:
    def __init__(self,ENV):
        self.ENV=ENV

    def test_type(self,obj,typ):
        if obj[0]==typ:
            return 1

    def Find_in_ENV(self,name):
        return filter((lambda obj:self.test_type(obj,name)),self.ENV)

    def Add_to_ENV(self,name,obj):
        self.ENV.append([name,obj])

    def Get_from_ENV(self,name):
        L=self.Find_in_ENV(name)
        if len(L)>0:
            self.ENV.remove(L[0])
            return L[0][1]
        
class cell(plasma):
    def __init__(self,ENV,position=[0,0]):
        self.ADN=ENV[0][1]
        self.ENV=ENV
        self.position=position
        self.BODY=None

    def cumulative_prob_sum(self):
        cum_sum=[]
        y=0;
        for el in self.ADN:   # <--- i will contain elements (not indices) from n
            y += el[2]    # <--- so you need to add i, not n[i]
            cum_sum.append(y)
        return cum_sum

    def execute_random_acction(self):
        cumulative=self.cumulative_prob_sum()
        rn=r()
        ind=[i for i in range(len(cumulative)) if cumulative[i] > rn]
        #This executes the magic function
        self.ADN[ind[0]][1](self)

    def change_ADN_prob(self,name, newProb):
        if newProb<=1.0 and newProb>=0.0:
            others=filter((lambda obj:not self.test_type(obj,name)),self.ADN)
            tp=reduce((lambda x,y:self.probability_of(x)+self.probability_of(y)),others)
            k=(1.0-newProb)/tp  
            for el in others:
                el[2]=k*el[2]
            special_element=self.Find_in_ADN(name)
            special_element[0][2]=newProb
        else:
            raise Exception("Probability should be between 0.0 and 1.0" )

    def probability_of(self,obj):
        try:
            return obj[2]
        except:
            return obj

    def Find_in_ADN(self,name):
        return filter((lambda obj:self.test_type(obj,name)),self.ADN)

    

class body(plasma):
    def __init__(self,ENV,CELLS):
        self.ENV=ENV
        self.CELLS=CELLS
        for icell in CELLS:
            icell.BODY=self


if __name__=="__main__":
    pass