import query_builder as qb
import question_to_query as q2q

# query = q2q.skill("Does Professor Khosmood teach next quarter?")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("Is csc 482 offered next quarter?")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("Is csc 482 offered this quarter?")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("random stuff")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("What format is cpe 442 offered in")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# # res = qb.generate_response("df_sched", {'Course': 'cpe 442', 'Quarter': 'F'}, ["Format"])
# # print(res)

# # res = qb.generate_response("df_sched", {'Course': 'cpe 428', 'Quarter': 'F'}, ["Format", "Instructor"])
# # print(res)

# query = q2q.skill("What classes are offered in the fall")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("What format is CSC 378 going to be in the Winter")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("What is the class description for CSC 308")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("What room is CPE 442 taught in?")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("Is CPE 315 taught by Professor Seng")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("when is ime 200")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("when is csc 482")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("is ime 200 offered next quarter")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("who teaches mate 450 this quarter")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("what is the enrollment capacity for cpe 202")
# print(query)
# res = qb.generate_response(query[0], query[1], query[2])
# print(res)

# query = q2q.skill("when is thesis")
# print(query)
# res = qb.generate_response("df_sched", {"Description": "senior project i"}, [])
# print(res)


# query = q2q.skill("is cpe 315 taught by professor seng")
# print(query)
# res = qb.generate_response(query[0], {'Course': 'cpe 315', "Quarter": "F"}, query[2])
# print(res)

with open('queries.txt') as f:
    lines = f.readlines()

i = 1
for line in lines:
    print("question: " + str(i))
    i += 1
    query = q2q.skill(line.lower())
    print(query)
    if query != None:
        res = qb.generate_response(query[0], query[1], query[2])
        print(res + "\n")


query = q2q.skill("How many sections of cpe 101 is dr siu teaching")
print(query)
res = qb.generate_response(query[0], query[1], query[2])
print(res)