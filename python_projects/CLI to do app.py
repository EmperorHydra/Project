print("To Do App")

print("Do you wish to add a task?")
option = input("if yes input y, if no input n:")
if option == "y":
    input_task_1 = input("Input Task 1: ")
    print(input_task_1)
    input_task_2 = input("Input Task 2: ")
    print(input_task_2)
    print("This is your to do list:")
    print(input_task_1)
    print(input_task_2)
else:
    print("Thank you,this is your to do list for the day,it is currently empty please restart to fill")


