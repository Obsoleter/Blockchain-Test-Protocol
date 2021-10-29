command = input("Enter x y z: ")

print(f"Len: {len(command.split(' '))}")

for command in command.split(' '):
    print(command)