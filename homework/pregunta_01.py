def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    import pandas as pd
    import re
    import os

    # Función para formatear fechas al formato deseado (día/mes/año o año/mes/día)
    def format_date(str_date):
        d = re.search(r'(^\d+)\/(\d+)\/(\d+)', str_date, re.IGNORECASE)  # Extraer partes de la fecha
        day = d.group(1)
        month = d.group(2)
        year = d.group(3)
        if len(day) > 2:  # Si el día tiene más de 2 dígitos, se asume que está en formato año/mes/día
            date = year + '/' + month + '/' + day
            return date
        else:  # Si no, se asume día/mes/año
            date = day + '/' + month + '/' + year
            return date

    # Leer el archivo CSV desde la carpeta de entrada
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    # Eliminar la primera columna innecesaria
    df = df[df.columns[1:]]

    # Eliminar registros duplicados y con valores faltantes
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Convertir todas las columnas de texto a minúsculas
    for i in df.columns:
        try:
            df[i] = df[i].str.lower()
        except:  # Ignorar columnas no textuales
            pass

    # Renombrar columna con caracteres mal codificados
    if "lã­nea_credito" in df.columns:
        df.rename(columns={"lã­nea_credito": "línea_credito"}, inplace=True)

    # Normalizar el texto en la columna "idea_negocio"
    df.idea_negocio = df.idea_negocio.map(lambda x: re.sub("-|_", " ", str(x)))
    df.idea_negocio = df.idea_negocio.str.strip()  # Eliminar espacios extra en los extremos

    # Eliminar caracteres especiales en "monto_del_credito" y convertirlo a tipo numérico
    df.monto_del_credito = df.monto_del_credito.map(lambda x: re.sub("\$|,", "", str(x)))
    df.monto_del_credito = df.monto_del_credito.map(lambda x: float(x))

    # Normalizar el texto en "línea_credito"
    df["línea_credito"] = df["línea_credito"].map(lambda x: re.sub("-|_", " ", str(x)))
    df["línea_credito"] = df["línea_credito"].str.strip()

    # Reemplazar espacios por guiones bajos en la columna "barrio"
    df.barrio = df.barrio.map(lambda x: re.sub("-| ", "_", str(x)))

    # Formatear las fechas en la columna "fecha_de_beneficio"
    df.fecha_de_beneficio = df.fecha_de_beneficio.map(format_date)

    # Eliminar duplicados y valores faltantes nuevamente después de los cambios
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Verificar los valores únicos en "tipo_de_emprendimiento" (opcional)
    df.tipo_de_emprendimiento.unique()

    # Crear la carpeta de salida si no existe
    output_dir = "files/output/"
    os.makedirs(output_dir, exist_ok=True)

    # Guardar el archivo limpio en la carpeta de salida
    df.to_csv("files/output/solicitudes_de_credito.csv", index=False, header=True, sep=";")

    return df

# Ejecutar la función
pregunta_01()
