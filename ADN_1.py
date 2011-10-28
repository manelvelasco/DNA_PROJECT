# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/mvelasco/.spyder2/.temp.py
"""
import random
r=random.random

        
class cell:
    def __init__(self,ENV,position=[0,0]):
        self.ADN=ENV[0][1]
        self.ENV=ENV
        self.position=position
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
        
    def test_type(self,obj,typ):
        if obj[0]==typ:
            return 1
        
    def Find_in_ENV(self,name):
        return filter((lambda obj:self.test_type(obj,name)),self.ENV)

    def Find_in_ADN(self,name):
        return filter((lambda obj:self.test_type(obj,name)),self.ADN)

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
    def Add_to_ENV(self,name,obj):
        self.ENV.append([name,obj])

    def Get_from_ENV(self,name):
        L=self.Find_in_ENV(name)
        if len(L)>0:
            self.ENV.remove(L[0])
            return L[0][1]


if __name__=="__main__":
    #Example of isolated execution
    #This example shows how to compute the 
    #explonential of a number in random way
    #To do so we use the taylor aproximation of exp function
    #exp(x)=1+x+1/2! x*x + 1/3! x*x*x etc..
    
    #As you can see the computation of coefs and powers are unrelated!!!!
    
    #DNA Functions
    def Compute_next_power(icell):
        try:
            max_pow=icell.Get_from_ENV('maxpower')
            print max_pow
            ep=icell.Get_from_ENV('evaluated_point')
            icell.Add_to_ENV('maxpower',max_pow*ep)
            ep=icell.Add_to_ENV('evaluated_point',ep)
        except:
            print "E1"

    def Compute_next_coef(icell):
        try:
            max_coef=icell.Get_from_ENV('maxcoef')
            n=icell.Get_from_ENV('n')
            icell.Add_to_ENV('maxcoef',max_coef/(n+1))
            icell.Add_to_ENV('n',n+1)
        except:
            print "E2"
        
    def compute_next_value(icell):
        try:
            val=icell.Get_from_ENV('value')
            max_coef=icell.Get_from_ENV('maxcoef')
            max_pow=icell.Get_from_ENV('maxpower')
            icell.Add_to_ENV('value',val+max_coef*max_pow)
            icell.Add_to_ENV('maxpower',max_coef)
            icell.Add_to_ENV('maxcoef',max_pow)
        except:
            print "E3"

    def start_computation(icell):
        icell.Add_to_ENV('maxpower',1)
        icell.Add_to_ENV('maxcoef',1)
        icell.Add_to_ENV('n',0)
        icell.Add_to_ENV('value',0)
        icell.Add_to_ENV('evaluated_point',0.5)
        icell.change_ADN_prob('Action4', 0)
        icell.change_ADN_prob('Action3', .999)
        
    ADN=[['Action1',Compute_next_power,0.25],
         ['Action2',Compute_next_coef,.25],
         ['Action3',compute_next_value,0.25],
         ['Action4',start_computation,0.25]]
    ENV=[['ADN',ADN],['Proteine1',1],['Proteine2',1]]
    
    cell1=cell(ENV)
    cell1.change_ADN_prob('Action3',.8)
    for i in range(10000):
        print i
        cell1.execute_random_acction()
        print cell1.Find_in_ENV('value')
        #print cell1.Find_in_ENV('value')
        
    
    