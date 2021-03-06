import random,time,datetime,subprocess,json,os,csv
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
        self.cl=[]
        self.dp=[]
        self.ic_d=[]
        self.ic=[]
        self.g_d=[]
        self.m_d=[]
        self.cascade_number=[]

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
        self.member_ci=[]#成员的ci是不变的
        self.member_di=[]#成员的di是不变的
        self.member_dixi={}#不同c值下的成员字典
        n=self.member
        while n>0:
            #生成每个成员的di,ci
            n-=1
            di=member_ud+member_dd*(1-2*n/(self.member-1))
            ci=member_dc*(1-2*n/(self.member-1))
            self.member_di.append(di)
            self.member_ci.append(ci)
        for c in self.c:
            dixi=[]#所有成员的di和xi
            n=self.member
            while n>0:
                n-=1
                di=self.member_di[n]
                xi=self.member_ci[n]+c+di/2
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
            l=-nm.ppf(f)
            dp=nm.ppf(h)-nm.ppf(f)
            #计算对应的d'以及lambda
            if f==0 or f==1 or h==0 or h==1:
                dp='-'
                l='-'
            elif f!=0 and h!=0 and f!=1 and h!=1:
                l=-nm.ppf(f)
                dp=nm.ppf(h)-nm.ppf(f)
            self.dp.append(dp)
            self.cl.append(l)
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
            ic_number=0
            g_d=0
            m_d=0
            ic=[]
            ic_d=[]
            cascade_number=0
            #member=GroupMember(0,0,0,0)
            while n>0:
                n-=1#一次trail
                self.set_input()#生成一个输入
                i=self.member
                member_hit=0
                member_false=0
                member_adopt=0
                member_reject=0
                go=0
                ic_member=0
                #print(self.sig,"\n")#正式运行需注释
                while i>0:#每一个成员的操作
                    i-=1
                    member=GroupMember(self.member_ud,self.member_dd,c,self.member_dc)
                    member.set_member()
                    member.f_and_h()
                    group_d=member_adopt-member_reject
                    groupd=[]
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
                    groupd.append(group_d)
                    if group_d>1 and go==0:
                        go=1
                        ic_member=self.member-i
                        cascade_number+=1
                g_d+=group_d
                m_d+=ic_member
                ic.append(ic_member)#本次trail中information cascade发生的时机   
                ic_d.append(groupd)#本次trail的所有d（information cascade标准）
                r=self.rule
                if member_hit>=r:
                    self.hit+=1
                elif member_false>=r:
                    self.false+=1
            g_d=g_d/cascade_number
            m_d=m_d/cascade_number
            self.cascade_number.append(cascade_number)
            self.g_d.append(g_d)
            self.m_d.append(m_d)
            self.ic.append(ic)#所有information cascade发生的时机（二维数组）
            self.ic_d.append(ic_d)#所有d（三维数组）
            h=self.hit/self.s
            f=self.false/self.n
            l=-nm.ppf(f)
            dp=nm.ppf(h)-nm.ppf(f)
            #计算对应的d'以及lambda
            if f==0 or f==1 or h==0 or h==1:
                dp='-'
                l='-'
            elif f!=0 and h!=0 and f!=1 and h!=1:
                l=-nm.ppf(f)
                dp=nm.ppf(h)-nm.ppf(f)
            self.h.append(h)
            self.f.append(f)
            self.dp.append(dp)
            self.cl.append(l)
            #print(t,"/",len(self.c))#显示进度
            pbar.update(10*t+1)
            t+=1
        pbar.finish()
        self.outport_fh()

    def calcu_ic(self):#处理information cascade的各个特征
        n=len(self.ic_d[0])
        m=len(self.ic_d)
        
        

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
        filename_j=str("group_"+
                   str(self.group)+"("+
                   str(self.member)+","+
                   str(self.rule)+","+
                   str(self.trail)+")_memberud_"+
                   str(self.member_ud)+"_memberdd_"+
                   str(self.member_dd)+"_memberdc_"+
                   str(self.member_dc)+".json")
        filename_jdp=str("group_"+
                     str(self.group)+"(d')_("+
                     str(self.member)+","+
                     str(self.rule)+","+
                     str(self.trail)+")_memberud_"+
                     str(self.member_ud)+"_memberdd_"+
                     str(self.member_dd)+"_memberdc_"+
                     str(self.member_dc)+".json")
        filename_c=str("group_"+
                   str(self.group)+"("+
                   str(self.member)+","+
                   str(self.rule)+","+
                   str(self.trail)+")_memberud_"+
                   str(self.member_ud)+"_memberdd_"+
                   str(self.member_dd)+"_memberdc_"+
                   str(self.member_dc)+".csv")
        filename_cdp=str("group_"+
                     str(self.group)+"(preprocessed)_("+
                     str(self.member)+","+
                     str(self.rule)+","+
                     str(self.trail)+")_memberud_"+
                     str(self.member_ud)+"_memberdd_"+
                     str(self.member_dd)+"_memberdc_"+
                     str(self.member_dc)+".csv")
        filename_cmember=str("member_of_group_"+
                         str(self.group)+"_("+
                         str(self.member)+","+
                         str(self.rule)+","+
                         str(self.trail)+")_memberud_"+
                         str(self.member_ud)+"_memberdd_"+
                         str(self.member_dd)+"_memberdc_"+
                         str(self.member_dc)+".csv")
        with open(filename,'w') as file_object:
            file_object.write(f)
            file_object.write(h)
        with open(filename_j,'w') as f_obj:
            json.dump([self.f,self.h],f_obj)
        num=len(self.f)
        with open(filename_c,"w",newline="") as datacsv:
            csvwriter = csv.writer(datacsv,dialect = ("excel"))
            if self.group=='sm':
                csvwriter.writerow(["c","false alarm rate","hit rate","d'","l"])
                for i in range(0,num):
                    csvwriter.writerow([self.c[i],self.f[i],self.h[i],self.dp[i],self.cl[i]])
            elif self.group=='ic':
                csvwriter.writerow(["c","false alarm rate","hit rate","d'","l",
                                    "d(mean)","cascade time","cascade number","trail",
                                    "P(cascade)"])
                for i in range(0,num):
                    csvwriter.writerow([self.c[i],self.f[i],self.h[i],self.dp[i],self.cl[i],
                                        self.g_d[i],self.m_d[i],self.cascade_number[i],
                                        self.trail,self.cascade_number[i]/self.trail])
        c=[]
        dp=[]
        with open(filename_cdp,"w",newline="") as datacsv:
            csvwriter = csv.writer(datacsv,dialect = ("excel"))
            if self.group=='sm':
                csvwriter.writerow(["c","false alarm rate","hit rate","d'","l"])
                for i in range(0,num):
                    if self.dp[i]!='-':
                        if self.dp[i]>0.00001:
                           csvwriter.writerow([self.c[i],self.f[i],self.h[i],self.dp[i],self.cl[i]])
                           c.append(self.c[i])
                           dp.append(self.dp[i])
            elif self.group=='ic':
                csvwriter.writerow(["c","false alarm rate","hit rate","d'","l",
                                    "d(mean)","cascade time","cascade number","trail",
                                    "P(cascade)"])
                for i in range(0,num):
                    if self.dp[i]!='-':
                        if self.dp[i]>0.00001:
                            csvwriter.writerow([self.c[i],self.f[i],self.h[i],self.dp[i],self.cl[i],
                                                self.g_d[i],self.m_d[i],self.cascade_number[i],
                                                self.trail,self.cascade_number[i]/self.trail])
                            c.append(self.c[i])
                            dp.append(self.dp[i])
        with open(filename_jdp,'w') as f_obj:
            json.dump([c,dp],f_obj)
        with open(filename_cmember,"w",newline="") as datacsv:
            csvwriter = csv.writer(datacsv,dialect = ("excel"))
            csvwriter.writerow(["member","d'","c_tendency"])
            for i in range(0,self.member):
                csvwriter.writerow([i+1,self.member_di[i],self.member_ci[i]])
            
           


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

        


            
        
