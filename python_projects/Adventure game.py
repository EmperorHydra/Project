print ("WELCOME HERO")

Name=input("Enter your name:")
print("Welcome to the vampire republic"+" " + Name)

Direction_input = input("Do you wish to go left or right?")

if Direction_input == "left":
    print("Welcome to the town square")
elif Direction_input == "right":
    print("Welcome to the castle")
else:
    Direction_input = input("Do you wish to go left or right?")

if Direction_input == "left":
    print("GOBLIN ENEMY ENCOUNTERED")
else:
    print ("SKELETON ENEMY ENCOUNTERD")

control_input = input("Attack or Defend or Flee?")

if control_input == "Attack":
    print("Enemy takes 10 damage,Enemy has been defeated.\n Game Is Won!")
elif control_input == "Defend":
    print("Enemy attacks for 10 damage, player is defeated.Game Over!")
else:
    print("Enemy attacks for 10 damage as you flee, player is defeated. Game Over!")