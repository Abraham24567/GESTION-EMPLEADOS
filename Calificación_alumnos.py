def registrar_alumno():
    nombre = input("Ingresa el nombre del alumno: ")
    calificaciones = []
    
    for i in range(5):  # Pedimos 5 calificaciones
        while True:
            try:
                nota = float(input(f"Ingresa la calificación {i+1} (0-100): "))
                if 0 <= nota <= 100:
                    calificaciones.append(nota)
                    break
                else:
                    print("La calificación debe estar entre 0 y 100.")
            except ValueError:
                print("Ingresa un número válido.")
    
    promedio = sum(calificaciones) / len(calificaciones)
    print(f"\nAlumno: {nombre}")
    print(f"Calificaciones: {calificaciones}")
    print(f"Promedio: {promedio:.2f}")
    if promedio >= 60:
        print("Resultado: Aprobado ✅\n")
    else:
        print("Resultado: Reprobado ❌\n")
    
    return {"nombre": nombre, "calificaciones": calificaciones, "promedio": promedio}

def main():
    alumnos = []
    while True:
        print("----- Menú -----")
        print("1. Agregar alumno")
        print("2. Mostrar todos los alumnos")
        print("3. Salir")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            alumno = registrar_alumno()
            alumnos.append(alumno)
        elif opcion == "2":
            if alumnos:
                for a in alumnos:
                    print(f"Alumno: {a['nombre']}, Promedio: {a['promedio']:.2f}, Calificaciones: {a['calificaciones']}")
                print()
            else:
                print("No hay alumnos registrados.\n")
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intenta de nuevo.\n")

if __name__ == "__main__":
    main()