import re

balance_numbers_only = re.sub("[^0-9]", "", "Balance: 38.169999989 QUANTA")
print(int(balance_numbers_only) / 1000000000)