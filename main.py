import random

def createPairs(lst):
	pairs = []
	for i in range(len(lst) - 1):
		pairs.append([lst[i], lst[i+1]])
	return pairs

def removeDupes(lst):
				i = 0
				while i < len(lst):
					j = i + 1
					while j < len(lst):
						if lst[i][0] == lst[j][0] and lst[i][1] == lst[j][1]:
							lst.remove(lst[j])
						else:
							j += 1
					i += 1

class Graph:
	def __init__(self, vertices):
		"""Initialisation"""
		self.V = vertices # nb of vertices
		self.graph = []

	def addEdge(self, u, v, w):
		"""Ajout d'une arete uv de poids w"""
		self.graph.append([u, v, w])
  
	def getEdgeWeight(self, u, v):
		"""Renvoie le poids associé à l'arete uv"""
		for edge in self.graph:
			if edge[0] == u and edge[1] == v:
				return edge[2]
		return None

	def printArr(self, dist):
		"""Affichage de la solution"""
		print("Arete\t\tDist. depuis source")
		for i in range(self.V):
			print("{0}\t\t{1}".format(i, dist[i]))

	def hasNegativeCycle(self):
		"""Verifie la presence de circuit negatif dans le graphe"""
		dist = [float("Inf")] * self.V
		dist[0] = 0
		for _ in range(self.V - 1):
			# Verifie si les distances sont mise a jour
			for u, v, w in self.graph:
				if dist[u] != float("Inf") and dist[u] + w < dist[v]:
					dist[v] = dist[u] + w
		# Verifie la presence de circuit negatif
		for u, v, w in self.graph:
			if dist[u] != float("Inf") and dist[u] + w < dist[v]:
				return True
		return False

	def generateRandWeight(self):
		"""Génère des poids aléatoires dans l'intervalle [-10, 10] pour toutes les arêtes"""
		for edge in self.graph:
			edge[2] = random.randint(-10, 10)
		while self.hasNegativeCycle():
			for edge in self.graph:
				edge[2] = random.randint(-10, 10)
    
	def setSource(self):
		"""Renvoie le premier sommet qui atteint au moimns la moitié des sommets du graph"""
		num_vertices = self.V  # Nombre de sommets du graphe
		threshold = num_vertices // 2  # Seuil pour atteindre la moitié des sommets 
		v = []	# liste pour stocker tous les sommets candidats 
		for vertex in range(num_vertices):
			count = 0  # Compteur pour le nombre de sommets atteints
			for edge in self.graph:
				if edge[0] == vertex:
					count += 1
			if count >= threshold:
				v.append((vertex, count))
		if v:
			res = max(v, key=lambda x: x[1])[0]	# on selectionne le sommet avec le plus d'aretes sortantes parmi celles au dessus du threshold
			return res
		else:
			print("Erreur: aucun sommet n'atteint la moitié des sommets du graphe")
			return None

	def graphArborescence(self, s):
		t= []
		G = Graph(self.V)
		for e in s:
			t.append(createPairs(e))
		t = [pair for sublist in t for pair in sublist if sublist]	# on desimbrique les listes
		t = list(set(map(tuple, t)))	# on garde une seule occurence de chaque element
		for v in t:
			G.addEdge(v[0],v[1], self.getEdgeWeight(v[0],v[1]))
		return G

	def BellmanFord(self, src):
		"""Application de l'algo de BellmanFord : renvoie les distances depuis la source + nb d'itérations + arborescence des plus courts chemins"""
		# Initialisation des distances depuis la source aux autres sommets à l'infini
		dist = [float("Inf")] * self.V
		dist[src] = 0

		# Initialisation des prédécesseurs
		predecessors = {}

		# Relaxation des arêtes au plus |V| - 1 fois
		iterations = 0  # Compteur d'itérations
		for _ in range(self.V - 1):
			is_updated = False  # Flag pour vérifier si une distance a été mise à jour dans l'itération actuelle
			for u, v, w in self.graph:
				if dist[u] != float("Inf") and dist[u] + w < dist[v]:
					dist[v] = dist[u] + w
					predecessors[v] = u  # Met à jour le prédécesseur de v
					is_updated = True
			if not is_updated:
				break  # Stop s'il n'y a pas eu de mise à jour de distance
			iterations += 1

		# Vérification de la présence de circuit négatif
			if is_updated:
				# Une mise à jour s'est produite à la (V-1)-ème itération, ce qui indique la possibilité d'un cycle négatif
            			# Effectuer une itération supplémentaire pour détecter quelles distances sont mises à jour
				for u, v, w in self.graph:
					# Il y a une mise à jour à cette itération, indiquant la présence d'un cycle négatif
					if dist[u] != float("Inf") and dist[u] + w < dist[v]:
						print("Erreur: Le graphe contient un cycle négatif.")
						return

		# Affichage
		self.printArr(dist)
		print("> Nb d'iterations:", iterations)

		# Construction de l'arborescence des plus courts chemins
		shortest_paths_tree = [[] for _ in range(self.V)]  # Liste de listes pour stocker l'arborescence
		for vertex in range(self.V):
			if vertex != src:
				path = []
				current_vertex = vertex
				while current_vertex != src:
					if current_vertex not in predecessors:
						break
					path.insert(0, current_vertex)
					current_vertex = predecessors[current_vertex]
				path.insert(0, src)
				shortest_paths_tree[vertex] = path  # Ajoute le chemin à l'arborescence
		arbo = self.graphArborescence(shortest_paths_tree)
		return iterations, arbo

	def find_sources_and_sinks(self):
		in_degrees = [0 for i in range(self.V)]
		out_degrees = [0 for i in range(self.V)]
		sources = []; sinks = []
		for edge in self.graph:
			out_degrees[edge[0]] += 1
			in_degrees[edge[1]] += 1
		print("out_degrees:", out_degrees)
		print("in_degrees:", in_degrees)
		for i in range(len(out_degrees)):
			if out_degrees[i] > 0 and in_degrees[i] == 0: sources.append(i)
			if in_degrees[i] > 0 and out_degrees[i] == 0: sinks.append(i)
		#sources = [i for i in out_degrees if out_degrees[i] > 0 and in_degrees[i] == 0]
		#sinks = [i for i in in_degrees if in_degrees[i] > 0 and out_degrees[i] == 0]
		return sources, sinks

	def calculate_delta(self,u):
		in_degree = sum(1 for edge in self.graph if edge[1] == u)
		out_degree = sum(1 for edge in self.graph if edge[0] == u)
		return out_degree - in_degree

	


	def GloutonFas(self):

		s1 = []
		s2 = []

		while self.graph:
			sources, sinks = self.find_sources_and_sinks()
			print("sources:", sources); print("sinks:", sinks)
			if sources:
				while sources:
					e = sources.pop()		#! si plusieurs sources, l'ordre n'influe pas sur le résultat
					print("e:", e)
					s1.append(e)
					#sources.remove(e)
					print("sources:", sources)
					self.graph = [edge for edge in self.graph if (edge[0] != e)]
					sources, _ = self.find_sources_and_sinks()
			if sinks:
				while sinks:
					e = sinks.pop()
					s2.insert(0,e)
					#sinks.remove(e)
					self.graph = [edge for edge in self.graph if (edge[1] != e)]
					_, sinks = self.find_sources_and_sinks()
			print("graph actualisé:", self.graph)
			print("s1:", s1); print("s2:", s2)
			if self.graph:
				u = max(self.graph, key=lambda x: self.calculate_delta(x[0]))
				print("u:",u)
				if u[0] not in s1 and u[0] not in s2:
					s1.append(u[0])
					self.graph = [edge for edge in self.graph if (edge[0] != u[0] and edge[1] != u[0])]
				print(self.graph,"\n")
			

		s = s1 + s2
		result = []
		for i in s:
			if i not in result:
				result.append(i)

		return s1,s2,s, result
	
