awd-framework（python2.7）
    主机管理：ssh连接，切换主机，打包文件到本地，webshell查找，敏感文件，恢复备份，布waf（php，（python，pwn））,流量管理
    自动攻击：后门利用，流量混淆，编写脚本放在指定目录下（set hosts,set ports,set c段）
    肉鸡管理：
    flag提交：

用到的库：requests,re,paramiko,os,pickle

ip控制

TODO:
    -参数检查还没写！！！
    -后期加一个好看的输出函数
    -敏感文件查找
    -webshell查找，linux实现更方便
    -攻击脚本预定义函数
    -根据流量直接生成exp
    -异常处理
    +利用 pickle 库，存储基本信息（备份源码等字典信息）
    +检测是否有信息，有的话直接连接 不需要手动重连

测试：
    ssh_add 129.211.0.177  9011  root  qazwsxedc  web1
    ssh_add 129.211.0.177  9012  root  tyutyutyu  web2

    主机1：
            web服务地址：129.211.0.177:9001
            ssh地址：129.211.0.177:9011	  密码：qazwsxedc
    主机2：
            web服务地址：129.211.0.177:9002
            ssh地址：129.211.0.177:9012	  密码：tyutyutyu
    主机3：
            web服务地址：129.211.0.177:9003
            ssh地址：129.211.0.177:9013	  密码：ploploplo

碰到的问题：
    pickle时 session一直报错，后来想起来session里面是直接初始化了一个ssh类的