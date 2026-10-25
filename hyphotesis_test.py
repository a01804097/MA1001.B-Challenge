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