def unionGraphs(graph1, graph2, graph3):
	# Création du graphe final
	finalGraph = Graph(len(graph1.graph))
	
	# Parcours des arêtes des trois graphes en même temps
	for i in range(len(graph1.graph)):
		#for j in range(len(graph1.graph[i])):
		# Récupération des arêtes des trois graphes
		edge1 = graph1.graph[i]
		edge2 = graph2.graph[i]
		edge3 = graph3.graph[i]
		
		# 1 et 2 identiques 
		if edge1[0] == edge2[0] and edge1[1] == edge2[1]:
			minWeight = min(edge1[2], edge2[2])		# Sélection de l'arête avec le plus petit poids
			# Si 2 et 3 egalement identiques
			if edge2[0] == edge3[0] and edge2[1] == edge3[1]:
				minWeight = min(minWeight, edge3[2])	# Sélection de l'arête avec le plus petit poids
			# Sinon on ajoute la derniere arete
			else: finalGraph.addEdge(edge3[0], edge3[1], edge3[2])
			# On ajoute l'arete "doublon" avec le plus petit poids
			finalGraph.addEdge(edge1[0], edge1[1], minWeight)

		# 2 et 3 identiques 
		elif edge2[0] == edge3[0] and edge2[1] == edge3[1]:
			minWeight = min(edge2[2], edge3[2])
			finalGraph.addEdge(edge2[0], edge2[1], minWeight)
			finalGraph.addEdge(edge1[0], edge1[1], edge1[2])	# arete 1 distincte

		# 1 et 3 identiques
		elif edge1[0] == edge3[0] and edge1[1] == edge3[1]:
			minWeight = min(edge1[2], edge3[2])
			finalGraph.addEdge(edge1[0], edge1[1], minWeight)
			finalGraph.addEdge(edge2[0], edge2[1], edge2[2])	# arete 2 distincte

		# Toutes les aretes sont disctinctes : on ajoute tout
		else:
			finalGraph.addEdge(edge1[0], edge1[1], edge1[2])
			finalGraph.addEdge(edge2[0], edge2[1], edge2[2])
			finalGraph.addEdge(edge3[0], edge3[1], edge3[2])
			
		removeDupes(finalGraph.graph)
	return finalGraph


