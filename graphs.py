import matplotlib.pyplot as plt

x = [1, 2, 4, 8, 16, 32]
y = [0.489533011,
     0.646272965,
     0.838754647,
     0.932184242,
     0.948907508,
     0.949344203,
     ]

plt.plot(x, y, color='green', linestyle='dashed', linewidth=3,
         marker='o', markerfacecolor='blue', markersize=12)
plt.xlabel('Cache size(Kb)')
plt.ylabel('IPC')

plt.title('Fixed way associative = 4 and cache line size = 64')
plt.show()
