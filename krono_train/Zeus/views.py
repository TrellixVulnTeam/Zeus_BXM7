import json
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Cliente, Tienda, Subcategoria, Categoria, Producto, Canasta, Orden
from .serializers import ClienteSerializer, TiendaSerializer, SubcategoriaSerializer, CategoriaSerializer, ProductoSerializer, CanastaSerializer, OrdenSerializer
from rest_framework.decorators import api_view
# Create your views here.

#Endpoint 1 | Todos los clientes

def get_users(request):
	queryset = Cliente.objects.all()
	return JsonResponse({ 'response':[ob.as_json() for ob in queryset], 'code': '0'}, safe=False)

def get_entity_user(request):
	return JsonResponse({ 'Cliente': {'id': 'integer','nombre': 'string','apellido': 'string', 'email': 'string', }} )

#Endpoints Clientes Crear | Editar | Delete
@api_view(['POST'])
def cliente_endpoint(request):
	try:		
		if request.data['task'] == "add":
			cliente = Cliente(nombre=request.data['nombre'], apellido=request.data['apellido'], email=request.data['email']).save()
			return JsonResponse({'mensaje': 'Creado satisfactoriamente', 'code': '00'})
		elif request.data['task'] == 'edit':
			id_cliente = request.data['id']			
			queryset = Cliente.objects.filter(id=id_cliente)
			if queryset.count() > 0:
				queryset.update(nombre=request.data['nombre'], apellido=request.data['apellido'], email=request.data['email'])
				return JsonResponse({'mensaje': 'Editado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe ese cliente en la base de datos', 'code' : '03'})
		elif request.data['task'] == 'delete':
			id_cliente = request.data['id']			
			queryset = Cliente.objects.filter(id=id_cliente)
			if queryset.count() > 0:
				queryset.delete()
				return JsonResponse({'mensaje': 'Eliminado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe ese cliente en la base de datos', 'code' : '03'})
			
		else:
			return JsonResponse({'mensaje': 'Error - parámetro task sin especificar', 'code' : '02'})
	except Exception as e:
		print(e)		
		return JsonResponse({'mensaje': 'Error - Datos enviados están mal parametrizados', 'code' : '01'})

#Endpoint 2 | Todas las subcategorias
def get_subcategoria(request):
	queryset = Subcategoria.objects.all()
	return JsonResponse({ 'response':[ob.as_json() for ob in queryset], 'code': '0'}, safe=False)

def get_entity_subcategoria(request):
	return JsonResponse({ 'Subcategoria': {'id': 'integer','nombre': 'string','activa': 'boolean' }} )

#Endpoints Clientes Crear | Editar | Delete
@api_view(['POST'])
def subcategoria_endpoint(request):
	try:		
		if request.data['task'] == "add":
			subcategoria = Subcategoria(nombre=request.data['nombre'], activa=request.data['activa']).save()
			return JsonResponse({'mensaje': 'Creado satisfactoriamente', 'code': '00'})
		elif request.data['task'] == 'edit':
			id_subcategoria = request.data['id']			
			queryset = Subcategoria.objects.filter(id=id_subcategoria)
			if queryset.count() > 0:
				queryset.update(nombre=request.data['nombre'], activa=request.data['activa'])
				return JsonResponse({'mensaje': 'Editado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa subcategoria en la base de datos', 'code' : '03'})
		elif request.data['task'] == 'delete':
			id_subcategoria = request.data['id']			
			queryset = Subcategoria.objects.filter(id=id_subcategoria)
			if queryset.count() > 0:
				queryset.delete()
				return JsonResponse({'mensaje': 'Eliminado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa subcategoria en la base de datos', 'code' : '03'})
			
		else:
			return JsonResponse({'mensaje': 'Error - parámetro task sin especificar', 'code' : '02'})
	except Exception as e:
		print(e)		
		return JsonResponse({'mensaje': 'Error - Datos enviados están mal parametrizados', 'code' : '01'})

#Endpoint 3 | Todas las categoria 
def get_categoria(request):
	queryset = Categoria.objects.all()
	return JsonResponse({ 'response':[ob.as_json() for ob in queryset], 'code': '0'}, safe=False)

