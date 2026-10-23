# Inferential analisis of dengue
By:

Catalina Alvarado Camacho - A01804097

Maria Fernanda González Chávez A01804360

André Julien Rojas - A01804341

Deyan Manuel Ruelas Gómez - A01803785

## Dengue Impact in (fergo)

blah blah blah

## Our questions
How do pre-existing conditions influence dengue susceptibility and clinical outcomes
Was there a difference between the pandemic and post-pandemic periods?

## Data cleaning
Number 1
```
import polars as pl

# 1. Leer forzando ID_REGISTRO como texto
df = pl.read_csv("Todos_los_anos.csv", schema_overrides={"ID_REGISTRO": pl.String})

print("Total filas:", len(df))
print("IDs únicos como String:", df["ID_REGISTRO"].n_unique())

# 2. Probar unicidad combinando 'FECHA_ACTUALIZACION' (o año) con 'ID_REGISTRO'
# Esto verifica si el ID solo se repite porque se reinicia cada año
unicos_con_fecha = df.select(["ID_REGISTRO", "FECHA_ACTUALIZACION"]).n_unique()
print("Combinaciones únicas (ID_REGISTRO + FECHA_ACTUALIZACION):", unicos_con_fecha)

# 3. Inspeccionar algunos duplicados para ver si son exactamente la misma fila
duplicados_ejemplo = df.filter(pl.col("ID_REGISTRO").is_duplicated()).sort("ID_REGISTRO").head(10)
print(duplicados_ejemplo.select(["ID_REGISTRO", "FECHA_ACTUALIZACION", "ESTATUS_CASO", "humedad_relativa", "evap", "fecha", "DICTAMEN"]))
```

Number 2

```
import pandas as pd

# Paso 1: Leer el CSV con la estructura especificada
df_resultados = pd.read_csv('resultado.csv')

# Paso 2 y 3: Procesar los registros
# Usamos un diccionario para mantener el registro más reciente por ID_REGISTRO
registros_unicos = {}

for _, fila in df_resultados.iterrows():
    id_registro = fila['ID_REGISTRO']
    defuncion_actual = fila['DEFUNCION']
    
    # Si el ID no está en el diccionario, lo agregamos
    if id_registro not in registros_unicos:
        registros_unicos[id_registro] = fila
    else:
        # Si ya existe, verificamos si el valor de DEFUNCION es distinto
        defuncion_existente = registros_unicos[id_registro]['DEFUNCION']
        
        if defuncion_actual != defuncion_existente:
            # Reemplazamos por el registro más reciente del loop
            registros_unicos[id_registro] = fila
        # Si no es distinto, no se hace nada (continúa el loop)

# Convertir el resultado procesado a un nuevo DataFrame
df_nuevo = pd.DataFrame(registros_unicos.values())

# Paso 4: Exportar el nuevo DataFrame a nuevo.csv
df_nuevo.to_csv('nuevo.csv', index=False)

print("Proceso completado. Se ha generado 'nuevo.csv' con éxito.")
```
## Hyphotesis proposal
Null Hyphotesis (H0): P1-P2 ≤ 0 (Death proportion during the pandemic was less or equal to that after)
Alternative Hyphotesis (H1): P1-P2 < 0 (Death proportion during the pandemic was greater to that after)

## Hyphotesis test

To evaluate the proposed hypothesis, a Python script was implemented using the pandas, numpy, and statsmodels libraries. A Z-test for the difference between two proportions was performed to compare mortality rates during and after the pandemic. The program automated the calculation of the Z-statistic and the p-value, determining the statistical decision by directly comparing the p-value against a significance level of alpha = 0.05.

