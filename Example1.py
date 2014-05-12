# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 22:16:24 2011

@author: -
"""
from ADN_1 import cell
import pprint
import pylab
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
        if max_pow==None:
            add_to_pending_functions(icell, Compute_next_power)
            return
        ep=icell.Get_from_ENV('evaluated_point')
        if ep==None:
            icell.Add_to_ENV('power',max_pow)
            return
        icell.Add_to_ENV('power',[max_pow[0]*ep,max_pow[1]+1])
        icell.Add_to_ENV('evaluated_point',ep)
    except:
        raise

def Compute_next_coef(icell):
    try:
        coef=icell.Get_from_ENV('coef')
        if coef==None:
            #add_to_pending_functions(icell, Compute_next_coef)
            return
        icell.Add_to_ENV('coef',[coef[0]/(coef[1]+1),coef[1]+1])
    except:
        raise
    
def compute_next_value(icell):
    try:
        coef=icell.Get_from_ENV('coef')
        if coef==None:
            add_to_pending_functions(icell,compute_next_value)
            return
        power=icell.Get_from_ENV('power')
        if power==None:
            icell.Add_to_ENV('coef',coef)
            #add_to_pending_functions(icell,compute_next_value)
            return
        value=icell.Get_from_ENV('value')
        if value==None:
            icell.Add_to_ENV('coef',coef)
            icell.Add_to_ENV('power',power)
            #add_to_pending_functions(icell,compute_next_value)
            return
        if value[1]==coef[1]-1 and value[1]==power[1]-1:
            icell.Add_to_ENV('value',[value[0]+coef[0]*power[0],value[1]+1])
        else:
            icell.Add_to_ENV('value',value)
            #add_to_pending_functions(icell,compute_next_value)
        icell.Add_to_ENV('coef',coef)
        icell.Add_to_ENV('power',power)
        
    except:
        raise

def start_computation(icell):
    icell.Add_to_ENV('power',[0.5,1.0])
    icell.Add_to_ENV('coef',[1.0,1.0])
    icell.Add_to_ENV('value',[1.0,0.0])
    ep=icell.Get_from_ENV('evaluated_point')
    if ep==None:
        icell.Add_to_ENV('evaluated_point',0.5)
    else:
        icell.Add_to_ENV('evaluated_point',ep)
    icell.change_ADN_prob('Action4',0.005)
    icell.change_ADN_prob('Action3',0.95)

def add_to_pending_functions(icell, fun):
    pending=icell.Get_from_ENV('pending')
    if pending==None:
        pending=[fun]
    else:
        pending.append(fun)
        icell.Add_to_ENV('pending',pending)

ADN=[['Action1',Compute_next_power,0.25],
     ['Action2',Compute_next_coef,.25],
     ['Action3',compute_next_value,0.25],
     ['Action4',start_computation,0.25]]
ENV=[['ADN',ADN],['pending',[]]]

cell1=cell(ENV)
for i in range(50000):
    cell1.execute_random_acction()
#    
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(cell1.Find_in_ENV('value'))
valores=[];
for el in cell1.Find_in_ENV('value'):
    valores.append(el[1][1])
print valores
pylab.hist(valores,bins=max(valores))
pylab.show()