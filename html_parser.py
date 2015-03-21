__author__ = 'tony'
import re
import copy
from collections import deque


class Tag:
    def __init__(self):
        self.name=""
        self.children=[]
        self.attr={}
        self.par=None
        self.closed=False
        self.text=''

    """def __int__(self,name):
        self.name=name
        self.children=[]
        self.attr=[]
        self.par=None
        self.closed=False
        self.text=''
    """
    def __init__(self,name='',attr=[],txt=''):
        self.name=name
        self.attr=attr
        self.text=txt
        self.children=[]
        self.par=None
        self.closed=False

    def addChild(self,tag):
        tag.par=self
        self.children.append(tag)

    def size(self):
        if len(self.children)==0:return 1
        return reduce(lambda x,y:x.size()+y.size(),self.children)

    def height(self):
        if len(self.children)==0:return -1
        return 1+max(self.children,key=lambda x:x.height()).height()

    def pathTo(self,tar):
        if tar==self: return []
        route=[self]
        t=self
        while t!=tar:
            t=t.par
            route.append(t)
        route=route[:-1]
        return route[::-1]


    def pathToRoot(self):
        root=self
        route=[]
        route.append(root)
        while root.par!=None:
            root=root.par
            route.append(root)
        route=route[:-1]
        return route[::-1]
    """
    :arg function-labda function returns value for which the function is true
    #give lambda function like x:x.name=="lala"
    """
    def find(self,function):
        if function(self):
            return self
        if len(self.children)>0:
            for i in range(len(self.children)):
                ret=self.children[i].find(function)
                if ret!=None:return ret
        return None

    def findParent(self,f):
        if self.par==None:return None
        if f(self.par):return self.par
        return self.par.findParent(f)

    def findAll(self,f):
        mtc=[]
        for i in range(len(self.children)):
            if f(self.children[i]):
                mtc.append(self.children[i])
        return mtc

    def distinct(self,other_tag):
        s=self.name*(self.name!=other_tag.name)
        t=self.text*(self.text!=other_tag.text)
        c=set(self.attr.items())-set(other_tag.attr.items())
        c={e[0]:e[1] for e in c}
        return Tag(s,c,t)

    def intersect(self,other_tag):
        s=self.name*(self.name==other_tag.name)
        c=set(self.attr.items()) & set(other_tag.attr.items())
        c={e[0]:e[1] for e in c}
        return Tag(s,c,'')
    #1.identify most promising tree
    #1.1 find subtree with most matches for pattern
    #2.search for full pattern in subtree
    #3.extract path to root
    #4.correlate path with similar trees
    def containsSubtrees(self,ofSize):
        if self.height()==0:return False
        if self.size()>=ofSize:return True
        return self.children[0].containsSubtrees()

    def __eq__(self,other):
        if type(other) is not Tag:return False
        return self.name==other.name and set(self.attr)==set(other.attr)

    def __str__(self):
        return self.name+("='"+self.text+"'")*(self.text!='')+' '+("["+';'.join('@'+k+"='"+self.attr[k]+"'" for k in self.attr)+"]")*(self.attr!={})

    def toString(self,f,t=True):
        ps=dict((k,v) for (k,v) in self.attr.items() if f((k,v)))
        return self.name+("='"+self.text+"'")*(t)+' '+("["+';'.join('@'+k+"='"+ps[k]+"'" for k in ps)+"]")*(ps!={})

class Match:
    def __init__(self,obj,wds):
        self.words=wds
        self.obj=obj
    def addWord(self,w):
        if w not in self.words:self.words.append(w)

