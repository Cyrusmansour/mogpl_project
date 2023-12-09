import random

def createPairs(lst):
	"""[0 1 2 3 4] -> [[0,1],[1,2],[2,3],[3,4]]"""
	pairs = []
	for i in range(len(lst) - 1):
		pairs.append([lst[i], lst[i+1]])
	return pairs

def removeDupes(lst):
	"""Enlève les doublons d'une liste de listes"""
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
	def __init__(self):
		"""Initialisation du graphe"""
		self.graph = []
		self.vertices = []

	def addEdge(self, u, v, w):
		"""Ajout d'une arete uv de poids w"""
		self.graph.append([u, v, w])
		if u not in self.vertices: self.vertices.append(u)
		if v not in self.vertices: self.vertices.append(v)

	def removeEdge(self, u, v): 
		"""Enleve l'arete uv du graphe"""
		self.graph = [ edge for edge in self.graph if edge[0] == u and edge[1] == v ]
	
	def removeVertex(self, u):
		"""Enleve le sommet u du graphe"""
		self.vertices.remove(u)
		self.graph = [ edge for edge in self.graph if (edge[0] != u and edge[1] != u)]

	def getVertexCount(self):
		"""Renvoie le nombre de sommets du graphe"""
		return len(self.vertices)

	def getEdgeWeight(self, u, v):
		"""Renvoie le poids associé à l'arete uv"""
		for edge in self.graph:
			if edge[0] == u and edge[1] == v:
				return edge[2]
		return None

	def printArr(self, dist):
		"""Affichage de la solution pour BellmanFord"""
		print("Arete\t\tDist. depuis source")
		for vertex in dist.keys():
			print("{0}\t\t{1}".format(vertex, dist[vertex]))

	def hasNegativeCycle(self):
		"""Verifie la presence de circuit negatif dans le graphe"""
		dist = { vertex: float("Inf") for vertex in self.vertices }
		dist[self.setSource()] = 0
		for _ in range(self.getVertexCount() - 1):
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
    
	def generate_random_graph():
		"""Génère un graphe aléatoire"""
		num_vertices = random.randint(4, 10)	# Nb de sommets (entre 4 et 10 ici)
		graph = Graph()

		for _ in range(random.randint(num_vertices, num_vertices * (num_vertices - 1) // 2)):
			u = random.randint(0, num_vertices - 1)
			v = random.randint(0, num_vertices - 1)
			while u == v or graph.getEdgeWeight(u, v) is not None:
				u = random.randint(0, num_vertices - 1)
				v = random.randint(0, num_vertices - 1)

			weight = random.randint(-10, 10)  # Poids de l'arête choisi aléatoirement (entre -10 et 10 ici)
			graph.addEdge(u, v, weight)

		sorted_list = sorted(graph.graph, key=lambda x: (x[0], x[1]))
		graph.graph = sorted_list
		return graph

	def countAccessibleVertexFrom(self, vertex):
		"""Compte le nombre de sommet accessible depuis vertex"""
		accessible = [vertex]
		edges = [edge for edge in self.graph if edge[1] != vertex ]
		k = 0
		while k < len(accessible):
			# on recupere les noeuds enfants
			childs = [ edge[1] for edge in edges if edge[0] == accessible[k]]
			# on enleve toutes les aretes connectees au sommet
			edges = [ edge for edge in edges if edge[0] != accessible[k] and edge[1] not in childs ]
			accessible += childs
			k += 1
		return len(accessible) - 1

	def hasSource(self):
		"""Renvoie true s'il existe une source dans le graphe, false le cas échéant"""
		threshold = self.getVertexCount() / 2
		for vertex in self.vertices:
			if self.countAccessibleVertexFrom(vertex) > threshold:
				return True
		return False

	def setSource(self):
		"""Renvoie la source du graphe"""
		threshold = self.getVertexCount() / 2
		for vertex in self.vertices:
			if self.countAccessibleVertexFrom(vertex) > threshold:
				return vertex
		#print("Erreur: aucun sommet n'atteint la moitié des sommets du graphe")
		return None

	def graphArborescence(self, s):
		"""Renvoie l'arborescence des plus courts chemins a partir d'une liste de predecesseurs"""
		t= []
		G = Graph()
		for e in s.values():
			t.append(createPairs(e))
		t = [pair for sublist in t for pair in sublist if sublist]	# on desimbrique les listes
		t = list(set(map(tuple, t)))	# on garde une seule occurence de chaque element
		for v in t:
			G.addEdge(v[0],v[1], self.getEdgeWeight(v[0],v[1]))
		return G

	def BellmanFord(self, src):
		"""Application de l'algo de BellmanFord : renvoie nb d'itérations + arborescence des plus courts chemins"""
		# Initialisation des distances depuis la source aux autres sommets à l'infini
		dist = { vertex: float("Inf") for vertex in self.vertices }
		dist[src] = 0
		# Initialisation des prédécesseurs
		predecessors = {}
		# Relaxation des arêtes au plus |V| - 1 fois
		iterations = 0  # Compteur d'itérations
		for _ in range(self.getVertexCount() - 1):
			is_updated = False  # Flag pour vérifier si une distance a été mise à jour dans l'itération actuelle
			for u, v, w in self.graph:
				if dist[u] != float("Inf") and dist[u] + w < dist[v]:
					dist[v] = dist[u] + w
					predecessors[v] = u  # Met à jour le prédécesseur de v
					is_updated = True
			if not is_updated:
				break  # Stop s'il n'y a pas eu de mise à jour de distance
			iterations += 1
		# Affichage - à decommenter si besoin
		# self.printArr(dist)
		# print("> Nb d'iterations:", iterations)
  
		# Construction de l'arborescence des plus courts chemins
		# vertex -> chemin (list<vertex>)
		shortest_paths_tree = { vertex: [] for vertex in self.vertices } # Liste de listes pour stocker l'arborescence
		for vertex in self.vertices:
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
		"""Renvoie la liste des sources et des puits du graphe"""
		in_degrees = { vertex: 0 for vertex in self.vertices }
		out_degrees = { vertex: 0 for vertex in self.vertices }
		sources = []; sinks = []
		for edge in self.graph:
			out_degrees[edge[0]] += 1
			in_degrees[edge[1]] += 1
		for vertex in self.vertices:
			if out_degrees[vertex] > 0 and in_degrees[vertex] == 0: sources.append(vertex)
			if in_degrees[vertex] > 0 and out_degrees[vertex] == 0: sinks.append(vertex)
		return sources, sinks

	def calculate_delta(self,u):
		"""Calcule le delta du sommet u"""
		in_degree = sum(1 for edge in self.graph if edge[1] == u)
		out_degree = sum(1 for edge in self.graph if edge[0] == u)
		return out_degree - in_degree

	def GloutonFas(self):
		"""Application de l'ago GloutonFas"""
		s1 = []
		s2 = []
		while self.vertices:
			sources, sinks = self.find_sources_and_sinks()
			if sources:
				while sources:
					e = sources.pop()		#! si plusieurs sources, l'ordre n'influe pas sur le résultat
					s1.append(e)
					self.removeVertex(e)
					sources, sinks = self.find_sources_and_sinks()
			if sinks:
				while sinks:
					e = sinks.pop()
					s2.insert(0,e)
					self.removeVertex(e)
					sources, sinks = self.find_sources_and_sinks()
			if self.vertices:
				u = max(self.vertices, key=lambda x: self.calculate_delta(x))
				s1.append(u)
				self.removeVertex(u)
		return s1 + s2

	def rearrangeEdges(self, vertices):
		"""Re-arrange les aretes selon une liste de sommets"""
		G = Graph()
		for vertex in vertices:
			for edge in self.graph:
				if edge[0] == vertex:
					G.addEdge(edge[0], edge[1], edge[2])
		return G
        
def unionGraphs(graph1, graph2, graph3):
	"""Renvoie l'union de trois graphes passés en argument"""
	finalGraph = Graph()
	# Parcours des arêtes des trois graphes en même temps
	for i in range(len(graph1.graph)):
		# Récupération des arêtes
		edge1 = graph1.graph[i]
		edge2 = graph2.graph[i]
		edge3 = graph3.graph[i]
		# si 1 et 2 identiques 
		if edge1[0] == edge2[0] and edge1[1] == edge2[1]:
			minWeight = min(edge1[2], edge2[2])		# Sélection de l'arête avec le plus petit poids
			# Si 2 et 3 egalement identiques
			if edge2[0] == edge3[0] and edge2[1] == edge3[1]:
				minWeight = min(minWeight, edge3[2])	# Sélection de l'arête avec le plus petit poids
			# Sinon on ajoute la derniere arete
			else: finalGraph.addEdge(edge3[0], edge3[1], edge3[2])
			# On ajoute l'arete "doublon" avec le plus petit poids
			finalGraph.addEdge(edge1[0], edge1[1], minWeight)
		# si 2 et 3 identiques 
		elif edge2[0] == edge3[0] and edge2[1] == edge3[1]:
			minWeight = min(edge2[2], edge3[2])
			finalGraph.addEdge(edge2[0], edge2[1], minWeight)
			finalGraph.addEdge(edge1[0], edge1[1], edge1[2])	# arete 1 distincte
		# si 1 et 3 identiques
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

def generateGraph():
    """Genere un graphe aleatoire qui ne contient pas de cycle négatif"""
    G = Graph.generate_random_graph()
    while not G.hasSource():
        G = Graph.generate_random_graph()
    if G.hasNegativeCycle(): 
        while not G.hasSource():
            G = Graph.generate_random_graph()
    return G

def generateGraphFromG(G):
    """Genere un graphe à partir de G : memes aretes mais poids différents"""
    G1 = Graph()
    for edge in G.graph:
        G1.addEdge(edge[0], edge[1], edge[2])
    G1.generateRandWeight()
    while G1.hasNegativeCycle():
        G1.generateRandWeight()
    return G1

# ------------------------------- TEST ---------------------------------

# Generation d'un graphe aleatoire 
G = generateGraph()
G1 = generateGraphFromG(G)
G2 = generateGraphFromG(G)
G3 = generateGraphFromG(G)
H = generateGraphFromG(G)
# print("G:", G3.graph)
# print("G1:", G.graph)
# print("G2:", G1.graph)
# print("G3:", G2.graph)
# print("H:", H.graph)

# BellmanFord sur G1 G2 G3
s = G.setSource()
i1, a1 = G1.BellmanFord(s)
i2, a2 = G2.BellmanFord(s)
i3, a3 = G3.BellmanFord(s)
# Union des arborescences
T = unionGraphs(a1, a2, a3)
#print("T:", T.graph)

# GloutonFas sur T
ordre_tot = T.GloutonFas()
H_bf = H.rearrangeEdges(ordre_tot)
iH_tot,aH_tot = H_bf.BellmanFord(ordre_tot[0])
iH, aH = H.BellmanFord(s)
print("Itérations BF sur H :", iH)
print("Itérations BF sur H avec ordre tot. :", iH_tot)

def generate_leveled_graph(levels, vertices_per_level):
	"""Génère un graphe par niveau avec des poids aléatoires pour toutes les arêtes"""
	graph = Graph()
	for level in range(levels - 1):
		for i in range(vertices_per_level):
			for j in range(vertices_per_level):
				u = level * vertices_per_level + i
				v = (level + 1) * vertices_per_level + j
				weight = random.randint(-10, 10)
				graph.addEdge(u, v, weight)
	sorted_list = sorted(graph.graph, key=lambda x: (x[0], x[1]))
	graph.graph = sorted_list
	return graph

g = generate_leveled_graph(2500,4)