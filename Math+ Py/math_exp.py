# Growth simulation
principal = float(input("Enter starting value (principal): "))
rate = float(input("Enter growth rate per step (like 0.05 for 5%): "))
steps = int(input("Enter number of steps: "))

# Using exponent
final_value = principal * ((1 + rate) ** steps)
print(f"Final value after growth: {final_value}")

# Compare integer division effect
int_growth = int(principal)
for _ in range(steps):
    int_growth = int_growth + int(int_growth * rate)
print(f"Approximate integer growth: {int_growth}")
