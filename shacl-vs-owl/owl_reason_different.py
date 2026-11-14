import owlrl
from rdflib import Graph, URIRef

ERROR = URIRef("http://www.daml.org/2002/03/agents/agent-ont#error")

graph = Graph().parse("vocab.ttl")
graph.parse("data.ttl")
graph.parse("people.ttl")

owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

errors = list(graph.objects(None, ERROR))
if errors:
    print("OWL reasoner: inconsistent")
    print("alice and a-smith are declared different, but a dataset")
    print("may have only one owner, so they would have to be the same.")
else:
    print("OWL reasoner: no errors")
