# Take input from the user
n = int(input("Enter the value of n: "))

# Check if n is within the specified constraints
if 1 <= n <= 100:
    # Use a loop to print "Hello world" n times
    for i in range(n):
        print("Hello world")
else:
    print("The value of n should be between 1 and 100, inclusive.")