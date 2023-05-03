#!/usr/bin/env python
# coding=utf-8

#放入__all__中所有属性均可导入，即使是以下划线开头
__all__ = ('func','__func','_A') 
  
class _A():  
    def __init__(self,name):  
        self.name = name  
        
def func():    
    print ('func() is called!')    
     
def func1():    
    print ('func1() is called!')    
    
def _func():    
    print ('_func() is called!')    
        
def __func():    
    print ('__func() is called!')