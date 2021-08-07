#!/usr/bin/env python
# coding: utf-8

# In[1]:


r''' Library with Pricing and Delta formulae for:
        - European option (call & put)
        - Binary option (call & put)

Formulae based on Wilmott ("Frequently Asked Questions in Quantitative Finance", Second Edition, Wiley, 2009).

'''

# import libraries

import math
from scipy.stats import norm
import numpy
import pandas


# In[4]:


def option_pricer(Spot, K_strike, rf_rate, vol, Term, product = 'european', opt_type = 'call'):
    
    r'''' Option Pricer
    The option Pricer function will return the Call or Put option Price, and its Delta.
    '''
    
    r'''
    In case the product type is european, the Vanilla European Option Price function will be use.
    In case the product type is binary, the Vanilla European Option Price function will be use.
    default value of product variable is 'european'
    No other product type is in scope of the function.
    '''
    
    r'''
    Default option type is call.
    To price a put, opt_type variable must be set to 'put'
    '''

    # validate numeric data is in numeric format
    assert type(Spot) in (int, float, numpy.int64, numpy.float64) , "Spot not int or float"
    assert type(K_strike) in (int, float, numpy.int64, numpy.float64) , "Stike (K_strike) not int or float"
    assert type(rf_rate)  in (float, numpy.float64) , "Risk free rate (rf_rate) not int or float"
    assert 0 < rf_rate < 1 , "Risk free rate (rf_rate) is invalid"
    assert type(vol) in (float, numpy.float64) , "Volatility (vol) not int or float"
    assert 0 < vol < 1 , "Volatility (vol) is invalid"
    assert type(Term) in (int, float, numpy.int64, numpy.float64) , "Term not int or float"
    
    # validate product and option type are string
    assert type(product) == str, "Product type must be string"
    assert type(opt_type) == str, "Option type must be string"
    
    # convert product and option type to lower case    
    product = product.lower()
    opt_type = opt_type[0].lower()
    
    # validate product and option type can be processed
    assert ( 'european' in product) or ('binary' in product ) , "Product type invalid"
    assert opt_type[0] in ('c', 'p') , "Option type invalid, must be call or put"
    
    
    # precalculate d1 and d2
    
    d1 = ( math.log( Spot / K_strike) + (rf_rate + ((vol**2)/2) ) * Term ) / (vol*math.sqrt(Term))
    
    d2 = d1 - (vol * math.sqrt(Term))

    
    # "Vanilla European Option Price"
    # if vanilla call
    if ('european' in product) & (opt_type == 'c'):
        opt_price = Spot * norm.cdf(d1) - K_strike * math.exp(-rf_rate * Term ) * norm.cdf(d2)
        opt_delta = norm.cdf(d1)
    
    # if vanilla put
    if ('european' in product) & (opt_type == 'p'):
        opt_price = K_strike * math.exp(-rf_rate * Term ) * norm.cdf(-d2) - Spot * norm.cdf(-d1)
        opt_delta = ( norm.cdf(d1) - 1 )

    r''' Binary Option Price '''

    # if binary call
    if ('binary' in product) & (opt_type == 'c'):
        opt_price = math.exp(- rf_rate * Term ) * norm.cdf(d2)
        
        # 07/08/21: Fix binary call Delta
        # Before:
        # opt_delta = math.exp(- rf_rate * Term )* norm.cdf(d2) / ( vol * Spot * math.sqrt(Term) )
        # After:
        opt_delta = math.exp(- rf_rate * Term ) * norm.pdf(d2) / ( vol * Spot * math.sqrt(Term) )
        # N'() = std normal density function (Excel normdist(x, 0, 1, false) )
        

    # if binary put
    if ('binary' in product) & (opt_type == 'p'): # fixed 21/07 @10.24pm, was == 'c'
        opt_price = math.exp(- rf_rate * Term ) * norm.cdf(-d2)
        
        # 07/08/21: Fix binary call Delta
        # Before:
        # opt_delta = math.exp(- rf_rate * Term ) * norm.cdf(-d2) / ( vol * Spot * math.sqrt(Term) )
        # After:
        opt_delta = - math.exp(- rf_rate * Term ) * norm.pdf(d2) / ( vol * Spot * math.sqrt(Term) )

    # 07/08/21: Fix binary call Delta
    # Before 
    # returns a pandas.Series
    # return( pandas.Series( [ round(opt_price, 4) , round(opt_delta, 6) ] ) )
    # After:
    
    price = round(opt_price, 4)
    delta = round(opt_delta, 6)
    
    # return list
    return [ price, delta ]

