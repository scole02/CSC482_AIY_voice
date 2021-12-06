# with open('queries.txt') as f:
#     lines = f.readlines()

# res = ""
# for line in lines:
#     print(line.split("?")[0])
#     res += line.split("?")[0] + "\n"

# with open('queries.txt', "w") as f:
#     f.write(res)

with open('conversions.txt') as f:
    lines = f.readlines()

conversions = []
for line in lines:
    input = line[2:-3].split("', '")
    print(line)
    print(input)
    conversions.append(input)
    # res += line.split("?")[0] + "\n"

print(conversions)
# with open('queries.txt', "w") as f:
#     f.write(res)