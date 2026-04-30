import pandas as pd

# 1. Carrega a base discretizada
try:
    df_fca = pd.read_csv('heart_failure_fca_ready.csv')

    lines = []

    # Cabeçalho SLF - formato suportado pelo Lattice Miner
    # IMPORTANTE: sem linhas em branco entre as seções
    # (o parser do Lattice Miner conta linhas em branco como objetos/atributos)
    lines.append("[Lattice]")
    lines.append(str(len(df_fca)))           # número de objetos
    lines.append(str(len(df_fca.columns)))   # número de atributos

    lines.append("[Objects]")
    for i in range(len(df_fca)):
        lines.append(f"P{i}")

    lines.append("[Attributes]")
    for col in df_fca.columns:
        lines.append(col)

    # Matriz de incidência: 0s e 1s separados por espaço, uma linha por objeto
    lines.append("[Relation]")
    for _, row in df_fca.iterrows():
        lines.append(" ".join(str(int(v)) for v in row))

    # Escreve com quebras de linha Unix (\n), sem \r
    # newline='' impede que o Python converta \n para \r\n no Windows
    content = "\n".join(lines) + "\n"
    with open('coracao_contexto.slf', 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print("Arquivo 'coracao_contexto.slf' gerado com sucesso!")
    print("Abra no Lattice Miner via File > Open Context e selecione o .slf")

except Exception as e:
    print(f"Erro ao gerar o arquivo: {e}")
