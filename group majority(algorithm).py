import random,time,datetime,os,csv
import numpy as np
from scipy.stats import norm as norm

class Group():
    def __init__(self,member,rule):#member,成员数量；rule，达成一致数量
        self.member=member
        self.rule=rule
        self.fgroup=0
        self.hgroup=0
        self.l=[]
        self.dp=[]
        self.group_f=[]
        self.group_h=[]
        self.member_f=[]
        self.member_h=[]

    def math_c(self,m,r):
        if r==0:
            c=1
        else:
            n=m
            for i in range(1,r):
                n-=1
                m=m*n
            n=r
            i=r
            for i in range(1,i):
                n-=1
                r=r*n
            c=m/r
            c=int(c)
        return(c)

    def set_member(self,member_ud,member_dd,member_dc):#生成成员字典
        self.member_ud=member_ud#设置成员di的平均值
        self.member_dd=member_dd#设置成员di的标准差
        self.member_dc=member_dc#设置成员ci的标准差

    def set_c(self,min_c,max_c):#设置c值范围
        self.c=[]
        a=float(min_c)
        max_c=float(max_c)
        while a<=max_c:
            if a<0.1 and a>-0.1:
                a=0
            self.c.append(a)
            a+=0.1
        
    def group_fh(self,f,h):#计算group的f和h
        m=self.member
        r=self.rule
        h_group=1
        f_group=1
        for i in range(0,r):
            h_group-=self.math_c(m,i)*(h**i)*((1-h)**(m-i))
            f_group-=self.math_c(m,i)*(f**i)*((1-f)**(m-i))
        self.fgroup=f_group
        self.hgroup=h_group

    def group_ldp(self):
        for c in self.c:
            member=GroupMember(self.member_ud,self.member_dd,c,self.member_dc)
            member.set_member()
            member.f_and_h()
            #if member.f<0.0001:
                #member.f=0
            #elif member.f>0.9999:
                #member.f=1
            #if member.h<0.0001:
                #member.h=0
            #elif member.h>0.9999:
                #member.h=1
            self.group_fh(member.f,member.h)
            if self.fgroup==0 or self.fgroup==1 or self.hgroup==0 or self.hgroup==1:
                group_dp='-'
                group_l='-'
            elif self.fgroup!=0 and self.hgroup!=0 and self.fgroup!=1 and self.hgroup!=1:
                group_l=-norm.ppf(self.fgroup)#计算lambda
                group_dp=norm.ppf(self.hgroup)-norm.ppf(self.fgroup)#计算d'
            self.member_f.append(member.f)
            self.member_h.append(member.h)
            self.l.append(group_l)
            self.dp.append(group_dp)
            self.group_f.append(self.fgroup)
            self.group_h.append(self.hgroup)

    def outport_data(self):
        self.member_ud=int(self.member_ud*100)
        self.member_dd=int(self.member_dd*100)
        self.member_dc=int(self.member_dc*100)
        filename_c=str("group_sm_"+"("+
                   str(self.member)+","+
                   str(self.rule)+")_memberud_"+
                   str(self.member_ud)+"_memberdd_"+
                   str(self.member_dd)+"_memberdc_"+
                   str(self.member_dc)+".csv")
        num=len(self.c)
        with open(filename_c,"w",newline="") as datacsv:
            csvwriter = csv.writer(datacsv,dialect = ("excel"))
            csvwriter.writerow(["c","member false alarm rate","member hit rate",
                                "group false alarm rate","group hit rate","d'","l"])
            for i in range(0,num):
                csvwriter.writerow([self.c[i],self.member_f[i],self.member_h[i],
                                    self.group_f[i],self.group_h[i],self.dp[i],self.l[i]])


 
class GroupMember():
    def __init__(self,ud,dd,uc,dc):#成员的属性包括μd，δd，μc，δc
        self.ud=ud
        self.dd=dd
        self.uc=uc
        self.dc=dc

    def set_member(self):#设置成员的di与ci
        self.di=np.random.normal(self.ud,self.dd)
        self.ci=np.random.normal(self.uc,self.dc)
        self.xi=self.ci+self.di/2#计算λ

    def f_and_h(self):#计算成员的f和h
        self.f=1-norm(0,1).cdf(self.xi)
        self.h=1-norm(0,1).cdf(self.xi-self.di)

#主程序
print("Set the group:")
m=input("members:")
r=input("rule:")
m=int(m)
r=int(r)
a=Group(m,r)#生成group

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

#设置c值范围
print("Set range of c:")
c_min=input("c_min:")
c_max=input("c_max:")
c_min=float(c_min)
c_max=float(c_max)
a.set_c(c_min,c_max)

a.group_ldp()
a.outport_data()






