__author__ = 'tony'
import Queue
import threading
import urllib2
import urllib
from html_parser import *
from classifiers import *
import sys
import os
from models import Store,Record

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

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
    urllib.urlretrieve(url,path)

def loadXpath(file):
    sm={}
    fl=open(file,"r").read().decode('mbcs').splitlines()
    for i in range(len(fl)):
        if fl[i].startswith('//'):continue
        l=fl[i].split(",")
        sm[l[0]]=l[1]
    return sm

class Job(object):
    """
    jobs=store,retrieve data,analyze
    :arg desc=dict{"url":url,"job":"retrieve/store/analyze {path to store data if store}",
    model:{key=name of data field,val=match patterns}
    """
    def __init__(self,desc):
        self.desc=desc



class Minion(threading.Thread):
    def __init__(self,job_queue,result_q,master):
        self.queue=job_queue
        self.result=result_q
        self.master=master
        threading.Thread.__init__(self)

    def run(self):
        while not self.queue.empty():
            #get next job
            self.job=self.queue.get()
            if self.job["job"].startwith("store"):
                download(self.job["url"],self.job["job"].split(" ")[1])
                self.queue.task_done()
            elif self.job["job"]=="retrieve":
                page=HtmlPage(get(self.job['url']))
                res=page.getFromXPath(self.master.xpaths[self.job['url']])
                self.queue.task_done()
                if res==None:
                    self.queue.put(Job({"url":self.job["url"],"job":"analyze"}))
                    return
                self.result.put(res)
            elif self.job["job"]=="analyze":
                page=get(self.job['url'])
                if re.match(r"(not found)|(doesn't exist)",page):
                    self.queue.task_done()
                    del self.master.xpaths[self.job['url']]
                    return
                page=HtmlPage(page)
                self.master.xpaths[self.job['url']]=page.buildXPath(self.master.classifier)
                self.queue.task_done()
                self.queue.put(Job({"url":self.job["url"],"job":"retrieve"}))


class Crawler:
    def __init__(self):
        self.job_queue=Queue.Queue()
        self.res_queue=Queue.Queue()
        self.xpaths=loadXpath(os.path.dirname(os.path.realpath(__file__))+'\xpath')
        self.classifier=RuleClassifier(loadSModel(os.path.dirname(os.path.realpath(__file__))+'\pattern'))

    """def test(self):
        f=open('e:/testsite/t.html')
        page=HtmlPage(f.read())
        c=RuleClassifier(loadSModel(os.path.dirname(os.path.realpath(__file__))+'\pattern'))
        t=page.buildXPath(c)
        print t
    """
    def saveXpath(self):
        f=open(os.path.dirname(os.path.realpath(__file__))+'\xpath','w')
        for k in self.xpaths:
            f.write(k+','+self.xpaths[k])
        f.close()

    def explore(self):
        self.tpool=[]
        thrs=min(len(self.xpaths)/2,100)
        for k in self.xpaths:
            self.job_queue.put(Job({'job':'analyze','url':k}))
        for i in range(thrs):
            self.tpool.append(Minion(self.job_queue,self.res_queue,self))
        self.job_queue.join()
        self.saveXpath()

    def update(self):
        self.tpool=[]
        thrs=min(len(self.xpaths)/2,100)
        for k in self.xpaths:
            self.job_queue.put(Job({'job':'retrieve','url':k}))
        for i in range(thrs):
            self.tpool.append(Minion(self.job_queue,self.res_queue,self))
        self.job_queue.join()
        while not self.res_queue.empty():
            data=self.res_queue.get()
            for i in range(len(data)):
                store=Store(link=data[i]['link'],price=data[i]['price'])
                store.save()
                try:
                    record=Record.objects.get(title=data[i]['title'])
                    record.cover=data[i]['cover'] if record.cover=='' else record.cover
                    record.stores.add(store)
                    record.save()
                except Record.DoesNotExist:
                    record=Record(title=data[i]['title'],artist=data[i]['artist'],
                              cover=data[i]['cover'],cat_no=data[i]['cat_no'],label=data[i]['label'],
                              genre=data[i]['genre'],time=None,stores=store)
                    record.save()
            self.res_queue.task_done()
        self.saveXpath()

