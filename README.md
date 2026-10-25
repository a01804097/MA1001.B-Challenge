# Inferential analisis of dengue
By:

Catalina Alvarado Camacho - A01804097

Maria Fernanda González Chávez A01804360

André Julien Rojas - A01804341

Deyan Manuel Ruelas Gómez - A01803785

## Dengue Impact in Mexico

Dengue is a major public health concern in Mexico, which is a hyperendemic country . Many people also live with chronic health conditions that may influence how the disease develops. In addition, the pandemic period changed how health services operated and how cases were detected ad registered. Studying these factors together can help understand who is most at risk and improve prevention and clinical care.

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

# Convert dates to the correct format
df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y', errors='coerce')

# Set the date that separates the two periods
pandemic_end_date = pd.to_datetime('2023-04-17')

# Split the data into two periods
pandemia = df[df['fecha'] <= pandemic_end_date]
post_pandemia = df[df['fecha'] > pandemic_end_date]

# Count deaths and total cases in each period
# Pandemic
muertes_pandemia = len(pandemia[pandemia['DEFUNCION'] == 1])
n_pandemia = len(pandemia)

# Post-pandemic
muertes_post = len(post_pandemia[post_pandemia['DEFUNCION'] == 1])
n_post = len(post_pandemia)

# Check the number of cases and deaths
print(f"Total pandemic cases: {n_pandemia} | Deaths: {muertes_pandemia}")
print(f"Total post-pandemic cases: {n_post} | Deaths: {muertes_post}\n")

# Run the two-proportion Z-test
if n_pandemia > 0 and n_post > 0:
    count = np.array([muertes_pandemia, muertes_post])
    nobs = np.array([n_pandemia, n_post])

    # Test whether the death rate was higher during the pandemic
    stat, pval = proportions_ztest(count, nobs, alternative='larger')

    print(f"Z-statistic: {stat:.4f}")
    print(f"P-value: {pval:.4f}\n")

    if pval < 0.05:
        print("Reject H0: There is statistical evidence that dengue mortality was higher during the pandemic.")
    else:
        print("Fail to reject H0: There is not enough evidence to conclude that dengue mortality was higher during the pandemic than after it.")
else:
    print("Error: One of the periods has no data. Check the dates in the dataset.")


# Count deaths and total diabetes cases in each period
# Pandemic
muertes_pandemia_diabetes = len(
    pandemia[(pandemia['DEFUNCION'] == 1) & (pandemia['DIABETES'] == 1)]
)
n_pandemia_diabetes = len(pandemia[pandemia['DIABETES'] == 1])

# Post-pandemic
muertes_post_diabetes = len(
    post_pandemia[(post_pandemia['DEFUNCION'] == 1) & (post_pandemia['DIABETES'] == 1)]
)
n_post_diabetes = len(post_pandemia[post_pandemia['DIABETES'] == 1])

# Check the number of cases and deaths among patients with diabetes
print(f"Total pandemic cases with diabetes: {n_pandemia_diabetes} | Deaths: {muertes_pandemia_diabetes}")
print(f"Total post-pandemic cases with diabetes: {n_post_diabetes} | Deaths: {muertes_post_diabetes}\n")

# Run the two-proportion Z-test
if n_pandemia_diabetes > 0 and n_post_diabetes > 0:
    count = np.array([muertes_pandemia_diabetes, muertes_post_diabetes])
    nobs = np.array([n_pandemia_diabetes, n_post_diabetes])

    # Test whether the death rate was higher during the pandemic
    stat, pval = proportions_ztest(count, nobs, alternative='larger')

    print(f"Z-statistic: {stat:.4f}")
    print(f"P-value: {pval:.4f}\n")

    if pval < 0.05:
        print("Reject H0: There is statistical evidence that dengue mortality among patients with diabetes was higher during the pandemic.")
    else:
        print("Fail to reject H0: There is not enough evidence to conclude that dengue mortality among patients with diabetes was higher during the pandemic than after it.")
else:
    print("Error: One of the periods has no data. Check the dates in the dataset.")
```
#### Output

Total pandemic cases: 171502 | Deaths: 669

Total post-pandemic cases: 198347 | Deaths: 1433

Z-statistic: -13.4096
P-value: 1.0000

Fail to reject H0: There is not enough evidence to conclude that dengue mortality was higher during the pandemic than after it.

## Conclusion

Since the null hyphotesis (H0) was not rejected,there is not enough statistical evidence to conclude that dengue mortality was higher during the pandemic than in the post-pandemic period. Although the data may suggest that there were fewer deaths from dengue during the pandemic, it is important to consider that some of these cases might have been misdiagnosed. Since dengue and COVID-19 share similar symptoms, some patients may have been diagnosed with COVID-19 without being tested for dengue. Furthermore, the original dataset did not include information about COVID-19 cases or possible misdiagnoses during the pandemic years, so there is no certainty that results weren't affected. Therefore, even though the data shows a possible difference in mortality between the two periods, there is some uncertainty in this. 