# Génération du graphe G
# G = Graph(7)
# G.addEdge(0, 1, 0)
# G.addEdge(0, 4, 0)
# G.addEdge(0, 5, 0)
# G.addEdge(1, 3, 0)
# G.addEdge(1, 5, 0)
# G.addEdge(2, 1, 0)
# G.addEdge(3, 1, 0)
# G.addEdge(3, 2, 0)
# G.addEdge(3, 6, 0)
# G.addEdge(3, 4, 0)
# G.addEdge(4, 5, 0)
# G.addEdge(5, 6, 0)
# G.addEdge(6, 0, 0)

G = Graph(8)
G.addEdge(0, 1, 0)
G.addEdge(0, 2, 0)
G.addEdge(1, 2, 0)
G.addEdge(2, 3, 0)
G.addEdge(3, 4, 0)
G.addEdge(3, 5, 0)
G.addEdge(3, 6, 0)
G.addEdge(4, 6, 0)
G.addEdge(5, 4, 0)
G.addEdge(5, 7, 0)
G.addEdge(6, 0, 0)
G.addEdge(7, 1, 0)
G.addEdge(7, 2, 0)

# G = Graph(5)
# G.addEdge(0, 1, 0)
# G.addEdge(0, 3, 0)
# G.addEdge(1, 4, 0)
# G.addEdge(2, 1, 0)
# G.addEdge(2, 3, 0)
# G.addEdge(2, 4, 0)
# G.addEdge(3, 4, 0)
# G.addEdge(4, 0, 0)

# print(G.find_sources_and_sinks())
# for e in range (G.V):
# 	print(G.calculate_delta(e))
s1,s2,s, result = G.GloutonFas()
print("s1: ", s1)
print("s2: ", s2)
print("s: ", s)
print("result: ", result)
#print(G.setSource())
# Sommet 0 comme source car il permet d'atteindre au moins |V|/2 sommets
source = 0

"""
# Génération des poids aléatoires pour G1, G2, G3, et H
G1 = Graph(8)
G1.graph = [edge.copy() for edge in G.graph]
G1.generateRandWeight()

G2 = Graph(8)
G2.graph = [edge.copy() for edge in G.graph]
G2.generateRandWeight()

G3 = Graph(8)
G3.graph = [edge.copy() for edge in G.graph]
G3.generateRandWeight()

H = Graph(8)
H.graph = [edge.copy() for edge in G.graph]
H.generateRandWeight()

# print("G:", G.graph)
# print("\nG1:", G1.graph)
# print("\nG2:", G2.graph)
# print("\nG3:", G3.graph)
# print("\nH:", H.graph) 

# print("\nPrésence de circuit négatif dans G :", G.hasNegativeCycle())
# print("Présence de circuit négatif dans G1 :", G1.hasNegativeCycle())
# print("Présence de circuit négatif dans G2 :", G2.hasNegativeCycle())
# print("Présence de circuit négatif dans G3 :", G3.hasNegativeCycle())
# print("Présence de circuit négatif dans H :", H.hasNegativeCycle())

i1, s1 = G1.BellmanFord(source)
i2, s2 = G2.BellmanFord(source)
i3, s3 = G3.BellmanFord(source)
print(s1.graph)
print(s2.graph)
print(s3.graph)

T = unionGraphs(s1,s2,s3)
print("Union:", T.graph)

print("GloutonFas sur T:", T.GloutonFas())"""

		

"""
# ------------ TEST ------------


g2 = Graph(4)
g2.addEdge(1, 2, 1)
g2.addEdge(2, 1, 1)
g2.addEdge(3, 1, 1)
g2.addEdge(3, 4, 1)
g2.addEdge(4, 2, 1)
result = g2.GloutonFas()
print("s = ", result)

G = Graph(4)
G.addEdge(0, 1, 1)
G.addEdge(1, 2, -2)
G.addEdge(2, 3, 3)
G.addEdge(3, 0, -4)

G1 = Graph(4)
G1.addEdge(0, 1, 1)
G1.addEdge(1, 2, 2)
G1.addEdge(2, 3, 3)
G1.addEdge(3, 0, 4)

# Vérification de la présence d'un circuit négatif
hasNegativeCycle = G.hasNegativeCycle()
print("Le graphe a un circuit négatif :", hasNegativeCycle)
hasNegativeCycle1 = G1.hasNegativeCycle()
print("Le graphe G1 a un circuit négatif :", hasNegativeCycle1)

G1 = Graph(4)
G1.addEdge(0, 1, 1)
G1.addEdge(1, 2, 2)
G1.addEdge(2, 3, 3)
G1.addEdge(3, 0, 4)
i, s = G1.BellmanFord(0)
print("S:", s.graph)
"""




