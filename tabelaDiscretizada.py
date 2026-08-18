import pandas as pd

# Carregar os dados
df = pd.read_csv('heart_failure_clinical_records_dataset.csv')

# 1. Remover a coluna 'time'
df = df.drop(columns=['time'])

# 2. Criar colunas para Sex (Masculine / Feminine)
df['is_masculine'] = df['sex'].apply(lambda x: 1 if x == 1 else 0)
df['is_feminine'] = df['sex'].apply(lambda x: 1 if x == 0 else 0)

# 3. Discretização baseada nos critérios clínicos (fontes: MedlinePlus)
df_fca = pd.DataFrame()

# Idade (Elderly 60+)
# Fonte: convenção clínica usual para "idoso" em estudos cardiovasculares
df_fca['elderly'] = df['age'].apply(lambda x: 1 if x >= 60 else 0)

# Anemia (já binário)
df_fca['anaemia'] = df['anaemia']

# CPK (Creatinine Phosphokinase)
# Fonte: MedlinePlus (ency/article/003503) - normal = 10-120 mcg/L
df_fca['high_cpk'] = df['creatinine_phosphokinase'].apply(lambda x: 1 if x > 120 else 0)

# Diabetes (já binário)
df_fca['diabetes'] = df['diabetes']

# Ejection Fraction (Bom se entre 55 e 70, caso contrário 'abnormal')
# Fonte: Heart.org - LVEF normal = 55-70%
df_fca['abnormal_ejection_fraction'] = df['ejection_fraction'].apply(lambda x: 0 if 55 <= x <= 70 else 1)

# High Blood Pressure (já binário)
df_fca['high_blood_pressure'] = df['high_blood_pressure']

# Platelets (Ruim se fora da faixa 150k - 400k)
# Fonte: MedlinePlus (ency/article/003647) - normal = 150.000-400.000/mcL
df_fca['abnormal_platelets'] = df['platelets'].apply(lambda x: 1 if x < 150000 or x > 400000 else 0)

# Serum Creatinine (Ruim se fora da faixa normal *dependente do sexo*)
# Fonte: MedlinePlus (ency/article/003475)
#   Homens : 0.7 - 1.3 mg/dL  -> anormal se > 1.3
#   Mulheres: 0.5 - 0.95 mg/dL -> anormal se > 0.95
df_fca['high_serum_creatinine'] = df.apply(
    lambda row: 1 if (
        (row['sex'] == 1 and row['serum_creatinine'] > 1.3) or   # homem
        (row['sex'] == 0 and row['serum_creatinine'] > 0.95)     # mulher
    ) else 0,
    axis=1
)

# Serum Sodium (Ruim se < 135 - Hiponatremia)
# Fonte: MedlinePlus (ency/article/003481) - normal = 135-145 mEq/L
df_fca['low_serum_sodium'] = df['serum_sodium'].apply(lambda x: 1 if x < 135 else 0)

# Smoking (já binário)
df_fca['smoking'] = df['smoking']

# Sexo (usando as novas colunas)
df_fca['masculine'] = df['is_masculine']
df_fca['feminine'] = df['is_feminine']

# Variável Alvo: Morte
df_fca['death_event'] = df['DEATH_EVENT']

# Salvar para o seu trabalho
df_fca.to_csv('heart_failure_fca_ready.csv', index=False)

print("Base discretizada com sucesso!")
print(df_fca.head())

# Resumo de quantos pacientes mudaram de classificação em relação ao
# algoritmo anterior (útil para citar no artigo, seção de metodologia)
old_creat = (df['serum_creatinine'] > 1.2).astype(int)
new_creat = df_fca['high_serum_creatinine']
old_plt = ((df['platelets'] < 150000) | (df['platelets'] > 450000)).astype(int)
new_plt = df_fca['abnormal_platelets']
old_cpk = (df['creatinine_phosphokinase'] > 190).astype(int)
new_cpk = df_fca['high_cpk']

print(f"\nPacientes reclassificados em high_serum_creatinine: {(old_creat != new_creat).sum()} / {len(df)}")
print(f"Pacientes reclassificados em abnormal_platelets: {(old_plt != new_plt).sum()} / {len(df)}")
print(f"Pacientes reclassificados em high_cpk: {(old_cpk != new_cpk).sum()} / {len(df)}")
