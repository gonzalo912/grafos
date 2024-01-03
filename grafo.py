from random import choice


class Grafo:
	''' 
	TDA Grafo al instanciar una clase de este TDA
	se recibe como parametro si es un grafo dirigido o no 
	'''

	def __init__(self, dirigido):
		self.vertices = {}
		self.cant_vertices = 0
		self.es_dirigido = dirigido


	def __iter__(self):
		return iter(self.vertices)


	def __len__(self):
		return self.cant_vertices
	

	def agregar_vertice(self, vertice):
		if vertice in self.vertices:
			return False 
		self.vertices[vertice] = {}
		self.cant_vertices += 1
		return True


	def agregar_arista(self, vert_inicio, vertice_fin, peso = 1):
		if vert_inicio not in self.vertices or vertice_fin not in self.vertices:
			print(f'no se puede agregar la arista desde {vert_inicio} hacia {vertice_fin}')
			return False
		
		adya_inicio = self.vertices.get(vert_inicio, {})
		adya_inicio[vertice_fin] = peso
		self.vertices[vert_inicio] = adya_inicio
		if not self.es_dirigido:
			adyac_fin = self.vertices.get(vertice_fin, {})
			adyac_fin[vert_inicio] = peso
			self.vertices[vertice_fin] = adyac_fin
		
		return True


	def eliminar_arista(self, desde, hasta):
		if desde not in self.vertices or hasta not in self.vertices:
			print(f'no se puede eliminar la arista {desde} hacia {hasta}')
			return False

		dict_adyacente = self.vertices.get(desde, {})
		dict_adyacente.pop(hasta)
		self.vertices[desde] = dict_adyacente
		
		if not es_dirigido:
			dict_hasta = self.vertices[hasta]
			dict_hasta.pop(desde)
			self.vertices[hasta] = dict_hasta
		return True


	def eliminar_vertice(self, vertice):
		if vertice not in self.vertices:
			print(f'el vertice {vertice} no se encuetra en el grafo')
			return False
		
		del self.vertices[vertice]		
		
		for vertices in self.vertices.values():
			vertices.pop(vertice, None)
		self.cant_vertices -= 1
		
		return True


	def vertice_random(self):
		return choice(list(self.vertices.keys()))


	def adyacentes(self, vertice):
		if vertice not in self.vertices:
			print(f'el vertice {vertice} no se encuetra en el grafo')
			return False
		return list(self.vertices[vertice])


	def obtener_vertices(self):
		return list(self.vertices)


	def pertenece_vertice(self, vertice):
		return vertice in self.vertices


	def peso(self, vertice1, vertice2):
		dic_aux = self.vertices[vertice1]
		peso = dic_aux.get(vertice2, 1) 
		return peso


	def vertices_unidos(self, vertice1, vertice2):
		dic_aux = self.vertices[vertice1]
		if vertice2 in dic_aux:
			return vertice1, vertice2, self.peso(vertice1, vertice2)
		return False

