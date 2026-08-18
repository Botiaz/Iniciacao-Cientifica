import pandas as pd

# Carregar os dados
df = pd.read_csv('heart_failure_clinical_records_dataset.csv')

# 1. Remover a coluna 'time'
df = df.drop(columns=['time'])

# 2. Criar colunas para Sex
# No dataset: 0 = feminino, 1 = masculino
df['is_masculine'] = df['sex'].apply(lambda x: 1 if x == 1 else 0)
df['is_feminine'] = df['sex'].apply(lambda x: 1 if x == 0 else 0)

# 3. Discretização baseada em critérios clínicos
df_fca = pd.DataFrame()

# ============================================================
# AGE
# Idoso: >= 60 anos
# Fonte: World Health Organization (WHO)
# ============================================================
df_fca['elderly'] = df['age'].apply(
    lambda x: 1 if x >= 60 else 0
)

# ============================================================
# ANAEMIA
# Já é uma variável binária no dataset
# ============================================================
df_fca['anaemia'] = df['anaemia']

# ============================================================
# CPK (Creatine Phosphokinase)
# Intervalo de referência adotado: 10–120 mcg/L
# Fonte: MedlinePlus
#
# O dataset original não fornece um limite de normalidade
# para CPK. Portanto, >120 mcg/L é adotado neste trabalho
# como critério operacional para CPK elevada.
# ============================================================
df_fca['high_cpk'] = df['creatinine_phosphokinase'].apply(
    lambda x: 1 if x > 120 else 0
)

# ============================================================
# DIABETES
# Já é uma variável binária no dataset
# ============================================================
df_fca['diabetes'] = df['diabetes']

# ============================================================
# EJECTION FRACTION
# Faixa normal adotada: 55–70%
# Fonte: American Heart Association (AHA)
#
# 0 = dentro da faixa normal
# 1 = fora da faixa normal
# ============================================================
df_fca['abnormal_ejection_fraction'] = df['ejection_fraction'].apply(
    lambda x: 0 if 55 <= x <= 70 else 1
)

# ============================================================
# HIGH BLOOD PRESSURE
# Já é uma variável binária no dataset
# ============================================================
df_fca['high_blood_pressure'] = df['high_blood_pressure']

# ============================================================
# PLATELETS
# Faixa de referência: 150,000–400,000 / µL
# Fonte: MedlinePlus
#
# 0 = dentro da faixa de referência
# 1 = fora da faixa de referência
# ============================================================
df_fca['abnormal_platelets'] = df['platelets'].apply(
    lambda x: 1 if x < 150000 or x > 400000 else 0
)

# ============================================================
# SERUM CREATININE
# Fonte: MedlinePlus
#
# Homens: 0.7–1.3 mg/dL
# Mulheres: 0.5–0.95 mg/dL
#
# A variável identifica especificamente creatinina elevada.
# ============================================================
df_fca['high_serum_creatinine'] = df.apply(
    lambda row: 1 if (
        (row['sex'] == 1 and row['serum_creatinine'] > 1.3) or
        (row['sex'] == 0 and row['serum_creatinine'] > 0.95)
    ) else 0,
    axis=1
)

# ============================================================
# SERUM SODIUM
# Hiponatremia: <135 mEq/L
# Fonte: MedlinePlus
#
# A variável identifica especificamente sódio baixo.
# ============================================================
df_fca['low_serum_sodium'] = df['serum_sodium'].apply(
    lambda x: 1 if x < 135 else 0
)

# ============================================================
# SMOKING
# Já é uma variável binária no dataset
# ============================================================
df_fca['smoking'] = df['smoking']

# ============================================================
# SEX
# 1 = masculino
# 0 = feminino
# ============================================================
df_fca['masculine'] = df['is_masculine']
df_fca['feminine'] = df['is_feminine']

# ============================================================
# TARGET
# 1 = morte durante o período de acompanhamento
# 0 = sobrevivência durante o período de acompanhamento
# ============================================================
df_fca['death_event'] = df['DEATH_EVENT']

# Salvar a base discretizada
df_fca.to_csv('heart_failure_fca_ready.csv', index=False)

print("Base discretizada com sucesso!")
print(df_fca.head())