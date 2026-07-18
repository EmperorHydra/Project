def my_function():
    print("Hello from a function")
my_function()

#without function
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)

#with function

def farenheit_to_celsius(farenheit):
    return (farenheit - 32) * 5 / 9
print(farenheit_to_celsius(77))
print(farenheit_to_celsius(95))
print(farenheit_to_celsius(50))

def get_greeting():
    return ("Hello from a function")

message = get_greeting()
print(message)
