import query_builder as qb
import question_to_query as q2q

query = q2q.skill("Does Professor Khosmood teach next quarter?")
print(query)
qb.generate_response(query[0], query[1], query[2])

query = q2q.skill("Is csc 482 offered next quarter?")
print(query)
qb.generate_response(query[0], query[1], query[2])

query = q2q.skill("Is csc 482 offered next quarter?")
print(query)
qb.generate_response(query[0], query[1], query[2])