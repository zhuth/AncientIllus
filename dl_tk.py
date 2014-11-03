# coding: utf-8
'''
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
'''

import sys, sqlite3, re, codecs
conn = sqlite3.connect('data.sqlite3')
conn.text_factory = str
c = conn.cursor()
c.execute('PRAGMA encoding = "UTF-8";')
c.execute(''' CREATE TABLE IF NOT EXISTS links(
	ID int,
	TITLE text UTF8,
	AUTHOR text UTF8,
	METHOD text UTF8,
	PERSON text,
	LOCATION text,
	SOURCE text,
	CLASSIFIER text
)''')
conn.commit()
fn =  sys.argv[1]
f = codecs.open(fn, 'r', 'gbk')
s = f.read()
p = re.compile(r"<tr.*?>.*?</tr>", re.MULTILINE|re.DOTALL)
for m in p.finditer(s):
	it = m.group().encode('utf8')
	if 'A HREF' in it.upper() and not ('上一页' in it):
		its = re.split(r'</td>\s+<td>', it)
		if len(its) < 3:
			continue
		lnk = its[0]
		lnk = lnk[lnk.find('WXID=') + 5:]
		lnk = lnk[:lnk.find('"')]
		for i in range(0, len(its)):
			its[i] = re.sub('<.*?>|\s|&nbsp;', '', its[i])
		sql = 'INSERT INTO links(ID, TITLE, AUTHOR, METHOD, PERSON, LOCATION, SOURCE, CLASSIFIER) values(?, ?, ?, ?, ?, ?, ?, ?)'
		c.execute(sql, (lnk, its[0], its[1], its[2], its[3], its[4], its[5], fn))
conn.commit()
c.close()
conn.close()