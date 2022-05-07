
# MirrorvAMM: Virtual AMM Modeling 
*(for Terra's Mirror Protocol, or any other Oracle based exchange system)*

**Overview (What does this repo contain, what does it do?)**
Mirror is a protocol on the Terra Blockchain that uses CDPs (Collateralized Debt Positions) and Oracles (External Reference Prices) to create 'Mirrored' versions of various assets that allow users 'Price-Exposure' who might otherwise be left out of U.S., or other, markets. Unfortunately, the protocol is plagued by 'de-pegging' issues whereby mAsset (Mirrored Asset) prices trade at a significant premium or discount to the Oracle prices. This is sadly due to the structure of the arbitrage mechanisms and Automated Market Maker (AMM) used to fascilitate trades and price equilibria. I decided to build out a simulation of current conditions an what/how things might change under a different market mechanism.

This repo contains python-simulated functions that allow:
- Constant Product swaps
- vAMM Swaps and Pool Tracking
- dynamic AMM Swap and Pool Tracking
- Integration of dynamic and virtual AMMs into a single AMM.

Charts and graphs are created based upon various parameters that the user may set/adjust to determine base-case, noise, and other conditions.

**Installation (How does a user clone or get the code and data?)**
Make sure the following python packages are installed and working:
- random
- math
- numpy
- matplotlib (specifically .pyplot)

Create a pull-request and it's good to go.
*note: This project was coded in the SPYDER IDE: Incompatabilities might occur using other IDEs*

**Usage (How does a user use the code?)**
Manipulate any variable in 'build oracle' or 'define global variables' to change:
- number of transactions to test
- oracle conditions
- CDP variables such as liquidation discount and user risk tolerance
After the desired parameters are set, run the code to build plots that you can use to visualize the behavior of the set parameters. See below some examples.

![Figure 2022-04-25 090506](https://user-images.githubusercontent.com/102979899/167237484-b49377ec-b1e8-4771-9a8d-5cc985df1c9b.png)
![Figure 2022-04-25 090523](https://user-images.githubusercontent.com/102979899/167237486-1cb3af27-ac5a-44d4-a2b1-09654580eb77.png)
![Figure 2022-04-25 090531](https://user-images.githubusercontent.com/102979899/167237488-203c4e73-28d2-4cda-a3a7-51b22a03cb5a.png)
