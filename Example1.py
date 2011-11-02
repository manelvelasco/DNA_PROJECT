# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 22:16:24 2011

@author: -
"""
from ADN_1 import cell
#Example of isolated execution
#This example shows how to compute the 
#explonential of a number in random way
#To do so we use the taylor aproximation of exp function
#exp(x)=1+x+1/2! x*x + 1/3! x*x*x etc..

#As you can see the computation of coefs and powers are unrelated!!!!

#DNA Functions
def Compute_next_power(icell):
    try:
        max_pow=icell.Get_from_ENV('power')
        ep=icell.Get_from_ENV('evaluated_point')
        icell.Add_to_ENV('power',[max_pow[1]*ep,max_pow[1]+1])
        ep=icell.Add_to_ENV('evaluated_point',ep)
    except:
        print "E1"

def Compute_next_coef(icell):
    try:
        coef=icell.Get_from_ENV('coef')
        icell.Add_to_ENV('coef',[coef[0]/(coef[1]+1),coef[1]+1])
    except:
        print "E2"
    
def compute_next_value(icell):
    try:
        coef=icell.Get_from_ENV('coef')
        power=icell.Get_from_ENV('power')
        value=icell.Get_from_ENV('value')
        if value[1]==coef[1]-1 and value[1]==power[1]-1:
            print [value[0]+coef[0]*power[0],value[1]+1]
            icell.Add_to_ENV('value',[value[0]+coef[0]*power[0],value[1]+1])
            print "Activation"
        else:
            icell.Add_to_ENV('value',value)
            pending=icell.Get_from_ENV('pending')
            print "Añadiendo funcion"  
            pending.append(f)
            icell.Add_to_ENV('pending',pending)
        icell.Add_to_ENV('power',coef)
        icell.Add_to_ENV('coef',power)
    except:
        print "E3"

def start_computation(icell):
    icell.Add_to_ENV('power',[1.0,0.0])
    icell.Add_to_ENV('coef',[1.0,0.0])
    icell.Add_to_ENV('value',[0.0,-1.0])
    icell.Add_to_ENV('evaluated_point',0.5)
    icell.change_ADN_prob('Action4',0.01)



ADN=[['Action1',Compute_next_power,0.25],
     ['Action2',Compute_next_coef,.25],
     ['Action3',compute_next_value,0.25],
     ['Action4',start_computation,0.25]]
ENV=[['ADN',ADN],['pending',[]]]

cell1=cell(ENV)
for i in range(10000):
    print i
    cell1.execute_random_acction()
    pending=cell1.Find_in_ENV('pending')
    #print pending
    if len(pending):
        for el in pending[0][1]:
            print el
            el(cell1)
    #try:
        #print cell1.Find_in_ENV('value')[0]
    #except:
        #print "No values yet"#print cell1.Find_in_ENV('value')
print ENV