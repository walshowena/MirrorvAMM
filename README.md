
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
After the desired parameters are set, run the code to build plots that you can use to visualize the behavior of the set parameters.
