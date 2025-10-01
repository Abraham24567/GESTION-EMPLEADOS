import json
from datetime import datetime

ARCHIVO = "empleados.json"

# ==============================
# 📌 Estructura base
# ==============================
empleados = []

# Cargar datos al iniciar
def cargar_datos():
    global empleados
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            empleados = json.load(f)
    except FileNotFoundError:
        empleados = []

# Guardar datos al archivo
def guardar_datos():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(empleados, f, indent=4, ensure_ascii=False)

# ==============================
# 🟢 Funciones principales
# ==============================

def registrar_empleado():
    nombre = input("Nombre del empleado: ")
    departamento = input("Departamento: ")
    sueldo = float(input("Sueldo: "))
    fecha_ingreso = input("Fecha de ingreso (YYYY-MM-DD): ")
    ticket = input("Número de ticket: ")
    
    # Calificaciones
    calificaciones = []
    for i in range(5):
        cal = float(input(f"Calificación {i+1}: "))
        calificaciones.append(cal)
    promedio = sum(calificaciones) / len(calificaciones)
    
    # Impuestos
    impuestos = sueldo * 0.10 if sueldo > 3000 else 0
    sueldo_final = sueldo - impuestos

    empleado = {
        "nombre": nombre,
        "departamento": departamento,
        "sueldo": sueldo,
        "impuestos": impuestos,
        "sueldo_final": sueldo_final,
        "fecha_ingreso": fecha_ingreso,
        "ticket": ticket,
        "calificaciones": calificaciones,
        "promedio": promedio
    }
    empleados.append(empleado)
    guardar_datos()
    print(f"✅ Empleado {nombre} registrado correctamente.\n")

def consultar_empleados():
    if not empleados:
        print("⚠️ No hay empleados registrados.")
        return
    print("\n📋 Lista de empleados:")
    for i, emp in enumerate(empleados, start=1):
        print(f"{i}. {emp['nombre']} - {emp['departamento']} - ${emp['sueldo_final']:.2f}")
    print()

def eliminar_empleado():
    consultar_empleados()
    if not empleados:
        return
    try:
        idx = int(input("Número de empleado a eliminar: ")) - 1
        eliminado = empleados.pop(idx)
        guardar_datos()
        print(f"🗑️ Empleado {eliminado['nombre']} eliminado.\n")
    except (ValueError, IndexError):
        print("❌ Opción inválida.\n")

def modificar_empleado():
    consultar_empleados()
    if not empleados:
        return
    try:
        idx = int(input("Número de empleado a modificar: ")) - 1
        emp = empleados[idx]
        print(f"Modificando a {emp['nombre']}...")
        emp['nombre'] = input(f"Nuevo nombre ({emp['nombre']}): ") or emp['nombre']
        emp['departamento'] = input(f"Nuevo departamento ({emp['departamento']}): ") or emp['departamento']
        nuevo_sueldo = input(f"Nuevo sueldo ({emp['sueldo']}): ")
        if nuevo_sueldo:
            emp['sueldo'] = float(nuevo_sueldo)
            emp['impuestos'] = emp['sueldo'] * 0.10 if emp['sueldo'] > 3000 else 0
            emp['sueldo_final'] = emp['sueldo'] - emp['impuestos']
        guardar_datos()
        print("✏️ Empleado modificado correctamente.\n")
    except (ValueError, IndexError):
        print("❌ Opción inválida.\n")

def empleados_de_este_anio():
    anio_actual = datetime.now().year
    encontrados = [e for e in empleados if datetime.strptime(e["fecha_ingreso"], "%Y-%m-%d").year == anio_actual]
    if encontrados:
        print(f"\n👷 Empleados ingresados en {anio_actual}:")
        for e in encontrados:
            print(f"- {e['nombre']} ({e['fecha_ingreso']})")
    else:
        print("⚠️ No hay empleados de este año.")
    print()

def imprimir_ticket():
    consultar_empleados()
    if not empleados:
        return
    try:
        idx = int(input("Número de empleado para imprimir ticket: ")) - 1
        emp = empleados[idx]
        print("\n========== 🧾 TICKET EMPLEADO ==========")
        print(f"Nombre: {emp['nombre']}")
        print(f"Departamento: {emp['departamento']}")
        print(f"Fecha ingreso: {emp['fecha_ingreso']}")
        print(f"Ticket #: {emp['ticket']}")
        print(f"Sueldo bruto: ${emp['sueldo']:.2f}")
        print(f"Impuestos: ${emp['impuestos']:.2f}")
        print(f"Sueldo neto: ${emp['sueldo_final']:.2f}")
        print(f"Promedio calificaciones: {emp['promedio']:.2f}")
        print("========================================\n")
    except (ValueError, IndexError):
        print("❌ Opción inválida.\n")

# ==============================
# 🟡 Menú principal
# ==============================
def menu():
    cargar_datos()
    while True:
        print("========= 🧰 MENÚ EMPLEADOS =========")
        print("1. Registrar empleado")
        print("2. Consultar empleados")
        print("3. Modificar empleado")
        print("4. Eliminar empleado")
        print("5. Empleados de este año")
        print("6. Imprimir ticket")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            consultar_empleados()
        elif opcion == "3":
            modificar_empleado()
        elif opcion == "4":
            eliminar_empleado()
        elif opcion == "5":
            empleados_de_este_anio()
        elif opcion == "6":
            imprimir_ticket()
        elif opcion == "7":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida, intente de nuevo.\n")

# ==============================
# 🚀 Inicio del programa
# ==============================
if __name__ == "__main__":
    menu()