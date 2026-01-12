import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,5,400)
y = x**2

# two points
x1, x2 = 1, 3
y1, y2 = x1**2, x2**2

# secant line
m = (y2 - y1)/(x2 - x1)
secant_y = m*(x - x1) + y1

plt.plot(x,y,label="y = x^2")
plt.plot(x,secant_y,'r--',label="Secant line")
plt.scatter([x1,x2],[y1,y2])
plt.grid(True)
plt.legend()
plt.show()
