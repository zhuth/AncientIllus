# coding: utf-8
import requests, codecs, sys
fn = sys.argv[1]
x = sys.argv[3]
f = codecs.open(fn, 'w', 'gbk')
ck = {}
print sys.argv
r = requests.get(('http://query.clcn.net.cn/GJAndST/gjct%s.asp?Direction=New&IType=' % x) + sys.argv[2], cookies=ck)
r.encoding = 'gbk'
f.write(r.text)
ls = r.text
print r.text
ck = r.cookies
i = 0
while True:
	i += 1
	r = requests.get('http://query.clcn.net.cn/GJAndST/gjct%s.asp?Direction=Next' % x, cookies=ck)
	r.encoding = 'gbk'
	if r.text == ls:
		break
	f.write(r.text)
	ls = r.text
	print i
f.close()
