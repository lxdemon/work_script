"""
requirements:
    pip install xlrd
    pip install xlwt
    pip install openpyxl
    pip install pandas
"""

import os
import time
import re
import pandas as pd


mac_start = 0x8C147D307CE4
mac_end = 0x8C147D30A32B
file_to_save = 'mac_masterkey.xlsx'


master_key = [0] * 16
masterkeyList = []

maclist = list(range(mac_start, mac_end + 1))

maclist = [hex(it) for it in maclist]
for i, mac in enumerate(maclist):
    maclist[i] = mac[2:]


def masterkeyGen(macaddr):
    seed = [114,69,109,79,84,101,67,48,99,79,110,69,120,85,109,49]

    res = re.findall(r'\S{1}', macaddr)
    a = int(res[11], 16)
    b = int(res[10], 16)
    c = int(res[9], 16)
    d = int(res[8], 16)
    e = int(res[7], 16)
    j = int(res[6], 16)

    h = int(res[4], 16) * 16 + int(res[5], 16)
    g = int(res[2], 16) * 16 + int(res[3], 16)
    f = int(res[0], 16) * 16 + int(res[1], 16)

    k = 0
    temp = 0
    temp2 = 0

    master_key[0] = seed[0] + a + 1
    master_key[1] = seed[1] + master_key[0] + b + 1 + a + 1
    master_key[2] = seed[2] + master_key[1] + c + 1 + b + 1 + a + 1
    master_key[3] = seed[3] + master_key[2] + d + 1 + c + 1 + b + 1 + a + 1
    master_key[4] = seed[4] + master_key[3] + e + 1 + d + 1 + c + 1 + b + 1 + a + 1
    master_key[5] = seed[5] + master_key[4] + d + 3 + c + 2 + b + 1 + f + 1
    master_key[6] = seed[6] + master_key[5] + c + 3 + b + 2 + g + 1
    master_key[7] = seed[7] + master_key[6] + b + 2 + h + 1
    master_key[8] = seed[8] + master_key[7] + j + 1
    master_key[9] = seed[9] + master_key[8] + b + 5 + a + 1
    master_key[10] = seed[10] + master_key[9] + c + 7 + b + 5 + a + 1
    master_key[11] = seed[11] + master_key[10] + d + 9 + c + 7 + b + 5 + a + 1
    master_key[12] = seed[12] + master_key[11] + e + 11 + d + 9 + c + 7 + b + 5 + a + 1
    master_key[13] = seed[13] + master_key[12] + d + 9 + c + 7 + b + 5 + f + 1
    master_key[14] = seed[14] + master_key[13] + c + 7 + b + 5 + g + 1
    master_key[15] = seed[15] + master_key[14] + b + 5 + h + 1

    for k in range(16):
        master_key[k] = master_key[k] & 0xff

    for k in range(16):
        temp = master_key[k]
        if temp < 48:
            temp = temp % 10
            temp += 48
        while temp > 122:
            temp = temp - 122
            if temp < 48:
                temp += 48

        if (temp < 97 and temp > 90):
            if temp % 2:
                temp = 97
            else:
                temp = 90

        if (temp < 65 and temp > 57):
            if temp % 2:
                temp = 65
            else:
                temp = 57
        master_key[k] = temp

    temp = master_key[15] % 15
    while temp > 0:
        temp2 = master_key[0]

        for k in range(15):
            master_key[k] = master_key[k+1]
        master_key[15] = temp2
        temp = temp - 1

    for k in range(16):
        master_key[k] = chr(master_key[k])

    masterkeyList.append(''.join(master_key))


for mac in maclist:
    masterkeyGen(mac)

print("Total {} masterkey generated".format(len(maclist)))

now = time.strftime('%Y%m%d', time.localtime())
split_name = file_to_save.split('.')
file_name = split_name[0] + '_' + now + '.' + split_name[1]

writer = pd.ExcelWriter(file_name)
df1 = pd.DataFrame({'mac': maclist, 'masterkey': masterkeyList})
df1.to_excel(writer, sheet_name='mac vs masterkey', header=False, index=False)
writer.save()
print("masterkey saved to {}".format(os.path.abspath(file_name)))
