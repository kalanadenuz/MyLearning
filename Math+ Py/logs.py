import math
import matplotlib.pyplot as plt

x=math.log10(100)
y=math.log2(8)
z=math.log(100)

print(x)
print(y)
print(z)

# Plotting logarithmic functions
x_values = [1, 10, 100, 1000, 10000]
log10_values = [math.log10(x) for x in x_values]
log2_values = [math.log2(x) for x in x_values]
log_values = [math.log(x) for x in x_values]
plt.plot(x_values, log10_values, label='log10(x)')
plt.plot(x_values, log2_values, label='log2(x)')
plt.plot(x_values, log_values, label='ln(x)')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('x (log scale)')
plt.ylabel('log(x) (log scale)')
plt.title('Logarithmic Functions')
plt.legend()
plt.grid(True)
plt.show()
# Growth simulation
principal = float(input("Enter starting value (principal): "))

