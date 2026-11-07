from pyshacl import validate
from rdflib import Graph
from rdflib.namespace import SH

data = Graph().parse("data.ttl")
shapes = Graph().parse("shapes.ttl")
vocab = Graph().parse("vocab.ttl")

conforms, report, _ = validate(data, shacl_graph=shapes, ont_graph=vocab)

print("Conforms:", conforms)
problems = []
for result in report.subjects(SH.resultMessage, None):
    node = report.value(result, SH.focusNode).split("/")[-1]
    message = report.value(result, SH.resultMessage)
    problems.append(f"- {node}: {message}")
print("\n".join(sorted(problems)))
