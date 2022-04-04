# -*- coding: utf-8 -*-
import random
"""
Created on Wed Feb 23 12:49:24 2022

@author: walsh
"""
#vAMM example

def pickNum(choice):
    test = [0,1,2,3,4,5,6,7,8,9]
    PN = [-1,1]
    sig = random.choice(PN)

    b = random.choice(test) * 10
    c = random.choice(test)
    d = random.choice(test) / 10
    e = random.choice(test) / 100

    if choice == 1:
        a = round(b + c + d + e, 2) * sig
    if choice != 1: 
        a = round(b + c + d + e, 2)
    return a

def regulate(inputK):
    n = 0.1
    q = 0.1
    b = -1

    x = inputK/100

    y = -1 * ( n / (x + q) + b ) / 2
    return y

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
oraclePrice = 12

# out, pool_mAsset, pool_UST, tx = transact_normalAMM(USTCount, 1, X, Y) #Denominated in UST
# print(out, pool_mAsset, pool_UST, tx)

# out, pool_mAsset, pool_UST, tx = transact_normalAMM(mAssetCount, 2, X, Y) #Denominated in mAsset
# print(out, pool_mAsset, pool_UST, tx)


# out, pool_mAsset, pool_UST, tx, w, a = transact_DynamicAMM(USTCount, 1, X, Y, oraclePrice)
# print(out, pool_mAsset, pool_UST, tx, w, a)
# print(pool_UST / pool_mAsset, pooled_mAsset_price)
# print(USTCount / out, "mAsset_price")

# out, pool_mAsset, pool_UST, tx, w, a = transact_DynamicAMM(mAssetCount, 2, X, Y, oraclePrice)
# print(out, pool_mAsset, pool_UST, tx, w, a)
# print(pool_UST / pool_mAsset, pooled_mAsset_price)
# print(out / mAssetCount, "mAsset_price")
oracleN = []

for each in range(0,100):
    g = 0
    p = 0
    sigs = random.choice([-1,1])
    a = regulate(pickNum(0)) / 10 * sigs

    deltaUnit = pickNum(1)
    out, pool_mAsset, pool_UST, tx = transact_normalAMM(deltaUnit,1,X,Y)
    #print(tx,"\t" ,delta, out, pool_mAsset, pool_UST)
    X = pool_mAsset
    Y = pool_UST
    g = Y / X * ( 1 + a )
    p = Y / X
    oracleN.append( [g - p, a] )
    
print((Y / X / oraclePrice - 1), X, Y)


print(a)
print(oracleN)
    