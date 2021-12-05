with open('queries.txt') as f:
    lines = f.readlines()

res = ""
for line in lines:
    print(line.split("?")[0])
    res += line.split("?")[0] + "\n"

with open('queries.txt', "w") as f:
    f.write(res)