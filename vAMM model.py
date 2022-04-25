# -*- coding: utf-8 -*-
import random
import math
import matplotlib.pyplot as plt
"""
Created on Wed Feb 23 12:49:24 2022

@author: walsh
"""
def gaus_rand(mu,sigma,tx_count):
    nums = [] 
    mu = mu
    sigma = sigma
        
    for i in range(tx_count): 
        temp = random.gauss(mu, sigma) 
        nums.append(temp) 
    out = []
    k = 0
    for each in nums:
        k += each
        out.append(k)
    return out


#vAMM example
def transact_normalAMM( assetInput, txType, pooled_mAsset, pooled_UST ): #txType determines buy[1] or sale[2] (of mAsset)
    x = pooled_mAsset
    y = pooled_UST
    k = x * y
    n = assetInput
    if txType == 1: #if tx type is a purchase of mAsset (using UST)
        if assetInput > 0:
            tx = 'Buys mAsset'
        else:
            tx = 'Sell mAsset'   
        y_n = y + n
        H = x - ( k / y_n )
        x_H = x - H
        return H, x_H, y_n, tx
    if txType == 2: #if tx type is a sale of mAsset (in exchange for UST)
        if assetInput > 0:
            tx = 'Sell mAsset'
        else:
            tx = 'Buys mAsset'    
        x_n = x + n
        H = y - ( k / x_n)
        y_H = y - H
        return H, x_n, y_H, tx
    
def transact_DynamicAMM( assetInput, txType, pooled_mAsset, pooled_UST, oraclePrice, swapFee): #txType determines buy or sale (of mAsset))
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

def transact_vAMM( assetInput, txType, tx_count, pooled_mAsset, pooled_UST, oraclePrice,swapFee):
    x = pooled_mAsset
    y = x**2 / x * oraclePrice

    ref_p = oraclePrice
    n = assetInput
    delta = 0
    cooldown = 10
    total_x = [x]
    data = []
    #DEBUG / graph related
    lead = cooldown
    tx = 0
    tx_f = 0
    summ = 0
    
    for each in range(0,tx_count):
        if each < tx_count:
            output = transact_DynamicAMM(n, txType, x, y, ref_p,swapFee)
            if delta + output[0] > pooled_mAsset:
                x = x
                y = y
                w = w
                a = a
                tx += 1
                tx_f += 1
            else:
                delta += output[0]
                #print(x)
                x = output[1]
                #print(x)
                y = output[2]
                w = output[4]
                a = output[5]  
                tx += 1
                summ += n
        balancer = delta / cooldown 
        delta -= balancer
        data.append( [x, y, w, a, delta, balancer])
        y = (x + balancer)**2 / x * ref_p
        x += balancer
    end = [data]
    return end
 
    
def mint_mAsset(UST,MCR,oraclePrice,Cushion):
    a_CR = MCR * (1 + Cushion) 
    mAsset = UST / a_CR / oraclePrice
    CR = UST / (mAsset * oraclePrice)
    value = mAsset * oraclePrice
    return mAsset, value, CR,  UST, oraclePrice
    
    
def burn_mAsset(position,oraclePrice,MCR,closing_fee,L_discount):
    mAsset = position[0]
    collateral = position[3]
    current_value = mAsset * oraclePrice
    current_CR = collateral / current_value
    liqd_col = 0
    r_collateral = collateral
    if current_CR < MCR :
        liq_discount = math.min(current_CR - 1,L_discount)
        
        liqd_col = collateral
    else:
        kk = 0
    return liqd_col 

   
#try several conditions 
### Part 1 - AMM vs Mint AMM idea

#Define Oracle

duration = 100.0 #duration of test in blocks (in seconds is duration * 6) if 1000 -> 100 minutes
baseOracle = 10
p_variation = 0.5 #percent to adjust Oracle to relative to baseOracle (both + and -)
top_test = int((baseOracle * ( 1 + p_variation)) * duration + 1)
bot_test = int((baseOracle * ( 1 - p_variation)) * duration)
print(top_test, bot_test)
Oracle = []

#^ or \/
for each in range(50,101,1):
    Oracle.append(each / 10)
Oracle.reverse()
for each in range(50,101,1):
    Oracle.append(each / 10)
#for each in range(1000,1501,1):
#    Oracle.append(each / 100)
    
#print(Oracle)
#Define Global variables

Per_block_value_used = 10 #in UST
cooldown = 10 #1 minute
MCR = 1.5
price_cushion = .5 #percent change to prevent liquidation
discount_rate = .2 #percent discount for liquidation
CDP_closure_fee = .015 #percent fee levied on minted mAsset value upon liquidation or CDP closure
swap_fee = 0.003 #percent fee levied on any swap transaction
Per_block_value_used = 10 #in UST
X_i = 1000
Y_i = 10000
cushion = 1
static_oracle = 10
p_i = Y_i / X_i

#NORMAL AMM w/ stable oracle
p = p_i
x = X_i
y = Y_i
O = static_oracle
d = Per_block_value_used
c = cushion
pos = []
x_con = [x]
y_con = [y]
p_con = [p]
test = 0
ret_UST = 0
minted = 0
minted_Cost = 0
Oracle.reverse()
for each in Oracle:
    p = y / x
    #print(p)
    print(each)
    if p > each:
        out = mint_mAsset(d, MCR, each, c)
        minted += out[1]
        test += d
        ret = transact_normalAMM(out[0], 2, x, y)
        ret_UST += ret[0]
        pos.append(out)
        x = ret[1]
        y = ret[2]


    elif p < each:
        itit = 9
    x_con.append(x)
    y_con.append(y)
    p_con.append(p)
    
    



fig, ax1 = plt.subplots()
ax1.plot(p_con, color = 'red')
#ax2 = ax1.twinx()
ax1.plot(Oracle, color = 'blue')
plt.xlabel("Block")
plt.ylabel("Price")



out = mint_mAsset(100, 1.5, 10, .5)
#print(out)















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
#X = 100000
#Y = 1200000
#dY = 1000
#O_n = 1000
#MCR = 1.5

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

#x1, y1, O_n1 = 100000, 1000000, 9
#x2, y2, O_n2 = 200000, 2000000, 10
#x3, y3, O_n3 = 300000, 3000000, 11



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

"""
fig, ax1 = plt.subplots()
ax1.plot(test[0],marker = '.', color = 'red',)
plt.xlabel("Block")
plt.ylabel("mAsset")
"""