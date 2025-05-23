import mysql.connector

def obtener_estudiantes_desde_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TopicosProyectoDB"
        )
        cursor = conexion.cursor()

        consulta = """
        SELECT 
            CONCAT(u.nombre, ' ', u.apellido_paterno, ' ', u.apellido_materno) AS nombre_completo,
            e.matricula,
            u.correo,
            c.nombre AS carrera,
            v.nombre AS voluntariado,
            ve.fecha_participacion,
            ve.horas_aportadas,
            ve.estado_validacion
        FROM Estudiantes e
        JOIN Usuarios u ON e.id_usuario = u.id
        JOIN Carreras c ON e.id_carrera = c.id
        LEFT JOIN Voluntariados_Estudiantes ve ON e.id_usuario = ve.id_estudiante
        LEFT JOIN Voluntariados v ON ve.id_voluntariado = v.id
        WHERE u.status = 1 AND e.status = 1
        ORDER BY u.nombre;
        """
        
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        conexion.close()
        estudiantes = []
        if resultados:
            for fila in resultados:
                fila = list(fila)
                fila[4] = fila[4] if fila[4] else "Sin voluntariado"
                fila[5] = fila[5].strftime("%d/%m/%Y") if fila[5] else "Sin fecha"
                fila[6] = fila[6] if fila[6] is not None else 0
                fila[7] = fila[7] if fila[7] else "Pendiente"
                estudiantes.append(tuple(fila))

        return estudiantes

    except mysql.connector.Error as err:
        print(f"❌ Error al conectar o consultar la base de datos: {err}")
        return []



def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="TopicosProyectoDB"
    )


def obtener_datos_estudiante(matricula):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT u.id AS id_usuario, u.nombre, u.apellido_paterno, u.apellido_materno,
               u.correo, u.telefono, u.fecha_registro, u.usuario, u.password,
               e.matricula, c.id AS id_carrera, c.nombre AS carrera,
               v.id AS id_voluntariado, v.nombre AS voluntariado,
               ve.fecha_participacion, ve.horas_aportadas, ve.estado_validacion
        FROM Estudiantes e
        JOIN Usuarios u ON e.id_usuario = u.id
        JOIN Carreras c ON e.id_carrera = c.id
        LEFT JOIN Voluntariados_Estudiantes ve ON ve.id_estudiante = u.id
        LEFT JOIN Voluntariados v ON ve.id_voluntariado = v.id
        WHERE e.matricula = %s
    """, (matricula,))
    row = cur.fetchone()
    if cur.description is not None and row is not None:
        columns = [desc[0] for desc in cur.description]
        resultado = dict(zip(columns, row))
    else:
        resultado = None
    con.close()
    return resultado

