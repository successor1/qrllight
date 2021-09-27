# Qrllight Wallet Update



## New Features



- Dice.py or another similar method to create entropy 

- Slaves.json implementation

- Efficient history implementation

- Fixing input bugs

- Confirmation before sending

- Send QRL to multiple recipients





The following will present a detailed description of the features.



## Creating entropy by mouse movements

It is now possible to create entropy by random mouse movements. The program does the following: It takes the x and y coordinates when you hover over area with your mouse, shuffles them and then inserts them into getRandomSeed(). This is experimental and not safe for mainnet use. This is because it could be predictable, the mouse area is limited, so are the number of inputs, this means less randomness than /dev/urandom. Another method would still not be reliable because there is no mathematical evaluation. /dev/urandom is still the recommended method for creating entropy.



## Slaves.json implementation

Slaves.json can now be created from GUI, you can do this by opening from your secure wallet file, wait about 10 minutes and you will get your slaves.json file in your current directory. You will have to move this to the mining node inside ~/.qrl/. Doing this from mnemonic / hexseed works now too.



## Efficient history implementation

History works, you will see your last 10 transactions. Datetime and amount are being shown.



## Fixing input bugs

For seed input, you will see a green, yellow or red line around the input box. This indicates whether your seed is correct. This is done with regex. For the sending view, there are input checks for fee and OTS key.



## Confirmation before sending

Confirmation before sending works.



## Send QRL to multiple recipients

Sending QRL to multiple recipients works. QRL address format: address1 address2. Amount format: amount1 amount2.