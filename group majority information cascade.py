import random,time,datetime,subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as nm
from progressbar import *

#首先建立Group对象，之后执行set_c方法，执行set_member方法
#之后若为simple majority执行act_sm方法,若为information cascade执行act_ic方法


class Group():
    def __init__(self,member,rule,trail):#member,成员数量；rule，达成一致数量;trail，信号辨认次数
        self.member=member
        self.rule=rule
        self.trail=trail
        self.s=0
        self.n=0
        self.hit=0
        self.hit=0
        self.h=[]
        self.f=[]

    def set_c(self,min_c,max_c):#设置c值范围
        self.c=[]
        a=float(min_c)
        max_c=float(max_c)
        while a<=max_c:
            self.c.append(a)
            a+=0.1
        self.total=len(self.c)

    def set_member(self,member_ud,member_dd,member_dc):#生成成员字典
        self.member_ud=member_ud#设置成员di的平均值
        self.member_dd=member_dd#设置成员di的标准差
        self.member_dc=member_dc#设置成员ci的标准差
        self.member_dixi={}#不同c值下的成员字典
        self.member_di=[]#成员的di是不变的
        n=self.member
        while n>0:
            member=GroupMember(member_ud,member_dd,0,0)
            member.set_member()#生成每个成员的di
            self.member_di.append(member.di)
            n-=1
        for c in self.c:
            dixi=[]#所有成员的di和xi
            n=self.member
            while n>0:
                n-=1
                di=self.member_di[n]
                xi=np.random.normal(c,member_dc)+di/2
                m_dixi=[di,xi]#每个成员的di和xi
                dixi.append(m_dixi)
            self.member_dixi[c]=dixi

    def set_input(self):
        self.sig=random.randint(0,1)
        if self.sig==1:
            self.s+=1#信号+1
        elif self.sig==0:
            self.n+=1#噪声+1

    def act_sm(self):#simple majority组反应
        self.group='sm'
        t=0
        #生成进度条
        widgets = ['Progress: ',Percentage(), ' ', Bar('#'),' ', Timer(),
                   ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=10*self.total).start()
        for c in self.c:
            self.hit=0
            self.false=0
            self.s=0
            self.n=0
            n=self.trail
            member=GroupMember(0,0,0,0)
            dixi=self.member_dixi[c]
            while n>0:
                n-=1#一次trail
                self.set_input()#生成一个输入
                i=self.member
                member_hit=0
                member_false=0
                while i>0:
                    i-=1
                    member.di=float(dixi[i][0])
                    member.xi=float(dixi[i][1])
                    member.f_and_h()
                    if self.sig==1:
                        if random.random()<member.h:
                            member_hit+=1
                    elif self.sig==0:
                        if random.random()<member.f:
                            member_false+=1 
                r=self.rule
                if member_hit>=r:
                    self.hit+=1
                elif member_false>=r:
                    self.false+=1
            h=self.hit/self.s
            f=self.false/self.n
            self.h.append(h)
            self.f.append(f)
            #print(t,"/",len(self.c))#显示进度
            pbar.update(10*t+1)
            t+=1
        pbar.finish()
        self.outport_fh()

    def act_ic(self):#information cascade组反应
        self.group='ic'
        t=0#进度值
        widgets = ['Progress: ',Percentage(), ' ', Bar('#'),' ', Timer(),
                   ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=10*self.total).start()
        for c in self.c:
            self.hit=0
            self.false=0
            self.s=0
            self.n=0
            n=self.trail
            member=GroupMember(0,0,0,0)
            dixi=self.member_dixi[c]
            while n>0:
                n-=1#一次trail
                self.set_input()#生成一个输入
                i=self.member
                member_hit=0
                member_false=0
                member_adopt=0
                member_reject=0
                #print(self.sig,"\n")#正式运行需注释
                while i>0:
                    i-=1
                    member.di=float(dixi[i][0])
                    member.xi=float(dixi[i][1])
                    member.f_and_h()
                    group_d=member_adopt-member_reject
                    #print(group_d)#正式运行需注释
                    if self.sig==1:
                        if group_d>1:
                            member_hit+=1
                            member_adopt+=1
                        elif group_d==1:
                            if random.random()<member.h:
                                member_hit+=1
                                member_adopt+=1
                            else:
                                if random.randint(0,1)==1:
                                    member_hit+=1
                                    member_adopt+=1
                                else:
                                    member_reject+=1
                        elif group_d==0:
                            if random.random()<member.h:
                                member_hit+=1
                                member_adopt+=1
                            else:
                                member_reject+=1
                        elif group_d==-1:
                            if random.random()<member.h:
                                if random.randint(0,1)==0:
                                    member_hit+=1
                                    member_adopt+=1
                                else:
                                    member_reject+=1
                            else:
                                member_reject+=1
                        elif group_d<-1:
                            member_reject+=1
                    elif self.sig==0:
                        if group_d>1:
                            member_adopt+=1
                        elif group_d==1:
                            if random.random()<member.c:
                                member_adopt+=1
                            else:
                                if random.randint(0,1)==1:
                                    member_adopt+=1
                                else:
                                    member_false+=1
                                    member_reject+=1
                        elif group_d==0:
                            if random.random()<member.c:
                                member_adopt+=1
                            else:
                                member_false+=1
                                member_reject+=1
                        elif group_d==-1:
                            if random.random()<member.c:
                                if random.randint(0,1)==0:
                                    member_adopt+=1
                                else:
                                    member_false+=1
                                    member_reject+=1
                            else:
                                member_false+=1
                                member_reject+=1
                        elif group_d<-1:
                            member_false+=1
                            member_reject+=1
                r=self.rule
                if member_hit>=r:
                    self.hit+=1
                elif member_false>=r:
                    self.false+=1
            h=self.hit/self.s
            f=self.false/self.n
            self.h.append(h)
            self.f.append(f)
            #print(t,"/",len(self.c))#显示进度
            pbar.update(10*t+1)
            t+=1
        pbar.finish()
        self.outport_fh()

    def outport_fh(self):
        self.member_ud=int(self.member_ud*100)
        self.member_dd=int(self.member_dd*100)
        self.member_dc=int(self.member_dc*100)
        f=str("f_group_"+
              str(self.group)+"_"+
              str(self.member)+"_"+
              str(self.rule)+"_"+
              str(self.trail)+"_memberud_"+
              str(self.member_ud)+"_memberdd_"+
              str(self.member_dd)+"_memberdc_"+
              str(self.member_dc)+"="+
              str(self.f)+"\n")
        h=str("h_group_"+
              str(self.group)+"_"+
              str(self.member)+"_"+
              str(self.rule)+"_"+
              str(self.trail)+"_memberud_"+
              str(self.member_ud)+"_memberdd_"+
              str(self.member_dd)+"_memberdc_"+
              str(self.member_dc)+"="+
              str(self.h)+"\n")
        #print(f)
        #print(h)

        filename=str("group_"+
                str(self.group)+"("+
                str(self.member)+","+
                str(self.rule)+","+
                str(self.trail)+")_memberud_"+
                str(self.member_ud)+"_memberdd_"+
                str(self.member_dd)+"_memberdc_"+
                str(self.member_dc)+".txt")
        with open(filename,'a') as file_object:
            file_object.write(f)
            file_object.write(h)
        
            

            
            






