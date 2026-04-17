import json
import csv
import datetime
ac = "mas_vendido.json"
def menuPrincipal():
    print("---------------------------------------")
    print("SISTEMA DE FACRURACION RESTAURANTE ACME")
    print("1. Menu productos")
    print("2. Menu mesas")
    print("3. Menu clientes")
    print("4. Crear factura")
    print("5. Registro de ventas")
    print("6. Ranking menos vendidos")
    print("7. Productos mas vendidos")
    print("8. Salir")
    print("---------------------------------------")
    
def menuProductos():
    print("---------------------------------------")
    print("MENU PRODUCTOS")
    print("1. registrar producto")
    print("2. ver productos")
    print("3. Salir")
    print("---------------------------------------")
    
def menuMesas():
    print("---------------------------------------")
    print("MENU MESAS")
    print("1. registrar mesas")
    print("2. ver mesas")
    print("3. Salir")
    print("---------------------------------------")
    
def menuClientes():
    print("---------------------------------------")
    print("MENU CLIENTES")
    print("1. registrar clientes")
    print("2. ver clientes")
    print("3. Salir")
    print("---------------------------------------")

def leerArchivo(ruta):
    try:
        with open(ruta,"r")as file:
            return json.load(file)
    except Exception:
        return []
    
def guardarArchivo(ruta,datos):
    with open(ruta,"w")as file:
        json.dump(datos,file,indent=4)
    

def registrarProductos(listaProductos):
    diccionarioProductos = {
        "codigo":input("digite codigo: "),
        "nombre":input("digite nombre: "),
        "precio":input("digite precio: "),
        "iva":input("digite iva: ")
    }
    listaProductos.append(diccionarioProductos)
    guardarArchivo("productos.json",listaProductos)
    return listaProductos
    
def registrarMesas(listaMesas):
    diccionarioMesas = {
        "codigo":input("digite codigo: "),
        "nombre":input("digite nombre: "),
        "puestos":input("digite puestos: "),
    }
    listaMesas.append(diccionarioMesas)
    guardarArchivo("mesas.json",listaMesas)
    return listaMesas

def generarReporteCSV(facturasFiltradas, listaProductos):
    nombre_archivo = "reporte_ventas.csv"
    encabezados = ["Mesa", "Producto", "Cantidad", "Subtotal", "IVA", "Total"]
    
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(encabezados) 

        for factura in facturasFiltradas:
            mesa = factura["codigoMesa"]
            
            for item in factura["productos"]:
                for p in listaProductos:
                    if p["codigo"] == item["codigo"]:
                        precio = float(p["precio"])
                        iva_porc = float(p["iva"])
                        cant = int(item["cantidad"])
                        
                        subtotal = precio * cant
                        iva_valor = subtotal * iva_porc
                        total = subtotal + iva_valor
                        
                        writer.writerow([mesa, p["nombre"], cant, subtotal, iva_valor, total])
    
    print("---------------------------------------")
    print("archivo creado.")
    print("---------------------------------------")

def rankingProductosMenosVendidos(listaFacturas, listaProductos):
    conteo_ranking = []
    
    for p in listaProductos:
        diccionario_auxiliar = {
            "codigo": str(p["codigo"]),
            "vendidos": 0
        }
        conteo_ranking.append(diccionario_auxiliar)

    for factura in listaFacturas:
        for item in factura["productos"]:
            codigo_vendido = str(item["codigo"]) 
            cantidad_vendida = int(item["cantidad"])
            
            for producto_conteo in conteo_ranking:
                if producto_conteo["codigo"] == codigo_vendido:
                    producto_conteo["vendidos"] = producto_conteo["vendidos"] + cantidad_vendida
                    break 

    lista_ordenada = sorted(conteo_ranking, key=lambda x: x["vendidos"])

    print("\n----------5 PRODUCTOS MENOS VENDIDOS ----------")
    contador = 1
    for p in lista_ordenada:
        print(f"{contador}. Código Producto: {p['codigo']}, unidades Vendidas: {p['vendidos']}")
        
        contador = contador + 1
        if contador > 5:
            break
    print("-------------------------------------------------------")
def productos_mas_vendidos(fecha_inicio, fecha_fin):
    listafacturas = leerArchivo("factura.json")
    listaProductos = leerArchivo("productos.json")
    conteo_mas_vendido = []
    facturas_seleccionadas = []
        
    for factura in listafacturas:
            if fecha_inicio <= factura["fecha"] <= fecha_fin:
                facturas_seleccionadas.append(factura)
        
    if len(facturas_seleccionadas) == 0:
            print("No se encontraron facturas en ese rango de fechas.")
    else:
        for p in listaProductos:
            deccionario_auxiliar = {
                "codigo": str(p["codigo"]),
                "nombre": str(p["nombre"]),
                "vendidos": 0
            }
            conteo_mas_vendido.append(deccionario_auxiliar)
        for factura in facturas_seleccionadas:
                for item in factura["productos"]:
                    codigo_vendido = str(item["codigo"])
                    cantidad_vendida = int(item["cantidad"])
                    for producto_conteo in conteo_mas_vendido:
                        if producto_conteo["codigo"] == codigo_vendido:
                            producto_conteo["vendidos"] = producto_conteo["vendidos"] + cantidad_vendida
                        
        lista_con_orden = sorted(conteo_mas_vendido, key=lambda x : x ["vendidos"], reverse=True)
        print("---------------Producto mas vendidos--------------")
        if len(lista_con_orden) > 0:
            a = lista_con_orden[0]
            print(a)
            a["fecha"] = datetime.datetime.now().strftime("%Y-%m-%d")
            global ac
            guardarArchivo(ac, a)
        else:
            print("ERROR")
            return
    #contador = 4
    #for p in lista_con_orden:
    #    print(f"{contador}. Codigo: {p['codigo']}, nombre: {p['nombre']}, vendido {p['vendidos']}")
    #    contador = contador -1
    #    if contador == -1:
    #        break