def get_entity_categoria(request):
	return JsonResponse({ 'Categoria': {'id': 'integer','nombre': 'string','activa': 'boolean', 'subcategorias': 'Array de Subcategorias' }} )

#Endpoints Categorias Crear | Editar | Delete
@api_view(['POST'])
def categoria_endpoint(request):
	try:		
		if request.data['task'] == "add":	
			array = []
			queryset = Subcategoria.objects.filter(id__in=request.data['subcategorias'])
			for sub in queryset:				
				array.append(sub)
			categoria = Categoria(nombre=request.data['nombre'], activa=request.data['activa'])
			categoria.save()
			for subcat in array:
				categoria.subcategorias.add(subcat)
			return JsonResponse({'mensaje': 'Creado satisfactoriamente', 'code': '00'})
		elif request.data['task'] == 'edit':
			array = []
			queryset = Subcategoria.objects.filter(id__in=request.data['subcategorias'])
			for sub in queryset:				
				array.append(sub)
			id_Categoria = request.data['id']
			queryset = Categoria.objects.filter(id=id_Categoria)
			if queryset.count() > 0:
				categoria = queryset.update(nombre=request.data['nombre'], activa=request.data['activa'])
				queryset[0].subcategorias.clear()
				for subcat in array:
					queryset[0].subcategorias.add(subcat)
				return JsonResponse({'mensaje': 'Editado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa categoria en la base de datos', 'code' : '03'})
			
		elif request.data['task'] == 'delete':
			id_Categoria = request.data['id']			
			queryset = Categoria.objects.filter(id=id_Categoria)
			if queryset.count() > 0:
				queryset.delete()
				return JsonResponse({'mensaje': 'Eliminado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa categoria en la base de datos', 'code' : '03'})
			
		else:
			return JsonResponse({'mensaje': 'Error - parámetro task sin especificar', 'code' : '02'})
	except Exception as e:
		print(e)		
		return JsonResponse({'mensaje': 'Error - Datos enviados están mal parametrizados', 'code' : '01'})


#Endpoint 4 | Todos los productos 
def get_producto(request):
	queryset = Producto.objects.all()
	return JsonResponse({ 'response':[ob.as_json() for ob in queryset], 'code': '0'}, safe=False)

def get_entity_producto(request):
	return JsonResponse({ 'Producto': {'id': 'integer','nombre': 'string','precio': 'double', 'foto': 'string','subcategorias': 'Array de Subcategorias' }} )

#Endpoints Categorias Crear | Editar | Delete
@api_view(['POST'])
def producto_endpoint(request):
	try:		
		if request.data['task'] == "add":	
			array = []
			queryset = Subcategoria.objects.filter(id__in=request.data['subcategorias'])
			for sub in queryset:				
				array.append(sub)
			producto = Producto(nombre=request.data['nombre'], precio=request.data['precio'], foto=request.data['foto'])
			producto.save()
			for subcat in array:
				producto.subcategoria.add(subcat)
			return JsonResponse({'mensaje': 'Creado satisfactoriamente', 'code': '00'})
		elif request.data['task'] == 'edit':
			array = []
			queryset = Subcategoria.objects.filter(id__in=request.data['subcategorias'])
			for sub in queryset:				
				array.append(sub)
			id_Producto = request.data['id']
			queryset = Producto.objects.filter(id=id_Producto)
			if queryset.count() > 0:
				producto = queryset.update(nombre=request.data['nombre'], precio=request.data['precio'], foto=request.data['foto'])
				queryset[0].subcategoria.clear()
				for subcat in array:
					queryset[0].subcategoria.add(subcat)
				return JsonResponse({'mensaje': 'Editado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa producto en la base de datos', 'code' : '03'})
			
		elif request.data['task'] == 'delete':
			id_Producto = request.data['id']			
			queryset = Producto.objects.filter(id=id_Producto)
			if queryset.count() > 0:
				queryset.delete()
				return JsonResponse({'mensaje': 'Eliminado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa producto en la base de datos', 'code' : '03'})
			
		else:
			return JsonResponse({'mensaje': 'Error - parámetro task sin especificar', 'code' : '02'})
	except Exception as e:
		print(e)		
		return JsonResponse({'mensaje': 'Error - Datos enviados están mal parametrizados', 'code' : '01'})


