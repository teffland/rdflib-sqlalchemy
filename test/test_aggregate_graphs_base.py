# import unittest, logging
# from rdflib import Literal
# from rdflib import plugin
# from rdflib import RDF
# from rdflib import RDFS
# from rdflib import URIRef
# from rdflib.store import Store
# from cStringIO import StringIO
# from rdflib.graph import Graph
# from rdflib.graph import ConjunctiveGraph
# from rdflib.graph import ReadOnlyGraphAggregate

# logging.basicConfig(level=logging.ERROR,format="%(message)s")
# _logger = logging.getLogger(__name__)
# _logger.setLevel(logging.DEBUG)

# testGraph1N3="""
# @prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
# @prefix : <http://test/> .
# :foo a rdfs:Class.
# :bar :d :c.
# :a :d :c.
# """

# testGraph2N3="""
# @prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
# @prefix : <http://test/> .
# @prefix log: <http://www.w3.org/2000/10/swap/log#>.
# :foo a rdfs:Resource.
# :bar rdfs:isDefinedBy [ a log:Formula ].
# :a :d :e.
# """

# testGraph3N3="""
# @prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
# @prefix log: <http://www.w3.org/2000/10/swap/log#>.
# @prefix : <http://test/> .
# <> a log:N3Document.
# """

# sparqlQ = \
# """
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# SELECT *
# FROM NAMED <http://example.com/graph1>
# FROM NAMED <http://example.com/graph2>
# FROM NAMED <http://example.com/graph3>
# FROM <http://www.w3.org/2000/01/rdf-schema#>

# WHERE {?sub ?pred rdfs:Class }"""

# sparqlQ2 =\
# """
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# SELECT ?class
# WHERE { GRAPH ?graph { ?member a ?class } }"""

# sparqlQ3 =\
# """
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX log: <http://www.w3.org/2000/10/swap/log#>
# SELECT ?n3Doc
# WHERE {?n3Doc a log:N3Document }"""

# # sqlalchemy_url = Literal('postgresql+psycopg2://gjh@localhost/test')
# sqlalchemy_url = Literal("mysql://gjh:50uthf0rk@localhost:3306/test")
# sqlalchemy_url = Literal("postgresql+psycopg2://gjh:50uthf0rk@localhost/test")

# class GraphAggregates1(unittest.TestCase):

#     def setUp(self):
#         memStore = plugin.get('SQLAlchemyBase', Store)(
#             identifier="rdflib_test", configuration=sqlalchemy_url)
#         self.graph1 = Graph(memStore)
#         self.graph2 = Graph(memStore)
#         self.graph3 = Graph(memStore)

#         for n3Str, graph in [(testGraph1N3, self.graph1),
#                              (testGraph2N3, self.graph2),
#                              (testGraph3N3, self.graph3)]:
#             graph.parse(StringIO(n3Str), format='n3')
#             _logger.debug("Graph... %s" % graph.serialize(format="nt"))

#         self.G = ReadOnlyGraphAggregate([self.graph1, self.graph2, self.graph3])

#     def testAggregateRaw(self):
#         #Test triples
#         assert len(list(self.G.triples((None, RDF.type, None)))) == 4,
#              len(list(self.G.triples((None, RDF.type, None))))
#         assert len(list(self.G.triples((URIRef("http://test/bar"), None, None)))) == 2
#         assert len(list(self.G.triples((None, URIRef("http://test/d"), None))))   == 3

#         #Test __len__
#         assert len(self.G) == 8, self.G.serialize(format="nt")

#         #assert context iteration
#         for g in self.G.contexts():
#             assert isinstance(g, Graph)

#         #Test __contains__
#         assert (URIRef("http://test/foo"), RDF.type, RDFS.Resource) in self.G

#         barPredicates = [URIRef("http://test/d"), RDFS.isDefinedBy]
#         assert len(list(self.G.triples_choices((URIRef("http://test/bar"), barPredicates, None)))) == 2

# class GraphAggregates2(unittest.TestCase):
#     def setUp(self):
#         memStore = plugin.get('SQLAlchemyBase', Store)(
#             identifier="rdflib_test", configuration=sqlalchemy_url)
#         self.graph1 = Graph(memStore, URIRef("http://example.com/graph1"))
#         self.graph2 = Graph(memStore, URIRef("http://example.com/graph2"))
#         self.graph3 = Graph(memStore, URIRef("http://example.com/graph3"))

#         for n3Str,graph in [(testGraph1N3, self.graph1),
#                             (testGraph2N3, self.graph2),
#                             (testGraph3N3, self.graph3)]:
#             graph.parse(StringIO(n3Str), format='n3')

#         self.graph4 = Graph(memStore, RDFS.uri)
#         self.graph4.parse(RDFS.uri)
#         self.G = ConjunctiveGraph(memStore)

#     def testAggregateSPARQL(self):
#         rt =  self.G.query(sparqlQ)
#         assert len(rt) > 1
#         rt = self.G.query(sparqlQ2, initBindings={u'?graph' : URIRef(u"http://example.com/graph3")})
#         try:
#             import json
#         except ImportError:
#             import simplejson as json
#         res = json.loads(rt.serialize(format='json'))
#         assert len(res['results']['bindings']) == 20, len(res['results']['bindings'])

# class GraphAggregates3(unittest.TestCase):
#     def setUp(self):
#         memStore = plugin.get('SQLAlchemyBase', Store)(
#             identifier="rdflib_test", configuration=sqlalchemy_url)
#         self.graph1 = Graph(memStore,URIRef("graph1"))
#         self.graph2 = Graph(memStore,URIRef("graph2"))
#         self.graph3 = Graph(memStore,URIRef("graph3"))

#         for n3Str, graph in [(testGraph1N3,self.graph1),
#                             (testGraph2N3,self.graph2),
#                             (testGraph3N3,self.graph3)]:
#             graph.parse(StringIO(n3Str),format='n3')
#         self.G = ConjunctiveGraph(memStore)

#     def testDefaultGraph(self):
#         #test that CG includes triples from all 3
#         assert self.G.query(sparqlQ3), "CG as default graph should *all* triples"
#         assert not self.graph2.query(sparqlQ3),
#             "Graph as default graph should *not* include triples from other graphs"

# if __name__ == '__main__':
#     unittest.main()
