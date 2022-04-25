# -*- coding: utf-8 -*-
import random
import math
import numpy as np
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
        out.append(each)
    return out

def build_Oracle(dynamic,start,minORmax,blockcount,variance=0):
    
    a = np.linspace(start,minORmax,blockcount)
    a_n = []
    b_n = []
    for each in a:
        a_n.append(each)
        b_n.append(each)
    b_n.remove(minORmax)
    b_n.reverse()
    for each in b_n:
        a_n.append(each)
    
    if dynamic == 1:
        c_n = []
        for each in a_n:
            out = gaus_rand(each,variance,1)
            c_n.append(out[0])  
        a_n = c_n
        
    return a_n
    

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
    end = data
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
        liq_discount = min(current_CR - 1,L_discount)
        
        liqd_col = min(mAsset / (1-liq_discount) * oraclePrice,collateral)
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




Oracle = build_Oracle(1,11,9,50,.05)
    
#print(Oracle)
#Define Global variables

Per_block_value_used = 10 #in UST
cooldown = 10 #1 minute
MCR = 1.2
price_cushion = .1 #percent change to prevent liquidation
discount_rate = .2 #percent discount for liquidation
CDP_closure_fee = .015 #percent fee levied on minted mAsset value upon liquidation or CDP closure
swap_fee = 0.003 #percent fee levied on any swap transaction
Per_block_value_used = 100 #in UST
X_i = 1000
Y_i = 10000
static_oracle = 10
p_i = Y_i / X_i



#NORMAL AMM w/ stable oracle
p = p_i
x = X_i
y = Y_i
O = static_oracle
d = Per_block_value_used
c = price_cushion
pos = []
x_con = [x]
y_con = [y]
p_con = [p]
test = 0
ret_UST = 0
minted = 0
minted_Cost = 0
tx_list = gaus_rand(0, 50, 100)
Oracle.reverse()
for each in range(0,len(Oracle)):
    
    p = y / x
    x_con.append(x)
    y_con.append(y)
    p_con.append(p)
    #print(p)
    #print(each)
    if p > Oracle[each]:
        out = mint_mAsset(d, MCR, Oracle[each], c)
        minted += out[1]
        test += d
        ret = transact_normalAMM(out[0], 2, x, y)
        ret_UST += ret[0]
        pos.append(out)
        x = ret[1]
        y = ret[2]


    elif p < Oracle[each]:
        for element in pos:
            value = element[3] / (element[0] * Oracle[each])
            #print(value)
            #print(element)
            #print(Oracle[each])
            if value < MCR:
                re_buy = transact_normalAMM(-element[0], 2, x, y)
                #print(re_buy)
                x = re_buy[1]
                y = re_buy[2]
                liqd_coll = burn_mAsset(element, each, MCR, CDP_closure_fee, discount_rate)
                
                if liqd_coll != element[3]:
                    pos[pos.index(element)] = mint_mAsset(element[3]-liqd_coll, MCR, each, 0.001)
                else:
                    pos.remove(element)
                #print(element)
                
    randomInteraction = transact_normalAMM(tx_list[each], 1, x, y)
    #print(randomInteraction)
    x = randomInteraction[1]
    y = randomInteraction[2] 
    
#print(pos)  

fig, (ax1,ax2) = plt.subplots(2,sharex=True,sharey=False)
ax1.plot(y_con,color = 'r',label = "Pooled USD")
ax1.grid()
ax1.set_ylabel("USD")
ax1.legend(loc = 'best')
ax2.plot(x_con, color = 'b',label = "Pooled mAsset")
ax2.grid()
ax2.set_ylabel("mAsset")
ax2.set_xlabel("Block")
ax1.set_title("Pool Concentration: mAsset vs. USD")
ax2.legend(loc = 'best')


fig, ax1 = plt.subplots()
ax1.plot(Oracle,color = 'r', label = "Oracle Price")
ax1.grid()
ax1.set_ylabel("USD")
ax1.set_xlabel("Block")
ax1.plot(p_con, color = 'b', label = "Pool Price")
plt.legend(loc = 'best')
ax1.set_title("Price Comparison: Oracle vs. Pool")
#ax1.plot(tx_list)



#dvAMM integration
x_2 = X_i
y_2 = Y_i
p_2 = p_i
x_con_2 = [x_2]
y_con_2 = [y_2]
p_con_2 = [p_2]
for each in range(0,len(Oracle)):
    p_2 = y_2 / x_2
    x_con_2.append(x_2)
    y_con_2.append(y_2)
    p_con_2.append(p_2)
    if p_2 > Oracle[each]:
        out = transact_vAMM(d, 1, 1, x_2, y_2, Oracle[each], 0)
        out_2 = transact_normalAMM(out[0][4], 2, x_2, y_2)
        #print(out_2)
        x_2 = out_2[1]
        y_2 = out_2[2]
    
    elif p_2 < Oracle[each]:
        out = transact_vAMM(-d, 1, 1, x_2, y_2, Oracle[each], 0)
        out_2 = transact_normalAMM(out[0][4], 2, x_2, y_2)
        print(out_2)
        x_2 = out_2[1]
        y_2 = out_2[2]
    
    randomInteraction = transact_normalAMM(tx_list[each], 1, x_2, y_2)
    #print(randomInteraction)
    x_2 = randomInteraction[1]
    y_2 = randomInteraction[2] 

fig, (ax1,ax2) = plt.subplots(2,sharex=True,sharey=False)
ax1.plot(y_con_2,color = 'r',label = "Pooled USD")
ax1.grid()
ax1.set_ylabel("USD")
ax1.legend(loc = 'best')
ax2.plot(x_con_2, color = 'b',label = "Pooled mAsset")
ax2.grid()
ax2.set_ylabel("mAsset")
ax2.set_xlabel("Block")
ax1.set_title("Pool Concentration: mAsset vs. USD")
ax2.legend(loc = 'best')


fig, ax1 = plt.subplots()
ax1.plot(Oracle,color = 'r', label = "Oracle Price")
ax1.grid()
ax1.set_ylabel("USD")
ax1.set_xlabel("Block")
ax1.plot(p_con_2, color = 'b', label = "Pool Price")
plt.legend(loc = 'best')
ax1.set_title("Price Comparison: Oracle vs. Pool")
#ax1.plot(tx_list)






#dvAMM + AMM

"""
fig, ax1 = plt.subplots()
ax1.plot(x_con, color = 'red',label = "mAsset")
ax1.set_xlabel("Block")
ax1.set_ylabel("mAsset")
plt.grid()
plt.legend(loc = 'upper right')
ax2 = ax1.twinx()
ax2.plot(y_con, color = 'blue',label = "USD")
ax2.set_ylabel("USD")
plt.legend(loc = 'upper left')
plt.grid()
fig.suptitle("Pool Concentration: mAsset vs. USD")
fig.savefig("pool_Con.jpg")
"""










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