#Endpoint 5 | Todas las tiendas 
def get_tienda(request):
	queryset = Tienda.objects.all()
	return JsonResponse({ 'response':[ob.as_json() for ob in queryset], 'code': '0'}, safe=False)

def get_entity_tienda(request):
	return JsonResponse({ 'Tienda': {'id': 'integer','nombre': 'string', 'ubicacion': 'string','categorias': 'Array de Categorias', 'clientes': 'Array de Clientes' }} )

#Endpoints Tienda Crear | Editar | Delete
@api_view(['POST'])
def tienda_endpoint(request):
	try:		
		if request.data['task'] == "add":	
			array_clientes = []
			queryset = Cliente.objects.filter(id__in=request.data['clientes'])
			for sub in queryset:				
				array_clientes.append(sub)

			array_categorias = []
			queryset = Categoria.objects.filter(id__in=request.data['categorias'])
			for sub in queryset:
				array_categorias.append(sub)

			tienda = Tienda(nombre=request.data['nombre'], ubicacion=request.data['ubicacion'])
			tienda.save()
			for cliente in array_clientes:
				tienda.clientes.add(cliente)

			for cate in array_categorias:
				tienda.categorias.add(cate)

			return JsonResponse({'mensaje': 'Creado satisfactoriamente', 'code': '00'})
		elif request.data['task'] == 'edit':
			array_clientes = []
			queryset = Cliente.objects.filter(id__in=request.data['clientes'])
			for sub in queryset:				
				array_clientes.append(sub)

			array_categorias = []
			queryset = Categoria.objects.filter(id__in=request.data['categorias'])
			for sub in queryset:
				array_categorias.append(sub)

			id_Tienda = request.data['id']
			queryset = Tienda.objects.filter(id=id_Tienda)
			if queryset.count() > 0:
				tienda = queryset.update(nombre=request.data['nombre'], ubicacion=request.data['ubicacion'])
				queryset[0].clientes.clear()
				queryset[0].categorias.clear()
				for cliente in array_clientes:
					queryset[0].clientes.add(cliente)

				for categoria in array_categorias:
					queryset[0].categorias.add(categoria)

				return JsonResponse({'mensaje': 'Editado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa tienda en la base de datos', 'code' : '03'})
			
		elif request.data['task'] == 'delete':
			id_Tienda = request.data['id']			
			queryset = Tienda.objects.filter(id=id_Tienda)
			if queryset.count() > 0:
				queryset.delete()
				return JsonResponse({'mensaje': 'Eliminado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa tienda en la base de datos', 'code' : '03'})
			
		else:
			return JsonResponse({'mensaje': 'Error - parámetro task sin especificar', 'code' : '02'})
	except Exception as e:
		print(e)		
		return JsonResponse({'mensaje': 'Error - Datos enviados están mal parametrizados', 'code' : '01'})

#Endpoint 6 | Todas las canastas 
def get_canasta(request):
	queryset = Canasta.objects.all()
	return JsonResponse({ 'response':[ob.as_json() for ob in queryset], 'code': '0'}, safe=False)

def get_entity_canasta(request):
	return JsonResponse({ 'Canasta': {'id': 'integer', 'productos': 'Array de Productos', 'cliente': 'Cliente', 'tienda': 'Tienda' }} )

