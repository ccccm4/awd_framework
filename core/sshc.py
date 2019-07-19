# _*_ coding: utf8 _*_

import paramiko
import re
import os
import pickle

# ad_server = {}
# server_sessions = {}
# backups = {}

def check_ip(ipAddr):
    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True    
    else:    
        return False

# from https://blog.csdn.net/u012322855/article/details/77839929
class SSHConnection(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = int(port)
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._connect()
 
    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        transport.connect(username=self._username, password=self._password)
        self._transport = transport
 
    #下载
    def download(self, remotepath, localpath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath)
 
    #上传
    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath)
 
    #执行命令
    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            print data.strip()   #打印正确结果
            return data
        err = stderr.read()
        if len(err) > 0:
            print err.strip()    #输出错误结果
            return err

    def deploy_waf(self):
        self.exec_command('mkdir /tmp/logs')
        self.exec_command('chmod -R 777 /tmp/logs')
        self.exec_command('python /tmp/setup.py')
 
    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()

class SSH_control():
    def __init__(self):
        # 从pickle中导入
        try:
            with open('data/ad_server.pickle','r') as fp:
                self.ad_server = pickle.load(fp)
            with open('data/backups.pickle','r') as fp:
                self.backups = pickle.load(fp)
        except:
            self.ad_server = {}
            self.backups = {}

        self.server_sessions = {}
        self.initialize()

        # 生成初始化的pickle文件
        # with open('data/ad_server.pickle','wb') as fp:
        #     pickle.dump(self.ad_server,fp)
        # with open('data/server_sessions.pickle','wb') as fp:
        #     pickle.dump(self.server_sessions,fp)
        # with open('data/backups.pickle','wb') as fp:
        #     pickle.dump(self.backups,fp)
        

    # ip,port,username,password,ad_server_name
    def add(self,argv_array,ad_server_name,status='0'):
        # print 'add'
        if False == check_ip(argv_array[0]):
            pass
        else:
            self.ad_server[ad_server_name] = argv_array
            self.server_sessions[ad_server_name] = SSHConnection(self.ad_server[ad_server_name][0],self.ad_server[ad_server_name][1],self.ad_server[ad_server_name][2],self.ad_server[ad_server_name][3])
            if status == '0':
                # 备份初始文件
                lpath = './original_backup/'+ad_server_name+'_original'+'.tar.gz'
                self.backups[ad_server_name] = {}
                self.backups[ad_server_name]['original'] = lpath
                self.backup(ad_server_name,lpath,'original')
                # 上传waf文件
                self.server_sessions[ad_server_name].put('./source/waf12.php','/tmp/waf.php')
                self.server_sessions[ad_server_name].exec_command('chmod +x /tmp/waf.php')
                self.server_sessions[ad_server_name].put('./source/setup.py','/tmp/setup.py')
                self.server_sessions[ad_server_name].exec_command('chmod +x /tmp/setup.py')
                self.check_webshell(lpath)
            with open('data/ad_server.pickle','wb') as fp:
                pickle.dump(self.ad_server,fp)

    def show_server(self):
        #print self.ad_server
        print self.server_sessions
        for key, value in self.ad_server.iteritems():
            print key,value

    # 备份文件
    def backup(self,ad_server_name,local_path,version,wwwroot='/var/www/html/'):
        remote_path = '/tmp/' + ad_server_name + '_' + version + '.tar.gz'
        cmd = 'tar zcvf '+ remote_path + ' ' + wwwroot + '*'
        self.server_sessions[ad_server_name].exec_command(cmd)
        self.server_sessions[ad_server_name].download(remote_path,local_path)
        with open('data/backups.pickle','wb') as ff:
            pickle.dump(self.backups,ff)

    # 恢复文件
    def recover(self,ad_server_name,version,wwwroot='/var/www/html/'):
        lpath = './backup/'+ad_server_name+'_'+version+'.tar.gz'
        self.server_sessions[ad_server_name].put(lpath,'/tmp/recover.tar.gz')
        cmd = 'tar -zxvf /tmp/recover.tar.gz -C '+wwwroot
        self.server_sessions[ad_server_name].exec_command(cmd)

    # 检查webshell 检查敏感文件
    def check_webshell(self,path):
        # 检查敏感文件
        # cmd = 'tar -zxvf '+path+' -C ./tmp/'
        # os.system(cmd)
        # 读取文件名字

        # 检查webshell hm
        pass

    # 初始化，连接ssh
    def initialize(self):
        if self.ad_server:
            for key, value in self.ad_server.iteritems():
                self.server_sessions[key] = SSHConnection(value[0],value[1],value[2],value[3])


    
