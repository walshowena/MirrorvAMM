# -*- coding: utf-8 -*-
import random
import math
"""
Created on Wed Feb 23 12:49:24 2022

@author: walsh
"""
#vAMM example
def transact_normalAMM( assetInput, txType, pooled_mAsset, pooled_UST ): #txType determines buy[1] or sale[2] (of mAsset)
    x = pooled_mAsset
    y = pooled_UST
    k = x * y
    n = assetInput
    if txType == 1: #if tx type is a purchase of mAsset (using UST)
        if assetInput < 0:
            tx = 'Buys mAsset'
        else:
            tx = 'Sell mAsset'   
        y_n = y + n
        H = x - ( k / y_n )
        x_H = x - H
        return H, x_H, y_n, tx
    if txType == 2: #if tx type is a sale of mAsset (in exchange for UST)
        if assetInput < 0:
            tx = 'Sell mAsset'
        else:
            tx = 'Buys mAsset'    
        x_n = x + n
        H = y - ( k / x_n)
        y_H = y - H
        return H, x_n, y_H, tx
    
def transact_DynamicAMM( assetInput, txType, pooled_mAsset, pooled_UST, oraclePrice ): #txType determines buy or sale (of mAsset))
    x = pooled_mAsset
    y = pooled_UST
    k = x * y
    n = assetInput
    ref_p = oraclePrice
    
    w = k * ( ref_p / ( y * y ) )
    a = x - ( y / ref_p )
    x_a = x - a
    
    if txType == 1: #if tx type is a purchase of mAsset (using UST)
        if assetInput > 0:
            tx = 'Buys mAsset'
        else:
            tx = 'Sell mAsset'
        y_n = y + n
        H = ( k / ( w * y_n ) - x_a ) * -1
        x_H = x - H
        return H, x_H, y_n, tx, w, a
    if txType == 2: #if tx type is a sale of mAsset (in exchange for UST)
        if assetInput > 0:
            tx = 'Sell mAsset'
        else:
            tx = 'Buys mAsset'    
        x_n = x + n
        H = ( k / ( w * ( x_a + n ) )  - y ) * -1  
        y_H = y - H
        return H, x_n, y_H, tx, w, a

pooled_mAsset = 100
pooled_UST = 1000

pooled_mAsset_price = pooled_UST / pooled_mAsset

X = pooled_mAsset
Y = pooled_UST
USTCount = 10
mAssetCount = 10
oraclePrice = 9

MCR = 1.5
dY = 1000

CDPn = MCR * dY

CumulativeCDPCost = 0
profit = 0
for each in range(0,100):
    profit = 0
    
#try several conditions 
### Part 1 - AMM vs Mint AMM idea

##NEW IDEA
"""
Burn MIR for mAsset_I
mAsset_I(price) == Oracle Price
(NOT SWAPPABLE AND IS LOCKED IN CONTRACT EXECUTION)
mAsset_I used to create CDP of original mAsset
Collateral multiplier (for new positions) increases as Peg is restored.
Negative rate is imposed when peg far gone (>20%)
Can liquidate to get more mAsset_I back vs mAsset depending on 'funding' 
Use mAsset_I to mint 

"""
X = 100000
Y = 1000000
dY = 1000
O_n = 1000
MCR = 1.5

"""
A)
Constant O_n, No Buy pressure   
Constant O_n, Buy Pressure < dY
Constant O_n, Buy Pressure = dY
Constant O_n, Buy Pressure > dY

B)
Linear 9 - 11 O_n, No Buy pressure
Linear 9 - 11 O_n, Buy Pressure < dY
Linear 9 - 11 O_n, Buy Pressure = dY
Linear 9 - 11 O_n, Buy Pressure > dY

Part 2
"""

x1, y1, O_n1 = 100000, 1000000, 9
x2, y2, O_n2 = 200000, 2000000, 10
x3, y3, O_n3 = 300000, 3000000, 11



"""
A)
Constant O_n, No Buy pressure   
Constant O_n, Buy Pressure < dY
Constant O_n, Buy Pressure = dY
Constant O_n, Buy Pressure > dY

B)
Invert O_n, No Buy pressure
Invert 9 - 11 O_n, Buy Pressure < dY
Invert 9 - 11 O_n, Buy Pressure = dY
Invert 9 - 11 O_n, Buy Pressure > dY
"""    
    
def transact_vAMM( assetInput, txType, pooled_mAsset, pooled_UST, oraclePrice, tx_count ):
    x = pooled_mAsset
    y = pooled_UST
    k = x * y
    n = assetInput
    ref_p = oraclePrice
    delta = 0
    cooldown = 5
    

    for each in range(0,tx_count+cooldown+1):
        if each <= tx_count:
            output = transact_DynamicAMM(n, txType, x, y, ref_p)
            delta += output[0]
            x = output[1]
            y = output[2]
            w = output[4]
            a = output[5]            
        balancer = delta / cooldown
        delta -= balancer
        x += balancer
        y = y - balancer * ref_p
        print(delta, x, y, w, a, balancer)
    
    
transact_vAMM(10, 1, 100, 1000, 10, 10)
    