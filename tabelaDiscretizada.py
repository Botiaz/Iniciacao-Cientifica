import pandas as pd

# Carregar os dados
df = pd.read_csv('heart_failure_clinical_records_dataset.csv')

# 1. Remover a coluna 'time'
df = df.drop(columns=['time'])

# 2. Criar colunas para Sex (Masculine / Feminine)
df['is_masculine'] = df['sex'].apply(lambda x: 1 if x == 1 else 0)
df['is_feminine'] = df['sex'].apply(lambda x: 1 if x == 0 else 0)
df = df.drop(columns=['sex'])

# 3. Discretização baseada nos seus critérios
df_fca = pd.DataFrame()

# Idade (Elderly 60+)
df_fca['elderly'] = df['age'].apply(lambda x: 1 if x >= 60 else 0)

# Anemia (já binário)
df_fca['anaemia'] = df['anaemia']

# CPK (Ruim se > 190)
df_fca['high_cpk'] = df['creatinine_phosphokinase'].apply(lambda x: 1 if x > 190 else 0)

# Diabetes (já binário)
df_fca['diabetes'] = df['diabetes']

# Ejection Fraction (Bom se entre 50 e 70, caso contrário 'abnormal')
# Para FCA, geralmente focamos no que é "ruim" para encontrar padrões de risco
df_fca['abnormal_ejection_fraction'] = df['ejection_fraction'].apply(lambda x: 0 if 50 <= x <= 70 else 1)

# High Blood Pressure (já binário)
df_fca['high_blood_pressure'] = df['high_blood_pressure']

# Platelets (Ruim se fora da faixa 150k - 450k)
df_fca['abnormal_platelets'] = df['platelets'].apply(lambda x: 1 if x < 150000 or x > 450000 else 0)

# Serum Creatinine (Ruim se > 1.2)
df_fca['high_serum_creatinine'] = df['serum_creatinine'].apply(lambda x: 1 if x > 1.2 else 0)

# Serum Sodium (Ruim se < 135 - Hiponatremia)
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