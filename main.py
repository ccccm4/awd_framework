# -*- coding: utf-8 -*-

from cmd import Cmd
import os
from core.sshc import *
import pickle
import time
from core.attack import *


class MainConsole(Cmd):
    prompt = "ccc> "
    Object = None

    def __init__(self):
        # SSH 类初始化
        self.sshct = SSH_control()
        # 从pickle中导入
        try:
            with open('data/servers.pickle','r') as fp:
                self.servers = pickle.load(fp)
        except:
            self.servers = []  

        # 生成初始化的pickle文件
        # with open('data/servers.pickle','wb') as fp:
        #     pickle.dump(self.servers,fp)

        # attack 初始化
        self.attack = Attack()

        # Cmd 初始化
        Cmd.__init__(self)

    # About part1 ssh
    def do_ssh_add(self,argv):
        argv_array = argv.split('  ')   # 连接主机的 status 控制
        ad_server_name = argv_array.pop()
        if ad_server_name in self.servers:
            return False
        self.servers.append(ad_server_name)
        with open('data/servers.pickle','wb') as fp:
            pickle.dump(self.servers,fp)
        if len(argv_array) != 4:
            print 'input error'
        else:
            self.sshct.add(argv_array,ad_server_name)
        #self.sshct.add()

    def ssh_remove(self,argv):
        pass
        # 清除
    
    def do_ssh_show(self,argv):
        #print self.servers
        self.sshct.show_server()

    def do_ssh_session(self,argv):
        print self.servers

    def do_ssh_exec(self,argv):
        argv_array = argv.split('  ')   #双空格做分割
        self.sshct.server_sessions[argv_array[0]].exec_command(argv_array[1])

    def do_deploy_waf(self,argv):
        self.sshct.server_sessions[argv].deploy_waf()

    def do_ssh_backup(self,argv):   # ssh_backup web1  v1
        argv_array = argv.split('  ')   # 参数检查还没写
        lpath = './backup/'+argv_array[0]+'_'+argv_array[1]+'.tar.gz'
        self.sshct.backups[argv_array[0]][argv_array[1]] = lpath
        self.sshct.backup(argv_array[0],lpath,argv_array[1])

    def do_show_backup(self,argv):
        print self.sshct.backups

    def do_ssh_recover(self,argv):
        argv_array = argv.split('  ')
        self.sshct.recover(argv_array[0],argv_array[1])

    def do_traffic_down(self,argv):
        cmd = 'tar zcvf /tmp/logs.tar.gz /tmp/logs/*'
        self.sshct.server_sessions[argv].exec_command(cmd)
        cmd = 'rm /tmp/logs/*'
        self.sshct.server_sessions[argv].exec_command(cmd)
        self.sshct.server_sessions[argv].download('/tmp/logs.tar.gz','./logs/'+str(time.time()).replace('.','_')+'_log_'+argv+'.tar.gz')

    # About attack
    def do_set_ip(self,argv):
        argv_array = argv.split('  ')   # set_ip web1  1.1.x.1  80  30
        self.attack.set_ip_1(argv_array[0],argv_array[1],argv_array[2],argv_array[3])

    def do_show_ip(self,argv):
        print self.attack.ip_list

    def do_load_exp(self,argv):
        self.attack.load_exp()

    def do_show_exp(self,argv):
        print self.attack.exploits

    def do_attack(self,argv):
        argv_array = argv.split('  ')
        self.attack.exploit(argv_array[0],argv_array[1])

    def do_sub_flag(self,argv):
        self.attack.submit_flag()

    def do_show_flag(self,argv):
        print self.attack.flag

    def do_mana_shell(self,argv):
        argv_array = argv.split('  ')
        if len(argv_array) == 2:
            self.attack.manage_shell(argv_array[0],argv_array[1])
        else:
            self.attack.manage_shell(argv_array[0])

if __name__ == "__main__":
    test = MainConsole()
    test.cmdloop()


