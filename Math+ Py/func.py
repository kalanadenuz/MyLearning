import matplotlib.pyplot as plt
import numpy as np

# 1️⃣ Define x values, avoiding the vertical asymptote
x = np.linspace(-10, 10, 1000)  # 1000 points from -10 to 10

# To avoid division by zero at x = 2 (vertical asymptote)
x = x[x != 2]

# 2️⃣ Define rational function
f = lambda x: (x**2 - 1)/(x - 2)  # Example: numerator = x^2-1, denominator = x-2

# 3️⃣ Plot function
plt.plot(x, f(x), label="f(x) = (x^2-1)/(x-2)")

# 4️⃣ Add vertical asymptote
plt.axvline(x=2, color='red', linestyle='--', label='Vertical Asymptote x=2')

# 5️⃣ Add horizontal asymptote
# Highest degree numerator = 2, denominator = 1 → no horizontal asymptote in this example
# Let's also plot a function with horizontal asymptote for comparison
g = lambda x: (3*x + 1)/(2*x - 5)
plt.plot(x, g(x), label="g(x) = (3x+1)/(2x-5)")
plt.axhline(y=3/2, color='green', linestyle='--', label='Horizontal Asymptote y=3/2')

# 6️⃣ Show the plot
plt.ylim(-10, 10)  # limit y-axis for better visualization
plt.legend()
plt.grid(True)
plt.show()
