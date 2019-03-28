import matplotlib.pyplot as plt
from scipy.stats import norm as nm
import numpy as np

m=input('member:')
d=input('memberd:')
c=input('memberc:')
d=float(d)
c=float(c)
l=c+d/2


plt.figure(figsize=(12,3))
plt.xlim((-7,7))
plt.ylim((0,0.5))

new_tickes=np.arange(-7,7,0.5)
plt.xticks(new_tickes)
plt.yticks([])

x1=np.arange(-4, 4,0.001)
y1=nm(0,1).pdf(x1)
plt.plot(x1,y1, color='r',linewidth = 2)

x2=np.arange(d-4,d+4,0.001)
y2=nm(d,1).pdf(x2)
plt.plot(x2,y2, color='b',linewidth = 2)

x3=[l,l]
y3=[0,0.5]
plt.plot(x3,y3, color='k',linewidth = 2)

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.savefig(f"{m}-memberd_{d}_memberc_{c}.png",box_inches='tight')

plt.show()
