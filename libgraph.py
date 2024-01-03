from grafo import * 
from collections import deque
from random import shuffle
import heapq as hp 

ITER_LABELS = 25
DAMPING_FACTOR = 0.85
ITER_PR = 45 


def bfs(grafo, inicio):
	visitados = set()
	costo = {}
	padre = {}
	
	visitados.add(inicio)
	padre[inicio] = None
	costo[inicio] = 0
	cola = deque()
	cola.append(inicio)
	while(cola):
		vertice = cola.popleft()
		for adyac in grafo.adyacentes(vertice):
			if adyac in visitados:
				continue
			visitados.add(adyac)
			padre[adyac] = vertice
			costo[adyac] = costo[vertice] + 1
			cola.append(adyac)

	return padre, costo


def camino_minimo(grafo, inicio, fin):
	camino = []
	costo = None
	padres, distancia = bfs(grafo, inicio)
	if fin not in distancia:
		return [], costo

	seguir = fin 
	camino.append(seguir)

	while padres[seguir] != None:
		insertar = padres[seguir]
		camino.append(insertar)
		seguir = insertar

	costo = distancia[fin]
	return camino[::-1], costo


def diametro_grafo(grafo):
	max_min_dist = 0
	padres = {}
	costo = {}
	for vertice in grafo:
		caminos, distancias = bfs(grafo, vertice)
		if (max(distancias.values()) > max_min_dist):
			padres = caminos
			costo = distancias
			max_min_dist = max(distancias.values())

	
	return max_min_dist, padres, costo


def ciclo(grafo, vertice, n, inicio, camino, visitados):
	if len(camino) == n:
		if vertice == inicio:
			camino.append(inicio)
			return True
		return False

	if len(camino) >= n or vertice in visitados:
		return False
	
	camino.append(vertice)
	visitados.add(vertice)

	for w in grafo.adyacentes(vertice):
		if ciclo(grafo, w, n, inicio, camino, visitados):
			return True
	
	camino.pop()
	visitados.remove(vertice)
	return False


def ciclo_de_largo_n(grafo, v, n):
	list_ciclo = []
	inicio = v
	visitados = set()
	ciclo(grafo, v, n, inicio, list_ciclo, visitados)
	return list_ciclo



def info_links(grafo):
	links_entrantes = {}
	cant_links = {} 
	for pagina in grafo:
		links_entrantes[pagina] = []
		cant_links[pagina] = 0

	for pagina in grafo:
		for link in grafo.adyacentes(pagina):
			links_entrantes[link].append(pagina)
			cant_links[pagina] += 1

	return links_entrantes, cant_links 


def pagerank(web, coef_amortiguacion = DAMPING_FACTOR, iteraciones = ITER_PR):  

	links_entrantes, cant_links = info_links(web)
	rank = {}
	for pagina in web:
		rank[pagina] = 1 / float(len(web))

	for _ in range(iteraciones):
		new_rank = {}
		for pagina in web:
			sum_rank = 0
			inlinks = links_entrantes[pagina]
			for link in inlinks:
				sum_rank += (float(rank.get(link)) / float(cant_links.get(link)))
	
			total_rango = ((1 - coef_amortiguacion) / float(len(web))) + coef_amortiguacion * sum_rank
			new_rank[pagina] = total_rango
		rank = new_rank


	return rank


def cfc(grafo):
	vertice = grafo.vertice_random()
	todas_cfc = []
	visitados = set()
	pila = deque()
	apilados = set()
	orden = {}
	mas_bajo = {}
	orden[vertice] = 0
	componentes_fuertemente_conexas(grafo, vertice, visitados, pila, apilados, orden, mas_bajo, todas_cfc)
	return todas_cfc

def componentes_fuertemente_conexas(grafo, v, visitados, pila, apilados, orden, mas_bajo, todas_cfc):
	visitados.add(v)
	mas_bajo[v] = orden[v]
	pila.appendleft(v)
	apilados.add(v)
	
	for w in grafo.adyacentes(v):
		if w not in visitados:
			orden[w] = orden[v] + 1
			componentes_fuertemente_conexas(grafo, w, visitados, pila, apilados, orden, mas_bajo, todas_cfc)
			mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])

		elif w in apilados:
			mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
   
	if orden[v] == mas_bajo[v]:
		nueva_cfc = []
		while True:
			w = pila.popleft()
			apilados.remove(w)
			nueva_cfc.append(w)
			if w == v:
				break

		todas_cfc.append(nueva_cfc)
  

def max_freq(vertice, vertices_entrantes, labels):

	if len(vertices_entrantes[vertice]) == 0:
		return labels[vertice]
	
	entrantes = vertices_entrantes[vertice]
	dict_frecuencias = {}
	label_mas_freq = None

	for entrante in entrantes:
		label = labels[entrante]
		if not label_mas_freq:
			label_mas_freq = label
		if label not in dict_frecuencias:
			dict_frecuencias[label] = 1
		else:
			dict_frecuencias[label] += 1

		if dict_frecuencias[label] > dict_frecuencias[label_mas_freq]:
			label_mas_freq = label
	
	return label_mas_freq


def label_propagation(grafo):
	labels = {}
	iniciar = 0
	for v in grafo:
		labels[v] = iniciar
		iniciar+=1

	vertices_entrantes, cant_entrantes = info_links(grafo)
	vertices = grafo.obtener_vertices()
	shuffle(vertices)
	
	for i in range(ITER_LABELS):
		shuffle(vertices)
		for v in vertices:
			labels[v] = max_freq(v, vertices_entrantes, labels)
	
	return labels
	
	