#Endpoints Canasta Crear | Editar | Delete
@api_view(['POST'])
def canasta_endpoint(request):
	try:		
		if request.data['task'] == "add":	
			array_productos = []
			queryset = Producto.objects.filter(id__in=request.data['productos'])
			for sub in queryset:				
				array_productos.append(sub)
			tienda = Tienda.objects.filter(id=request.data['tienda'])
			cliente = Cliente.objects.filter(id=request.data['cliente'])

			if tienda.count() > 0 and cliente.count() > 0:
				canasta = Canasta(cliente=cliente[0], tienda= tienda[0])
				canasta.save()
				for producto in array_productos:
					canasta.productos.add(producto)	
				return JsonResponse({'mensaje': 'Creado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esta tienda o cliente en la base de datos', 'code': '03'})
			
		elif request.data['task'] == 'edit':
			array_productos = []
			queryset = Producto.objects.filter(id__in=request.data['productos'])
			for sub in queryset:				
				array_productos.append(sub)
			
			id_Canasta = request.data['id']
			queryset = Canasta.objects.filter(id=id_Canasta)
			if queryset.count() > 0:
				tienda = Tienda.objects.filter(id=request.data['tienda'])
				cliente = Cliente.objects.filter(id=request.data['cliente'])

				if tienda.count() > 0 and cliente.count() > 0:
					canasta = queryset.update(cliente=cliente[0], tienda= tienda[0])
					queryset[0].productos.clear()
					for producto in array_productos:
						queryset[0].productos.add(producto)
					return JsonResponse({'mensaje': 'Editado satisfactoriamente', 'code': '00'})
				else:
					return JsonResponse({'mensaje': 'No existe esta tienda o cliente en la base de datos', 'code': '03'})
			else:
				return JsonResponse({'mensaje': 'No existe esa Canasta en la base de datos', 'code' : '03'})
			
		elif request.data['task'] == 'delete':
			id_Canasta = request.data['id']			
			queryset = Canasta.objects.filter(id=id_Canasta)
			if queryset.count() > 0:
				queryset.delete()
				return JsonResponse({'mensaje': 'Eliminado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa Canasta en la base de datos', 'code' : '03'})
			
		else:
			return JsonResponse({'mensaje': 'Error - parámetro task sin especificar', 'code' : '02'})
	except Exception as e:
		print(e)		
		return JsonResponse({'mensaje': 'Error - Datos enviados están mal parametrizados', 'code' : '01'})

#Endpoint 7 | Todas las ordenes 
def get_orden(request):
	queryset = Orden.objects.all()
	return JsonResponse({ 'response':[ob.as_json() for ob in queryset], 'code': '0'}, safe=False)

def get_entity_orden(request):
	return JsonResponse({ 'Orden': {'id': 'integer', 'canasta': 'Canasta'}} )

#Endpoints Ordenes Crear | Editar | Delete
@api_view(['POST'])
def orden_endpoint(request):
	try:		
		if request.data['task'] == "add":				
			canasta = Canasta.objects.filter(id=request.data['canasta'])
			if canasta.count() > 0:
				orden = Orden(canasta=canasta[0])
				orden.save()
				return JsonResponse({'mensaje': 'Creado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa canasta en la base de datos', 'code': '03'})
			
		elif request.data['task'] == 'edit':
			
			id_Orden = request.data['id']
			queryset = Orden.objects.filter(id=id_Orden)
			if queryset.count() > 0:
				canasta = Canasta.objects.filter(id=request.data['canasta'])
				if canasta.count() > 0:
					canasta = queryset.update(canasta=canasta[0])
					return JsonResponse({'mensaje': 'Editado satisfactoriamente', 'code': '00'})
				else:
					return JsonResponse({'mensaje': 'No existe esta canasta en la base de datos', 'code': '03'})
			else:
				return JsonResponse({'mensaje': 'No existe esa Orden en la base de datos', 'code' : '03'})
			
		elif request.data['task'] == 'delete':
			id_Orden = request.data['id']			
			queryset = Orden.objects.filter(id=id_Orden)
			if queryset.count() > 0:
				queryset.delete()
				return JsonResponse({'mensaje': 'Eliminado satisfactoriamente', 'code': '00'})
			else:
				return JsonResponse({'mensaje': 'No existe esa Orden en la base de datos', 'code' : '03'})
			
		else:
			return JsonResponse({'mensaje': 'Error - parámetro task sin especificar', 'code' : '02'})
	except Exception as e:
		print(e)		
		return JsonResponse({'mensaje': 'Error - Datos enviados están mal parametrizados', 'code' : '01'})