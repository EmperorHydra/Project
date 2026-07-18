x = "Awesome"

def myfunc():
    print("Python is " + x)

myfunc()


def myfunc():
    x = "Fantastic"
    print("Python is " + x)

myfunc()

def myfunc():
    global x
    x = "Fantastic"
    print("Python is " + x)

myfunc()

print("Python is " + x)

