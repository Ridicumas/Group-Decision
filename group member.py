import random,time,datetime,subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as nm
from progressbar import *



"""
class Group():
    def __init__(self,member):#member：成员数量
        self.member=member

    def majority_rule(self):
"""





class GroupMember():
    def __init__(self,ud,dd,uc,dc,trail):#成员的属性包括μd，δd，μc，δc
        self.ud=ud
        self.dd=dd
        self.uc=uc
        self.dc=dc
        self.trail=trail
        self.hit=0
        self.false=0
        self.s=0
        self.n=0
        self.h_rate=0
        self.f_rate=0
        


    def set_member(self):#计算成员的di与ci
        self.di=np.random.normal(self.ud,self.dd)
        self.ci=np.random.normal(self.uc,self.dc)
        self.xi=self.ci+self.di/2#计算λ

    def f_and_h(self):#计算成员的f和h
        self.f=1-nm(0,1).cdf(self.xi)
        self.h=1-nm(0,1).cdf(self.xi-self.di)

    def set_input(self):#设置输入
        self.sig=random.randint(0,1)
        if self.sig==1:
            self.s+=1#信号+1
        elif self.sig==0:
            self.n+=1#噪声+1

    def act(self):#模拟成员的接受或拒绝
        if self.sig==1:
            if random.random()<self.h:
                self.hit+=1
        elif self.sig==0:
            if random.random()<self.f:
                self.false+=1

    def cacul_hf(self):#测试计算正确性
        self.h_rate=self.hit/self.s
        self.f_rate=self.false/self.n
        #print("h="+str(self.h_rate))
        #print("f="+str(self.f_rate))
        
    def procedure(self):
        self.set_member()
        self.f_and_h()
        n=self.trail#抽样数
        while n>0:
            self.set_input()
            self.act()
            n-=1
        self.cacul_hf()

#主程序
start_time="Start time: "+time.strftime("%Y-%m-%d %H:%M:%S")#开始时间
timer_start=datetime.datetime.now()#计时器开始计时

print("Set your members:")
ud=input("member_ud:")
dd=input("member_dd:")
#uc=input("member_uc:")
dc=input("member_dc:")
ud=float(ud)
dd=float(dd)
#uc=float(member_uc)
dc=float(dc)

print("Set range of c:")
c_min=input("c_min:")
c_max=input("c_max:")
c_min=float(c_min)
c_max=float(c_max)

print("How many trails are there?")
t=input()
t=int(t)

sd=input("Do you want to shut down after end?\nY/N\n").upper()

c=[]
h=[]
f=[]
c_num=c_min
while c_num<=c_max:
    c.append(c_num)
    c_num+=0.1

i=0
total=len(c)
widgets = ['Progress: ',Percentage(), ' ', Bar('#'),' ', Timer(),
           ' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=10*total).start()
for ci in c:
    a=GroupMember(ud,dd,ci,dc,t)
    a.procedure()
    h.append(a.h_rate)
    f.append(a.f_rate)
    #print(i,"/",len(c))
    pbar.update(10 * i + 1)
    i+=1
pbar.finish()
    
ud=ud*100
dd=dd*100
#uc=uc*100
dc=dc*100
ud=int(ud)
dd=int(dd)
#uc=int(uc)
dc=int(dc)
out_f=str("f_ind_ud_"+str(ud)+
          "_dd_"+str(dd)+
#          "_uc_"+str(uc)+
          "_dc_"+str(dc)+
          "_"+str(a.trail)+"="+
          str(f)+"\n")
out_h=str("h_ind_ud_"+str(ud)+
          "_dd_"+str(dd)+
#          "_uc_"+str(uc)+
          "_dc_"+str(dc)+
          "_"+str(a.trail)+"="+
          str(h)+"\n")
#print(out_f)
#print(out_h)

filename=str("individual("+
             "ud_"+str(ud)+
             "_dd_"+str(dd)+
#             "_uc_"+str(uc)+
             "_dc_"+str(dc)+
             "_"+str(a.trail)+
             ").txt")
with open(filename,'a') as file_object:
    file_object.write(out_f)
    file_object.write(out_h)

end_time="End time: "+time.strftime("%Y-%m-%d %H:%M:%S")#结束时间
timer_end=datetime.datetime.now()#计时器结束计时
during=(timer_end-timer_start).seconds
hour=during//3600
minute=(during%3600)//60
second=during-hour*3600-minute*60
during="During time: "+str(hour)+":"+str(minute)+":"+str(second)
filename='record.txt'
information=("Individual ud: "+str(ud)+
             "\n"+"Individual dd: "+str(dd)+
             "\n"+"Individual dc: "+str(dc)+
             "\n"+"Trails: "+str(t)+
             "\n")
time_information=(start_time+"\n"+
                  end_time+"\n"+
                  during+"\n\n")
with open(filename,'a') as file_object:#输出时间记录
    file_object.write(information)
    file_object.write(time_information)

if sd=='Y':
    print("The computer will shut down in 5 seconds.")
    for s in range(5):
        print(5-s)
        time.sleep(1)
    subprocess.call("shutdown /p")





            
        
