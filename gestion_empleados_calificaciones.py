import json
import os
import datetime
import uuid
from typing import List, Dict, Any

DB_FILE = "employees.json"
TAX_THRESHOLD = 3000.0
TAX_RATE = 0.10  # 10% por defecto


def cargar_datos() -> Dict[str, Any]:
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def guardar_datos(data: Dict[str, Any]) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def generar_ticket() -> str:
    return str(uuid.uuid4())[:8]


def pedir_fecha(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        try:
            datetime.datetime.strptime(s, "%Y-%m-%d")
            return s
        except Exception:
            print("Fecha inválida. Usa formato YYYY-MM-DD.")


def pedir_float(prompt: str, allow_empty=False) -> float:
    while True:
        s = input(prompt).strip()
        if allow_empty and s == "":
            return 0.0
        try:
            return float(s)
        except Exception:
            print("Ingresa un número válido.")


def pedir_calificaciones() -> List[float]:
    grades = []
    print("Ingresa 5 calificaciones (0-100):")
    for i in range(1, 6):
        while True:
            s = input(f"  Calificación {i}: ").strip()
            try:
                g = float(s)
                if 0 <= g <= 100:
                    grades.append(g)
                    break
                else:
                    print("La calificación debe estar entre 0 y 100.")
            except Exception:
                print("Ingresa un número válido.")
    return grades


def calcular_promedio(grades: List[float]) -> float:
    if not grades:
        return 0.0
    return round(sum(grades) / len(grades), 2)


def calcula_impuesto(salario: float) -> Dict[str, float]:
    if salario > TAX_THRESHOLD:
        impuesto = round(salario * TAX_RATE, 2)
        neto = round(salario - impuesto, 2)
        return {"aplica": True, "impuesto": impuesto, "neto": neto}
    else:
        return {"aplica": False, "impuesto": 0.0, "neto": salario}


# ---------- Operaciones CRUD ----------


def registrar_empleado(data: Dict[str, Any]) -> None:
    ticket = generar_ticket()
    nombre = input("Nombre completo: ").strip()
    departamento = input("Departamento: ").strip()
    fecha_ingreso = pedir_fecha("Fecha de ingreso (YYYY-MM-DD): ")
    salario = pedir_float("Salario mensual: ")
    calificaciones = pedir_calificaciones()
    promedio = calcular_promedio(calificaciones)
    impuestos = calcula_impuesto(salario)

    empleado = {
        "ticket": ticket,
        "nombre": nombre,
        "departamento": departamento,
        "fecha_ingreso": fecha_ingreso,
        "salario": salario,
        "calificaciones": calificaciones,
        "promedio": promedio,
        "impuestos": impuestos,
    }
    data[ticket] = empleado
    guardar_datos(data)
    print(f"Empleado registrado con ticket: {ticket}")


def modificar_empleado(data: Dict[str, Any]) -> None:
    ticket = input("Ticket del empleado a modificar: ").strip()
    if ticket not in data:
        print("No existe un empleado con ese ticket.")
        return
    emp = data[ticket]
    print("Deja vacío para mantener el valor actual.")
    nombre = input(f"Nombre [{emp['nombre']}]: ").strip() or emp["nombre"]
    departamento = input(f"Departamento [{emp['departamento']}]: ").strip() or emp["departamento"]
    fecha_ingreso = input(f"Fecha de ingreso [{emp['fecha_ingreso']}]: ").strip() or emp["fecha_ingreso"]
    # validamos fecha
    try:
        datetime.datetime.strptime(fecha_ingreso, "%Y-%m-%d")
    except Exception:
        print("Fecha inválida. Se mantiene la original.")
        fecha_ingreso = emp["fecha_ingreso"]
    salario_input = input(f"Salario [{emp['salario']}]: ").strip()
    salario = emp["salario"]
    if salario_input:
        try:
            salario = float(salario_input)
        except Exception:
            print("Salario inválido. Se mantiene el original.")
    cambiar_notas = input("¿Deseas modificar las 5 calificaciones? (s/n): ").strip().lower()
    calificaciones = emp["calificaciones"]
    if cambiar_notas == "s":
        calificaciones = pedir_calificaciones()
    promedio = calcular_promedio(calificaciones)
    impuestos = calcula_impuesto(salario)

    emp.update({
        "nombre": nombre,
        "departamento": departamento,
        "fecha_ingreso": fecha_ingreso,
        "salario": salario,
        "calificaciones": calificaciones,
        "promedio": promedio,
        "impuestos": impuestos,
    })
    guardar_datos(data)
    print("Empleado modificado correctamente.")


def eliminar_empleado(data: Dict[str, Any]) -> None:
    ticket = input("Ticket del empleado a eliminar: ").strip()
    if ticket not in data:
        print("No existe un empleado con ese ticket.")
        return
    confirm = input("¿Seguro que deseas eliminar? (s/n): ").strip().lower()
    if confirm == "s":
        del data[ticket]
        guardar_datos(data)
        print("Empleado eliminado.")
    else:
        print("Operación cancelada.")


def consultar_empleado(data: Dict[str, Any]) -> None:
    ticket = input("Ticket del empleado a consultar: ").strip()
    if ticket not in data:
        print("No existe un empleado con ese ticket.")
        return
    emp = data[ticket]
    imprimir_ticket(emp)


def listar_empleados(data: Dict[str, Any]) -> None:
    if not data:
        print("No hay empleados registrados.")
        return
    print("Listado de empleados:")
    for t, emp in data.items():
        print(f"- Ticket: {t} | Nombre: {emp['nombre']} | Dept: {emp['departamento']} | Promedio: {emp['promedio']}")


# ---------- Funciones adicionales ----------


def empleados_de_este_anyo(data: Dict[str, Any]) -> None:
    year = datetime.date.today().year
    encontrados = []
    for emp in data.values():
        try:
            y = datetime.datetime.strptime(emp["fecha_ingreso"], "%Y-%m-%d").year
            if y == year:
                encontrados.append(emp)
        except Exception:
            continue
    if not encontrados:
        print(f"No se encontraron empleados con fecha de ingreso en {year}.")
        return
    print(f"Empleados ingresados en {year}:")
    for emp in encontrados:
        print(f"- {emp['ticket']} | {emp['nombre']} | {emp['departamento']} | {emp['fecha_ingreso']}")


def imprimir_ticket(emp: Dict[str, Any]) -> None:
    print("\n" + "=" * 40)
    print("TICKET DE EMPLEADO")
    print("=" * 40)
    print(f"Ticket ID: {emp['ticket']}")
    print(f"Nombre: {emp['nombre']}")
    print(f"Departamento: {emp['departamento']}")
    print(f"Fecha de ingreso: {emp['fecha_ingreso']}")
    print(f"Salario bruto: {emp['salario']}")
    if emp.get("impuestos", {}).get("aplica"):
        print(f"Impuesto aplicado: {emp['impuestos']['impuesto']}")
        print(f"Salario neto: {emp['impuestos']['neto']}")
    else:
        print("No aplica impuesto")
    print("Calificaciones:")
    for i, g in enumerate(emp.get("calificaciones", []), 1):
        print(f"  {i}: {g}")
    print(f"Promedio: {emp.get('promedio', 0.0)}")
    print("=" * 40 + "\n")


def exportar_json(data: Dict[str, Any]) -> None:
    path = input("Nombre archivo exportado (por defecto export_empleados.json): ").strip() or "export_empleados.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Datos exportados a {path}")


