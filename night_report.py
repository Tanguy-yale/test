#!/opt/anaconda/bin/python

#set up the class so that we can read the response form and assign atributes to each night
class nightReport:
	def __init__(self,submit,bon,obs,obsast,wthr,ssee,lsee,hrobs,hrtoo,hreng,hrsys,hrwthr,dis,comments):
		self.submit=submit
		self.bon=bon
		self.obs=obs
		self.obsast=obsast
		self.wthr=wthr
		self.ssee=ssee
		self.lsee=lsee
		self.hrobs=hrobs
		self.hrtoo=hrtoo
		self.hreng=hreng
		self.hrsys=hrsys
		self.hrwthr=hrwthr
		self.dis=dis
		self.comments=comments

#this will handle multiple responses are given for weather and store them in a list
	def wthrExp(self):
		return self.wthr.split(', ')

#this will handle multiple responses are given for disposition and store them in a list 
	def disExp(self):
		return self.dis.split(', ')

#this list, nights, will hold each class. each class will be its own element
nights=[]

inputfile=open('15mResponses.tsv')

for line in inputfile:
	s=line.split('\t') #we are expecting the response form to be tab delimited
	nights.append(nightReport(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11],s[12],s[13]))

inputfile.close()

#find how many nights there were. subtract one because the column headings are also included
totnights=len(nights)-1

#find sums of hours observing etc. dont bother with the 0th index, it is the column headings
obstothr=sum([float(nights[i].hrobs) for i in range(1,totnights + 1)])
tootothr=sum([float(nights[i].hrtoo) for i in range(1,totnights + 1)])
engtothr=sum([float(nights[i].hreng) for i in range(1,totnights + 1)])
systothr=sum([float(nights[i].hrsys) for i in range(1,totnights + 1)])
wthrtothr=sum([float(nights[i].hrwthr) for i in range(1,totnights + 1)])

#find the range of the minimum seeing and the maximum seeing
minssee=min([float(nights[i].ssee) for i in range(1, totnights + 1)])
minlsee=min([float(nights[i].lsee) for i in range(1, totnights + 1)])
if minssee < minlsee:
	minsee=minssee
else:
	minsee=minlsee

maxssee=max([float(nights[i].ssee) for i in range(1, totnights + 1)])
maxlsee=max([float(nights[i].lsee) for i in range(1, totnights + 1)])
if maxssee < maxlsee:
	maxsee=maxlsee
else:
	maxsee=maxssee

#find the different weather types experienced, and count the instances of each
#use wthrExp() defined above to split up instances of multiple weather types experienced
#wthrexp will be a list which contains a list for each night whcih contains the weather types experienced
wthrexp=[nights[i].wthrExp() for i in range(1,len(nights))]

#we just want one list with the weather responses given, so flatten out wthrexp
w=[]
for i in range(0,len(wthrexp)):
	for j in range(0,len(wthrexp[i])):
		w.append(wthrexp[i][j])

#wset contains the unique values of w
wset=set(w)
wsetcount=[(x, w.count(x)) for x in wset]
wsetcountdict=dict(wsetcount)	#wsetcountdict is a dictionary whose keys are weather and values are # reported

#print our results
print 'weather types experienced'
for key in wsetcountdict:
	print key, wsetcountdict[key]
print 'total nights :' + str(totnights)
print 'seeing range :' + str(minsee) + '-' + str(maxsee)
print 'total hours spent observing :' + str(obstothr)
print 'total hours spent on ToO    :' + str(tootothr)
print 'total hours lost to engineering :' + str(engtothr)
print 'total hours lost to system failure : '+ str(systothr)
print 'total hours lost to weather :' + str(wthrtothr)
