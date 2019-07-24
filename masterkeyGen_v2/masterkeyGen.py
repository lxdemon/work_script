import re
import time
import pdutil


class Masterkey(object):

    def __init__(self):
        self.master_key = [0] * 16
        self.masterkeyList = []
        self.macList = []

    def generateOne(self, macaddr):
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

        self.master_key[0] = seed[0] + a + 1
        self.master_key[1] = seed[1] + self.master_key[0] + b + 1 + a + 1
        self.master_key[2] = seed[2] + self.master_key[1] + c + 1 + b + 1 + a + 1
        self.master_key[3] = seed[3] + self.master_key[2] + d + 1 + c + 1 + b + 1 + a + 1
        self.master_key[4] = seed[4] + self.master_key[3] + e + 1 + d + 1 + c + 1 + b + 1 + a + 1
        self.master_key[5] = seed[5] + self.master_key[4] + d + 3 + c + 2 + b + 1 + f + 1
        self.master_key[6] = seed[6] + self.master_key[5] + c + 3 + b + 2 + g + 1
        self.master_key[7] = seed[7] + self.master_key[6] + b + 2 + h + 1
        self.master_key[8] = seed[8] + self.master_key[7] + j + 1
        self.master_key[9] = seed[9] + self.master_key[8] + b + 5 + a + 1
        self.master_key[10] = seed[10] + self.master_key[9] + c + 7 + b + 5 + a + 1
        self.master_key[11] = seed[11] + self.master_key[10] + d + 9 + c + 7 + b + 5 + a + 1
        self.master_key[12] = seed[12] + self.master_key[11] + e + 11 + d + 9 + c + 7 + b + 5 + a + 1
        self.master_key[13] = seed[13] + self.master_key[12] + d + 9 + c + 7 + b + 5 + f + 1
        self.master_key[14] = seed[14] + self.master_key[13] + c + 7 + b + 5 + g + 1
        self.master_key[15] = seed[15] + self.master_key[14] + b + 5 + h + 1

        for k in range(16):
            self.master_key[k] = self.master_key[k] & 0xff

        for k in range(16):
            temp = self.master_key[k]
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
            self.master_key[k] = temp

        temp = self.master_key[15] % 15
        while temp > 0:
            temp2 = self.master_key[0]

            for k in range(15):
                self.master_key[k] = self.master_key[k+1]
            self.master_key[15] = temp2
            temp = temp - 1

        for k in range(16):
            self.master_key[k] = chr(self.master_key[k])

        self.masterkeyList.append(''.join(self.master_key))

    def generate(self, mac_start, mac_end):
        self.macList = list( range(mac_start, mac_end + 1) )

        self.macList = ["{:#014X}".format(it) for it in self.macList]

        for index, mac in enumerate(self.macList):
            self.macList[index] = mac[2:]

        for mac in self.macList:
            self.generateOne(mac)
        
        return index + 1

    def save(self, file_to_save):
        now = time.strftime('%Y%m%d', time.localtime())
        split_name = file_to_save.split('.')
        file_name = split_name[0] + '_' + now + '.' + split_name[1]

        pdutil.save2xls(file_name, {'mac': self.macList, 'masterkey': self.masterkeyList})
        
        return (file_name)


if __name__ == "__main__":

    masterkey = Masterkey()
    num = masterkey.generate(int('000000000000',16), int('000000000011',16))

    print("{} masterkey generated".format(num))
    # for idx in range(num):
        # print("{}:{}".format(masterkey.macList[idx], masterkey.masterkeyList[idx]))

    file_path = masterkey.save('masterkeyGen_test.xlsx')
    print('Masterkey has been write to {}'.format(file_path))
    
