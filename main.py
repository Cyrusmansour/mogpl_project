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
	def __init__(self):
		"""Initialisation"""
		self.graph = []
		self.vertices = []

	def addEdge(self, u, v, w):
		"""Ajout d'une arete uv de poids w"""
		self.graph.append([u, v, w])
		if u not in self.vertices: self.vertices.append(u)
		if v not in self.vertices: self.vertices.append(v)

	# TODO: def removeEdge(self, u, v): self.graph = [ edge for edge in self.graph if edge[0] == u and edge[1] == v ]
	
	def removeVertex(self, u):
		"""Enleve le sommet u du graphe"""
		self.vertices.remove(u)
		self.graph = [ edge for edge in self.graph if (edge[0] != u and edge[1] != u)]

	def getVertexCount(self):
		return len(self.vertices)

	def getEdgeWeight(self, u, v):
		"""Renvoie le poids associé à l'arete uv"""
		for edge in self.graph:
			if edge[0] == u and edge[1] == v:
				return edge[2]
		return None

	def printArr(self, dist):
		"""Affichage de la solution"""
		print("Arete\t\tDist. depuis source")
		for i in range(len(dist)):
			print("{0}\t\t{1}".format(i, dist[i]))

	def hasNegativeCycle(self):
		"""Verifie la presence de circuit negatif dans le graphe"""
		dist = [float("Inf")] * self.getVertexCount()
		dist[0] = 0
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
		while self.hasNegativeCycle():
			for edge in self.graph:
				edge[2] = random.randint(-10, 10)
    
	def generate_random_graph():
		"""Génère un graphe aléatoire"""
		num_vertices = random.randint(3, 10)  # Choisissez le nombre de sommets aléatoirement (entre 2 et 10 ici)
		graph = Graph()

		for _ in range(random.randint(num_vertices, num_vertices * (num_vertices - 1) // 2)):
			u = random.randint(0, num_vertices - 1)
			v = random.randint(0, num_vertices - 1)
			while u == v or graph.getEdgeWeight(u, v) is not None:
				u = random.randint(0, num_vertices - 1)
				v = random.randint(0, num_vertices - 1)

			weight = random.randint(-10, 10)  # Poids de l'arête choisi aléatoirement (entre 1 et 10 ici)
			graph.addEdge(u, v, weight)

		sorted_list = sorted(graph.graph, key=lambda x: (x[0], x[1]))
		graph.graph = sorted_list
		return graph

	def setSource(self):
		"""Renvoie le premier sommet qui atteint au moins la moitié des sommets du graphe"""
		num_vertices = self.getVertexCount()  # Nombre de sommets du graphe
		threshold = num_vertices // 2  # Seuil pour atteindre la moitié des sommets 
		v = []	# liste pour stocker tous les sommets candidats 
		for vertex in self.vertices:#range(num_vertices):
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
		G = Graph()
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
		dist = [float("Inf")] * self.getVertexCount()
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
		shortest_paths_tree = [[] for _ in range(self.getVertexCount())]  # Liste de listes pour stocker l'arborescence
		for vertex in range(self.getVertexCount()):
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

def unionGraphs(graph1, graph2, graph3):
	# Création du graphe final
	finalGraph = Graph()
	
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

G = Graph.generate_random_graph()
print("G:", G.graph)
print("GloutonFas sur G:" , G.GloutonFas())