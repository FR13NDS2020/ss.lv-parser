dicto = {}
new = []
for i in range(10):
    new = {}
    for k in range(5):
        new[k] = i

    dicto[i] = new

print(dicto[1])