import matplotlib.pyplot as plt
x=[0,1,1]
y=[1,1,0]

plt.figure(figsize=(8,8))
plt.xlabel("false alarm rate",fontsize=14)
plt.ylabel("hit rate",fontsize=14)

l11,=plt.plot(f_group_ic_9_5_10000_memberud_100_memberdd_100_memberdc_0,
              h_group_ic_9_5_10000_memberud_100_memberdd_100_memberdc_0,
              linewidth=1.0,
              color='red')

plt.legend(handles=[l9,l11,l12,l13],
           labels=["information cascade(9/5),memberdd=0",
                   "information cascade(9/5),memberdd=1",
                   "information cascade(9/9),memberdd=1",
                   "information cascade(9/9),memberdd=1(test)"],
           fontsize=14,
           loc='best')

plt.show()