class HtmlPage:

    def __init__(self,page):
        rx=re.compile(r'((?<=\>)\s+(?=\<))|(<!doctype html.*>)|(<!--[\s\S]*?-->)|(<meta.*>)',re.IGNORECASE)
        self.page=rx.sub('',page)
        self.page=re.sub(r'(<(script|head|footer)>).*(</(script|head|footer)>)','',self.page,re.I)#filter page
        #self.page=re.sub(r'\s{2,}','',self.page)
        self.root=None
        self.buildTree()

    def find(self,f):
        return self.root.find(f)

    def closeBracket(self,i):
        tag=Tag()
        current_string=""
        props_string=""
        prop=False
        props={}
        stack=[]
        while(i<len(self.page) and self.page[i]!='>'):
            if self.page[i].isspace() and not prop:
                if tag.name=="":tag.name=current_string.strip('</')
                current_string=""
            elif self.page[i:i+2]=='/>':#self.page[i]=="/" and self.page[i+1]=='>':
                tag.closed=True
            elif self.page[i]=="=":
                props_string=current_string
                current_string=""
                prop=True
            elif self.page[i]=='"':
                if len(stack)>0:
                    props[props_string]=current_string#((props_string,current_string))
                    props_string=""
                    current_string=""
                    prop=False
                    stack.pop()
                else:
                    stack.append(self.page[i])
            else:
                current_string += self.page[i]
            i+=1
        #=self.page[i-1]
        if props_string!='' and current_string!='':
            props[props_string]=current_string
            current_string=''
        tag.name=current_string.strip('</') if current_string!="" else tag.name
        tag.attr=props
        return(tag,i)

    def buildTree(self):
        stack=[]
        txtStack=[""]
        i=0
        while(i<len(self.page)):
            if(self.page[i]=="<"):
                if self.page[i+1]=="/":
                    t=self.closeBracket(i+1)
                    not_found=True
                    while not_found and len(stack)>0:
                        #print stack[-1].name
                        if stack[-1].name==t[0].name:
                            not_found=False
                            if len(stack)==1:
                                self.root=stack.pop()
                                return
                            tag=stack.pop()
                            tag.text=txtStack.pop()
                            if len(stack)>0:stack[-1].addChild(tag)
                        else:
                            stack.pop()
                    i=t[1]
                else:
                    t=self.closeBracket(i+1)
                    if t[0].closed:
                        stack[-1].addChild(t[0])
                    else:
                        stack.append(t[0])
                        txtStack.append("")
                    i=t[1]
            else:
                txtStack[-1] += self.page[i]
            i+=1
        self.root=stack.pop()

    def getProps(self,s):
        p={}
        for i in range(len(s)):
            s1=s[i].strip("@").split("=")
            p[s1[0]]=s1[1].strip("'")
        return p
	
    def goTo(self,start,xpath):
        if '{'in xpath and not xpath[0]=='{':
            xa=xpath[xpath.index("{"):xpath.index('}')+1]
            xpath=xpath[:xpath.index("{")]
            xp=xpath.split("/")
            xp.append(xa)
        else:
            xp=xpath.split("/")
        ix=start
        for i in range(len(xp)):
            f=lambda x:x.name==xp[i].strip(' ')
            if xp[i]=='':continue
            if xp[i]=="*":
                return ix.children,""
            elif xp[i].startswith("@") or '{' in xp[i]:#.contains('{'):
                return ix,xp[i]
            elif '[' in  xp[i]:#.contains("["):
                #warning do not use regex python is NOT a real language and does not support it!!!
                tag=xp[i][:xp[i].index('[')-1]
                p=self.getProps(xp[i][xp[i].index("[")+1:xp[i].index(']')].split(";"))
                #sp=set(p)
                f=lambda x:x.name==tag and x.attr==p
            elif '=' in xp[i]:#.conatins('='):
                s=xp[i].split("=")
                s[1]=s[1].strip("'")
                f=lambda x:x.name==s[0] and x.text==s[1]

            """elif xp[i].startswith("@"):
                return ix.attr[xp[i].strip('@')]
            elif xp[i].contains('{'):
                return ix,xp[i]
            """
            ix=ix.find(f)
            if ix==None:return None,None
        return ix,None

    def getValue(self,start,p):
        t,s=self.goTo(start,p)
        if t==None:return ''
        if s!=None:
            return t.attr[s.strip('@')]
        return t.text

    def getFromXPath(self,s):
        if s=='':return None
        t,s=self.goTo(self.root,s)
        if t is None:return None
        tmpl=s.strip('{}').split(',')
        tmpl=[tmpl[i].split(':') for i in range(len(tmpl))]
        res=[]
        td={tmpl[i][0]:tmpl[i][1] for i in range(len(tmpl))}
        for i in range(len(t.children)):
            r=copy.deepcopy(td)
            for k in r:
                tc=self.getValue(t.children[i],r[k])
                r[k]=tc
            res.append(r)
        return res

    def bfs(self,start):
        d=deque()
        d.append(start)
        res=[]
        while not len(d)==0:
            n=d.popleft()
            if n.height()==1:
                res+=n.children
            else:
                d+=n.children
        return res

    def identifySubtree(self,c):
        leaves=self.bfs(self.root)
        #matches={}
        candidates={}#node.name(root of tree):found children
        targets=c.patterns()
        for i in range(len(leaves)):
            for t in targets:
                m1=c.belongsTo(leaves[i].text,t)
                if m1=='1' or (m1!='2' and m1!='0'):
                    tr=leaves[i].findParent(lambda x:len(x.children)>2)
                    if tr!=None:
                        if str(tr) in candidates:
                            candidates[str(tr)].addWord(t)
                        else:
                            candidates[str(tr)]=Match(tr,[t])
                    #if tr != None:candidates[tr]=candidates.get(tr,[])+[t]
                    #matches[t]+=leaves[i]
                    #targets.remove(t)
                elif m1=='2':
                    #matches[t]+=leaves[i+1]
                    if not i+1>len(leaves)-1:
                        tr=leaves[i+1].findParent(lambda x:len(x.children)>2)
                        i+=1
                        if tr!=None:
                            if str(tr) in candidates:
                                candidates[str(tr)].addWord(t)
                            else:
                                candidates[str(tr)]=Match(tr,[t])
                        #if tr != None:candidates[tr]=candidates.get(tr,[])+[t]

                elif m1=='0':
                    m2=c.belongsTo(','.join(leaves[i].attr.values()),t)
                    if m2=='0':
                        pass
                    else:
                        tr=leaves[i].findParent(lambda x:len(x.children)>2)
                        #if tr != None:candidates[tr]=candidates.get(tr,[])+[t]
                        if tr!=None:
                            if str(tr) in candidates:
                                candidates[str(tr)].addWord(t)
                            else:
                                candidates[str(tr)]=Match(tr,[t])
                        #targets.remove(t)
        #candidates={k:list(set(candidates[k])) for k in candidates}
        candidates=candidates.values()
        candidates.sort(key=lambda x:(len(x.words),len(x.obj.children)),reverse=True)
        return candidates

    def pathToString(self,path):
        s='/'
        for i in range(len(path)):
            s+=path[i].toString(lambda x:not x[1].isdigit() and not '/' in x[1] and not ';' in x[1],False)+'/'
        return s

    def getExactPath(self,c,t,wds):
        l=self.bfs(t)
        wl=[]
        wds=sorted(wds)
        for w in wds:
            for j in range(len(l)):
                m=c.belongsTo(l[j].text,w)
                if m=='1':
                    tr=l[j] if l[j].text!='' else l[j].find(lambda x:x.text!='')
                    wl.append(w+':'+self.pathToString(tr.pathTo(t)))
                    l.remove(l[j])
                    break
                elif m=='2':
                    if j+1>len(l)-1:break
                    tr=l[j+1] if l[j+1].text!='' else l[j+1].find(lambda x:x.text!='')
                    wl.append(w+':'+self.pathToString(tr.pathTo(t)))
                    l.remove(l[j+1])
                    l.remove(l[j])
                    break
                elif m=='0':
                    m=c.belongsTo(','.join(l[j].attr.values()),w)
                    if m=='1' or m=='2':
                        tr=l[j] if l[j].text!='' else l[j].find(lambda x:x.text!='')
                        wl.append(w+':'+self.pathToString(tr.pathTo(t)))
                        l.remove(l[j])
                        break
                    elif m!='0':
                        tr=l[j] if m in l[j].attr.keys() else l[j].find(lambda x:m in x.attr.keys())
                        wl.append(w+':'+self.pathToString(tr.pathTo(t))+'@'+m)
                        l.remove(l[j])
                        break
                else:
                    tr=l[j] if m in l[j].attr.keys() else l[j].find(lambda x:m in x.attr.keys())
                    wl.append(w+':'+self.pathToString(tr.pathTo(t))+'@'+m)
                    l.remove(l[j])
                    break
        res=','.join(wl)
        return res

    def buildXPath(self,c):
        stree=self.identifySubtree(c)
        if len(stree)==0:return ''
        missing=list( set(c.patterns())-set(stree[0].words))
        target=stree[0].obj.par
        xp='{'+self.getExactPath(c,stree[0].obj.par,stree[0].words)
        if len(missing)>0:
            for i in range(len(stree[0].obj.par.children)):
                if not stree[0].obj.par.children[i]==stree[0].obj:
                    s=self.getExactPath(c,stree[0].obj.par.children[i],missing)
                    if s!='':
                        xp+=','+s
                        break
        xp+='}'
        target= target if len(target.children)>2 else target.findParent(lambda x:len(x.children)>2)
        if target is None :return ''
        xp=self.pathToString(target.pathToRoot()) + xp
        return xp
