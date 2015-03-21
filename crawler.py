__author__ = 'tony'
 #-*- coding: utf-8 -*-
import Queue
import threading
import urllib2
import urllib
import sys
import os

import django

from html_parser import *
from classifiers import *


"""
    Job class specification
    url
    title
    artist
"""
def get(url):
    request=urllib2.Request(url)
    request.add_header(key="User-agent",val="tCrawler 1.0")
    response=urllib2.urlopen(request)
    return response.read()
def download(url,path):
    #import os.path
    #if not os.path.exists(path):os.mkdir(path)
    urllib.urlretrieve(url,path)
def fixurl(mess,url):
    if 'http:' not in mess:
            mess='http:'+mess
    if url not in mess:
        mess=url+mess
    return mess
def loadXpath(file):
    print 'loading xpath'
    sm={}
    fl=open(file,"r").read().decode('mbcs').splitlines()
    for i in range(len(fl)):
        if fl[i].startswith('//'):continue
        l=fl[i].split("!")
        sm[l[0]]=l[1]
    return sm

"""
    jobs=store,retrieve data,analyze
    :arg desc=dict{"url":url,"job":"retrieve/store/analyze {path to store data if store}",
    model:{key=name of data field,val=match patterns}
"""

class Minion(threading.Thread):
    def __init__(self,job_queue,result_q,master):
        self.queue=job_queue
        self.result=result_q
        self.master=master
        threading.Thread.__init__(self)

    def run(self):
        print 'running'
        while not self.queue.empty():
            #get next job
            self.job=self.queue.get()
            if self.job["job"].startswith("store"):
                print 'downloading image'
                download(self.job["url"],self.job["path"])
                self.queue.task_done()
            elif self.job["job"]=="retrieve":
                print 'attempting to retrieve data'
                page=HtmlPage(get(self.job['url']))
                res=page.getFromXPath(self.master.xpaths[self.job['url']])
                self.queue.task_done()
                if res==None:
                    self.queue.put({"url":self.job["url"],"job":"analyze"})
                else:
                    if res[0].has_key('cover'):
                        url=re.match(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})\/',self.job['url']).group()
                        for i in range(len(res)):
                            uri=fixurl(res[i]['cover'],url)
                            import uuid
                            fl=str(uuid.uuid1())+'.jpg'
                            res[i]['cover']=fl
                            self.queue.put({'job':'store','url':uri,'path':'static/'+fl})
                    else:
                        for i in range(len(res)):
                            res[i]['cover']='static/egg.png'
                    self.result.put(res)
            elif self.job["job"]=="analyze":
                print 'analyzing page ' + self.job['url']
                page=get(self.job['url'])
                if re.match(r"(not found)|(doesn't exist)",page):
                    self.queue.task_done()
                    del self.master.xpaths[self.job['url']]
                    return
                page=HtmlPage(page)
                s=page.buildXPath(self.master.classifier)
                self.queue.task_done()
                if s=='':continue
                self.master.xpaths[self.job['url']]=s
                self.queue.put({"url":self.job["url"],"job":"retrieve"})


class Crawler:
    def __init__(self):
        self.job_queue=Queue.Queue()
        self.res_queue=Queue.Queue()
        self.xpaths=loadXpath('xpath')
        self.classifier=RuleClassifier(loadSModel('pattern'))

    """def test(self):
        f=open('e:/testsite/t.html')
        page=HtmlPage(f.read())
        c=RuleClassifier(loadSModel(os.path.dirname(os.path.realpath(__file__))+'\pattern'))
        t=page.buildXPath(c)
        print t
    """
    def saveXpath(self):
        f=open('xpath','w')
        for k in self.xpaths:
            f.write(k+'!'+self.xpaths[k]+'\n')
        f.close()

    def explore(self):
        self.tpool=[]
        thrs=min(len(self.xpaths)/2,100)
        for k in self.xpaths:
            self.job_queue.put({'job':'analyze','url':k})
        for i in range(thrs):
            self.tpool.append(Minion(self.job_queue,self.res_queue,self))
        self.job_queue.join()
        self.saveXpath()

    def update(self):
        print 'crawling'
        self.tpool=[]
        thrs=min(len(self.xpaths),100)
        for k in self.xpaths:
            self.job_queue.put({'job':'retrieve','url':k})
        print 'assigning tasks'
        for i in range(thrs):
            m=Minion(self.job_queue,self.res_queue,self)
            self.tpool.append(m)
            m.start()
            m.join()
        self.job_queue.join()
        self.saveXpath()
        while not self.res_queue.empty():
            data=self.res_queue.get()
            print 'populating database'
            for i in range(len(data)):
                store=None
                if all(v=='' for v in data[i].values()):continue
                if 'link' in data[i].keys():
                    import HTMLParser
                    h = HTMLParser.HTMLParser()
                    try:
                        from urlparse import urlparse
                        parsed_uri = urlparse( data[i]['link'] )
                        domain = '{uri.netloc}'.format(uri=parsed_uri)
                        store=Store(link=urllib.quote(data[i]['link'],safe="/"),price=h.unescape(data[i]['price']),name=domain)
                        store.save()
                    except:
                        print data[i]['link']
                        continue
                try:
                    tl=''
                    if not data[i].has_key('artist'):
                        tl=re.split(r'\s\W\s',data[i]['title']) if data[i].has_key('title') else re.split(r'\s\W\s',data[i]['artist'])[0]
                    else:
                        tl=data[i]['artist']
                    record=Record.objects.get(title=unicode(tl,errors='replace'))
                    record.cover=data[i]['cover'] if record.cover=='' else record.cover
                    record.save()
                    if store is not None :record.stores.add(store)
                except Record.DoesNotExist,KeyError:
                    record=None
                    if not data[i].has_key('artist') or not data[i].has_key('title'):
                        s=re.split(r'\s\W\s',data[i]['title']) if data[i].has_key('title') else re.split(r'\s\W\s',data[i]['artist'])
                        if len(s)<2:continue
                        record=Record(title=unicode(s[1],errors='replace'),artist=unicode(s[0],errors='replace'),
                             cover=unicode(data[i]['cover']) if data[i].has_key('cover') else '',cat_no=unicode(data[i]['cat_no'],errors='replace') if data[i].has_key('cat_no') else ''
                             ,label=unicode(data[i]['label'],errors='replace') if data[i].has_key('label') else '',
                            genre=unicode(data[i]['genre']) if data[i].has_key('genre') else '')

                    else:
                        record=Record(unicode(data[i]['title'],errors='replace') if data[i].has_key('title') else '',artist=unicode(data[i]['artist'],errors='replace') if data[i].has_key('artist') else '',
                             cover=data[i]['cover'] if data[i].has_key('cover') else '',cat_no=data[i]['cat_no'] if data[i].has_key('cat_no') else ''
                             ,label=unicode(data[i]['label'],errors='replace') if data[i].has_key('label') else '',
                             genre=data[i]['genre'] if data[i].has_key('genre') else '')
                    try:
                        record.save()
                        if store is not None:record.stores.add(store)
                    except:
                        continue
            self.res_queue.task_done()
        print 'job done'
#p=HtmlPage(open(os.path.dirname(os.path.realpath(__file__))+'/t.html','r').read())
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'vinylmap_project.settings'
application = get_wsgi_application()
django.setup()
from recordstoreapp.models import Record,Store
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
c=Crawler()
c.update()