```
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

df = pd.read_excel('nuevo2.xlsx')

# Correct format to 
df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y', errors='coerce')


# 2. Definir la fecha de corte (ej. 17 de abril de 2023, fin de emergencia sanitaria por OMS)
fecha_fin_pandemia = pd.to_datetime('2023-04-17')

# 3. Separar los datos en los dos periodos
pandemia = df[df['fecha'] <= fecha_fin_pandemia]
post_pandemia = df[df['fecha'] > fecha_fin_pandemia]

# 4. Calcular el número de muertes (DEFUNCION == 1) y el total de casos por periodo
# Pandemia (P1)
muertes_pandemia = len(pandemia[pandemia['DEFUNCION'] == 1])
n_pandemia = len(pandemia)

# Post-pandemia (P2)
muertes_post = len(post_pandemia[post_pandemia['DEFUNCION'] == 1])
n_post = len(post_pandemia)

# Verificación de seguridad para asegurar que los grupos no estén vacíos
print(f"Total casos pandemia: {n_pandemia} | Defunciones: {muertes_pandemia}")
print(f"Total casos post-pandemia: {n_post} | Defunciones: {muertes_post}\n")

# 5. Realizar la prueba Z para dos proporciones
# Solo ejecuta la prueba si hay datos en ambos grupos
if n_pandemia > 0 and n_post > 0:
    count = np.array([muertes_pandemia, muertes_post])
    nobs = np.array([n_pandemia, n_post])

    # alternative='larger' evalúa H1: P1 - P2 > 0
    stat, pval = proportions_ztest(count, nobs, alternative='larger')

    print(f"Estadístico Z: {stat:.4f}")
    print(f"Valor p (p-value): {pval:.4f}\n")

    if pval < 0.05:
        print("Rechazamos H0: Hay evidencia estadística para afirmar que la mortalidad por dengue fue mayor durante la pandemia.")
    else:
        print("No rechazamos H0: No hay evidencia suficiente para afirmar que la mortalidad fue mayor durante la pandemia en comparación a la post-pandemia.")
else:
    print("Error: Uno de los periodos no tiene datos. Revisa las fechas en la base de datos.")


# 4. Calcular el número de muertes (DEFUNCION == 1) y el total de casos por periodo
# Pandemia (P1)
muertes_pandemia_diabetes = len(pandemia[(pandemia['DEFUNCION'] == 1) & (pandemia['DIABETES'] == 1)])
n_pandemia_diabetes = len(pandemia[pandemia['DIABETES'] == 1])

# Post-pandemia (P2)
muertes_post_diabetes = len(post_pandemia[(post_pandemia['DEFUNCION'] == 1) & (post_pandemia['DIABETES'] == 1)])
n_post_diabetes = len(post_pandemia[post_pandemia['DIABETES'] == 1])

# Verificación de seguridad para asegurar que los grupos no estén vacíos
print(f"Total casos pandemia: {n_pandemia_diabetes} | Defunciones: {muertes_pandemia_diabetes}")
print(f"Total casos post-pandemia: {n_post_diabetes} | Defunciones: {muertes_post_diabetes}\n")

if n_pandemia_diabetes > 0 and n_post_diabetes > 0:
    count = np.array([muertes_pandemia_diabetes, muertes_post_diabetes])
    nobs = np.array([n_pandemia_diabetes, n_post_diabetes])

    # alternative='larger' evalúa H1: P1 - P2 > 0
    stat, pval = proportions_ztest(count, nobs, alternative='larger')

    print(f"Estadístico Z: {stat:.4f}")
    print(f"Valor p (p-value): {pval:.4f}\n")

    if pval < 0.05:
        print("Rechazamos H0: Hay evidencia estadística para afirmar que la mortalidad por dengue fue mayor durante la pandemia.")
    else:
        print("No rechazamos H0: No hay evidencia suficiente para afirmar que la mortalidad fue mayor durante la pandemia en comparación a la post-pandemia.")
else:
    print("Error: Uno de los periodos no tiene datos. Revisa las fechas en la base de datos.") 
```
#### Output

Total pandemic cases: 171502 | Deaths: 669
Total post-pandemic cases: 198347 | Deaths: 1433

Z-statistic: -13.4096
P-value: 1.0000

Fail to reject H0: There is not enough evidence to conclude that dengue mortality was higher during the pandemic than after it.

## Conclusion

Given the result of the hypthotesis test, we fail to reject that during the pandemic the dengue mortality was higher.