def importar_json(data: Dict[str, Any]) -> None:
    path = input("Ruta del archivo JSON a importar: ").strip()
    if not os.path.exists(path):
        print("Archivo no encontrado.")
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            newdata = json.load(f)
        # sobrescribir o fusionar?
        choice = input("Deseas (s)obrescribir la DB o (m)ezclar?: (s/m): ").strip().lower()
        if choice == "s":
            guardar_datos(newdata)
            print("Base de datos sobrescrita.")
        else:
            data.update(newdata)
            guardar_datos(data)
            print("Datos importados y fusionados.")
    except Exception as e:
        print("Error leyendo JSON:", e)


def mostrar_menu_principal() -> None:
    print("\n=== GESTIÓN EMPLEADOS Y CALIFICACIONES ===")
    print("1. Registrar empleado")
    print("2. Modificar empleado")
    print("3. Eliminar empleado")
    print("4. Consultar empleado (por ticket)")
    print("5. Listar empleados")
    print("6. Empleados ingresados este año")
    print("7. Imprimir ticket (por ticket)")
    print("8. Exportar a JSON")
    print("9. Importar desde JSON")
    print("10. Crear scripts para Git (mostrar comandos)")
    print("0. Salir")


def mostrar_git_instructions() -> None:
    print("\nInstrucciones rápidas para crear un repositorio Git y un script bash:")
    print("1) Inicializar localmente y hacer primer commit:")
    print("   git init")
    print("   git add .")
    print("   git commit -m \"Inicial commit: gestión empleados\"")
    print("2) Crear repo en GitHub (puedes usar la web) y luego enlazar:")
    print("   git remote add origin https://github.com/tu_usuario/tu_repo.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\nSi usas Git Bash o Termux, estos mismos comandos funcionan.")
    print("Puedes crear un archivo init_git.sh con estos comandos para ejecutarlo en bash.")


def buscar_y_imprimir_ticket(data: Dict[str, Any]) -> None:
    ticket = input("Ticket del empleado a imprimir: ").strip()
    emp = data.get(ticket)
    if not emp:
        print("No encontrado.")
        return
    imprimir_ticket(emp)


def main():
    data = cargar_datos()
    while True:
        mostrar_menu_principal()
        opt = input("Elige una opción: ").strip()
        if opt == "1":
            registrar_empleado(data)
        elif opt == "2":
            modificar_empleado(data)
        elif opt == "3":
            eliminar_empleado(data)
        elif opt == "4":
            consultar_empleado(data)
        elif opt == "5":
            listar_empleados(data)
        elif opt == "6":
            empleados_de_este_anyo(data)
        elif opt == "7":
            buscar_y_imprimir_ticket(data)
        elif opt == "8":
            exportar_json(data)
        elif opt == "9":
            importar_json(data)
        elif opt == "10":
            mostrar_git_instructions()
        elif opt == "0":
            print("Saliendo. ¡Hasta luego!")
            break
        else:
            print("Opción no reconocida. Intenta de nuevo.")


if __name__ == "__main__":
    main()