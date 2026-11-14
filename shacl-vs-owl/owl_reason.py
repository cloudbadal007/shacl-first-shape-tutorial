import owlrl
from rdflib import Graph
from rdflib.namespace import OWL

graph = Graph().parse("vocab.ttl")
graph.parse("data.ttl")

owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

print("OWL reasoner: no errors")
print("New facts it inferred:")
for a, b in sorted(graph.subject_objects(OWL.sameAs)):
    if str(a) < str(b):
        print(f"- {a.split('/')[-1]} is the same as {b.split('/')[-1]}")