class GroupMember():
    def __init__(self,ud,dd,uc,dc):#成员的属性包括μd，δd，μc，δc
        self.ud=ud
        self.dd=dd
        self.uc=uc
        self.dc=dc
        self.hit=0
        self.false=0
        self.s=0
        self.n=0
        self.xi=0
        self.di=0
        self.ci=0


    def set_member(self):#设置成员的di与ci
        self.di=np.random.normal(self.ud,self.dd)
        self.ci=np.random.normal(self.uc,self.dc)
        self.xi=self.ci+self.di/2#计算λ

    def f_and_h(self):#计算成员的f
        self.f=1-nm(0,1).cdf(self.xi)
        self.h=1-nm(0,1).cdf(self.xi-self.di)
        self.c=1-self.f

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
        h=self.hit/self.s
        f=self.false/self.n
        #print("h="+str(h))
        #print("f="+str(f))
        self.h.append(h)
        self.f.append(f)

    

    def procedure(self):
        self.set_member()
        self.f_and_h()
        n=input("how many trail do you want?")
        n=int(n) 
        while n>0:
            self.set_input()
            self.act()
            n-=1

#主程序
start_time="start time: "+time.strftime("%Y-%m-%d %H:%M:%S")#开始时间
timer_start=datetime.datetime.now()#计时器开始计时

print("Set the group:")
m=input("members:")
r=input("rule:")
t=input("trails:")
print("Choose the kind of the group:")
print("1.simple majority")
print("2.information cascade")
g=input("input a number:")
m=int(m)
r=int(r)
t=int(t)
a=Group(m,r,t)#生成group

print("Set range of c:")
c_min=input("c_min:")
c_max=input("c_max:")
c_min=float(c_min)
c_max=float(c_max)
a.set_c(c_min,c_max)

print("Set group members:")
ud=input("member_ud:")
dd=input("member_dd:")
#uc=input("member_uc:")
dc=input("member_dc:")
ud=float(ud)
dd=float(dd)
#uc=float(member_uc)
dc=float(dc)
a.set_member(ud,dd,dc)

sd=input("Do you want to shut down after end?\nY/N\n").upper()

if g=='1':
    a.act_sm()
    g='simple majority'
elif g=='2':
    a.act_ic()
    g='information cascade'

end_time="end time: "+time.strftime("%Y-%m-%d %H:%M:%S")#结束时间
timer_end=datetime.datetime.now()#计时器结束计时
during=(timer_end-timer_start).seconds
hour=during//3600
minute=(during%3600)//60
second=during-hour*3600-minute*60
during="during time: "+str(hour)+":"+str(minute)+":"+str(second)
filename='record.txt'
information=("GROUP INFORMATION:\n"+
             "group type: "+g+"\n"+
             "group members: "+str(m)+"\n"+
             "group rule: "+str(r)+"\n"+
             "trails: "+str(t)+"\n"+
             "MEMBER INFORMATION:\n"+
             "member ud: "+str(ud)+"\n"+
             "member dd: "+str(dd)+"\n"+
             "member dc: "+str(dc)+"\n")
time_information=("TIME INFORMATION:\n"+
                  start_time+"\n"+
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

        


            
        
