import json
import matplotlib.pyplot as plt

#绘制框架
plt.figure(figsize=(8,8))
plt.xlim((0,1))
plt.ylim((0,1))
plt.xlabel("false alarm rate",fontsize=14)
plt.ylabel("hit rate",fontsize=14)
x=[0,1]
y=[0,1]
plt.plot(x,y,linewidth=1,color='black',linestyle='--')

#输入需绘制的individual曲线
file_name=[]
curve_name=[]
f=[]
h=[]
figure_name=""
a=input("Do you want to plot individual performance?Y/N\n")
if a.upper()=='Y':
    n=input("How many individuals do you want to plot?\n")
    n=int(n)
    figure_name+="ind"
    for i in range(1,n+1):
        print(f"INDIVIDUAL{i}:")
        ud=input("ud:")
        dd=input("dd:")
        dc=input("dc:")
        curve_name_i=f"individual({ud},{dd},{dc})"
        ud=int(float(ud)*100)
        dd=int(float(dd)*100)
        dc=int(float(dc)*100)
        t=input("trail:")
        file_name_i=f"individual(ud_{ud}_dd_{dd}_dc_{dc}_{t}).json"
        file_name.append(file_name_i)
        curve_name.append(curve_name_i)
        figure_name+=f"_({ud},{dd},{dc})"
        
#输入需绘制的group曲线
a=input("Do you want to plot group performance?Y/N\n")
if a.upper()=='Y':
    n=input("How many groups do you want to plot?\n")
    n=int(n)
    figure_name+="group"
    for i in range(1,n+1):
        print(f"GROUP{i}:")
        c_num=input("group class(1.simple majority,2.information cascade):")
        if c_num=='1':
            c='sm'
        elif c_num=='2':
            c='ic'
        m=input("member:")
        r=input("rule:")
        ud=input("member ud:")
        dd=input("member dd:")
        dc=input("member dc:")
        t=input("trail:")
        curve_name_i=f"group_{c}({m},{r},{t})_member({ud},{dd},{dc})"
        ud=int(float(ud)*100)
        dd=int(float(dd)*100)
        dc=int(float(dc)*100)
        file_name_i=f"group_{c}({m},{r},{t})_memberud_{ud}_memberdd_{dd}_memberdc_{dc}.json"
        file_name.append(file_name_i)
        curve_name.append(curve_name_i)
        figure_name+=f"_{c}({m},{r}_{ud},{dd},{dc})"
figure_name+=".png"

#绘制曲线
n=len(file_name)
curve_color=['blue','red','yellow','green','pink','black']
l=[]
for i in range(0,n):
    with open(file_name[i]) as file_object:
        f_h=json.load(file_object)
        f=f_h[0]
        h=f_h[1]
    i,=plt.plot(f,h,
                linewidth=1.0,
                color=curve_color[i])
    l.append(i)
plt.legend(handles=l,
           labels=curve_name,
           fontsize=14,
           loc='best')
plt.savefig(figure_name,box_inches='tight')
plt.show()
