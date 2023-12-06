import random

def createPairs(lst):
	pairs = []
	for i in range(len(lst) - 1):
		pairs.append([lst[i], lst[i+1]])
	return pairs

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
					path.insert(0, current_vertex)
					current_vertex = predecessors[current_vertex]
				path.insert(0, src)
				shortest_paths_tree[vertex] = path  # Ajoute le chemin à l'arborescence
		arbo = self.graphArborescence(shortest_paths_tree)
		return iterations, arbo


	def GloutonFas(self):
		"""Application de l'algorithme GloutonFas"""
		# Initialisation
		s1 = []
		s2 = []

		# Conversion du graphe en représentation d'adjacence
		adj_list = {}
		in_degree = {}
		out_degree = {}

		for edge in self.graph:
			u, v, _ = edge  # Ignore weights for this algorithm
			if u not in adj_list:
				adj_list[u] = []
				in_degree[u] = 0
				out_degree[u] = 0
			if v not in adj_list:
				adj_list[v] = []
				in_degree[v] = 0
				out_degree[v] = 0

			adj_list[u].append(v)
			out_degree[u] += 1
			in_degree[v] += 1

		# Fonction pour choisir le sommet avec la différence maximale 
		# entre son degré sortant et son degré entrant (ici noté delta)
		def choose_vertex():
			max_delta = float("-inf")
			chosen_vertex = None

			for vertex in adj_list:
				delta = out_degree[vertex] - in_degree[vertex]
				if delta > max_delta:
					max_delta = delta
					chosen_vertex = vertex

			return chosen_vertex

		# Algorithme GloutonFast
		while adj_list:
			# Traitement des sources
			sources = [vertex for vertex in adj_list if in_degree[vertex] == 0]
			for source in sources:
				s1.append(source)
				for neighbor in adj_list[source]:
					in_degree[neighbor] -= 1
				del adj_list[source]

			# Traitement des puits
			sinks = [vertex for vertex in adj_list if out_degree[vertex] == 0]
			for sink in sinks:
				s2.insert(0, sink)
				for neighbor in adj_list[sink]:
					out_degree[neighbor] -= 1
				del adj_list[sink]

			# Choisir et retirer le sommet avec le plus grand delta
			chosen_vertex = choose_vertex()
			if chosen_vertex is not None:
				s1.append(chosen_vertex)
				for neighbor in adj_list[chosen_vertex]:
					in_degree[neighbor] -= 1
					out_degree[chosen_vertex] -= 1
				del adj_list[chosen_vertex]

		return s1 + s2
	
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
			else: finalGraph.addEdge(edge3[0], edge3[1], minWeight)
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
	return finalGraph



# Génération du graphe G
G = Graph(5)
G.addEdge(0, 1, 0)
G.addEdge(0, 2, 0)
G.addEdge(0, 4, 0)
G.addEdge(1, 3, 0)
G.addEdge(2, 3, 0)
G.addEdge(3, 4, 0)
	
# Sommet 0 comme source car il permet d'atteindre au moins |V|/2 sommets
source = 0

# Génération des poids aléatoires pour G1, G2, G3, et H
G1 = Graph(5)
G1.graph = [edge.copy() for edge in G.graph]
G1.generateRandWeight()

G2 = Graph(5)
G2.graph = [edge.copy() for edge in G.graph]
G2.generateRandWeight()

G3 = Graph(5)
G3.graph = [edge.copy() for edge in G.graph]
G3.generateRandWeight()

H = Graph(5)
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

S = unionGraphs(s1,s2,s3)
print("Union:", S.graph)

		

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



