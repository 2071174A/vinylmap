__author__ = 'tony'
from math import *
import re

def loadSModel(file):
    sm={}
    fl=open(file,"r").read().decode('mbcs').splitlines()
    for i in range(len(fl)):
        if fl[i].startswith('//'):continue
        l=fl[i].split("==")
        sm[l[0]]=l[1].split(';')
    return sm

class Classifier:
    def classify(self,sample):
        pass
    def belongsTo(self,s,m):
        pass
    def patterns(self):
        pass
#region "Bayes"
class Sample:
    def __init__(self,txt):
        self.text=re.sub('\s(to|and|or|with|an|a|the|on|then|that|which|else|\,|for|are)\s'," ",txt)
        self.words={}
        self.extractData()

    def extractData(self):
        wds=self.text.lower().split(" ")
        size=len(wds)
        for i in range(len(wds)):
            self.words[wds[i]]+=1
        for k in self.words.keys():
            self.words[k]/=size

    def size(self):
        return len(self.words)
class Feature:
    def __init__(self,m,ms,n):
        self.mean=m
        self.m2=ms
        self.n=n

    def mean(self):
        return self.mean

    def variance(self):
        return self.m2/self.mean

    def addValue(self,x):
        self.n+=1
        delta=self.mean+(x-self.mean)/self.n
        self.m2+=(x-self.mean)*(x-delta)
        self.mean=delta

class Model:
    def __init__(self,c,name):
        self.ft={}#features {name:Feature} must be sorted by name
        self.n=1
        self.classifier=c
        self.name=name
    def prior(self):
        return self.n/self.classifier.n
    def condProbFor(self,x):
        if not x[0] in self.ft.keys():return 1
        s=self.ft[x[0]]
        return (1/sqrt(2*pi*s.variance()))*exp(-((x[1]-s.mean())**2)/2*s.variance())

class NaiveBayes(Classifier):
    def __init__(self):
        self.models=[]
        self.n=1
    def train(self,m,sample):
        s=Sample(sample)
        m.n+=1
        self.n+=1
        for k in s.words.keys():
            if not m.ft.has_key(k):
                m.ft[k]=Feature(0,0,0)
            m.ft[k].addValue(s.words[k])
        return m
    """
        :arg samples-list of text
    """
    def createModel(self,name,samples):
        m=Model(self,name)
        for i in range(len(samples)):
            m=self.train(m,samples[i])
        m.n=len(samples)
        self.n+=len(samples)
        self.models.append(m)

    def classify(self,sample):
        maxM=None
        for i in range(len(self.models)):
            p=math.log(self.models[i].prior())
            m=self.models[i]
            for j in sample.words.items():
                #p+=math.log((1/sqrt(2*pi*m.ft[j].variance()))*exp(-(sample.words[j]-m.ft[j].mean())**2/2*m.ft[j].variance()))
                p+=math.log(m.condProbFor(j))
            if maxM is None or p>maxM[1]:
                maxM=(m,p)
        self.train(maxM[0],sample)
        return maxM[0]

    def belongsTo(self,s,m):
        return self.classify(s).name==m.name
#endregion

class RuleClassifier(Classifier):
    def __init__(self,model={}):
        self.kwds=model
    #0-no match
    #1-strong match(matched re pattern)
    #2-weak match(matched keyword)
    def belongsTo(self,s,m):
        if not m in self.kwds.keys() or type(s) is not str:return '0'
        if s=='':return '0'
        if self.kwds[m][1]!='':
            if re.search(u'('+ self.kwds[m][1] +')',s,re.UNICODE and re.I) is not None:return self.kwds[m][2] or '1'
        if self.kwds[m][0]=='':return '0'
        return self.kwds[m][2] or '2' if re.search(u'(' + self.kwds[m][0] +')',s,re.UNICODE and re.I) is not None else '0'

    def patterns(self):
        return self.kwds.keys()

    def classify(self,sample):
        for k in self.kwds:
            p=self.belongsTo(sample,k)
            if p!='0':return[k,p]
        return None

		
