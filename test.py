filename = str(input('Nama file: '))

with open(filename, 'r') as file:
    data = file.read().splitlines()

print(data)