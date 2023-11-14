import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista para armazenar todos os dados de todas as páginas
dados_totais = []

# Loop através das 34 páginas
for pagina in range(1, 35):
    url = f"https://www.vriconsulting.com.br/trabalhista/grau-risco-rat.php?pagina={pagina}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar a tabela
        table = soup.find('table', {'id': 'grauRiscoTable'})
        if table:
            # Extrair dados diretamente da tabela
            rows = table.find_all('tr')[1:]  # Ignorar a primeira linha (cabeçalho)
            for row in rows:
                columns = row.find_all(['td', 'th'])
                codigo = columns[0].text.strip()
                cnae = columns[1].text.strip()
                descricao = columns[2].text.strip()
                gr = columns[3].text.strip()
                rat = columns[4].text.strip()

                # Adicionar os dados à lista total
                dados_totais.append({'Código': codigo, 'CNAE': cnae, 'Descrição': descricao, 'GR': gr, 'RAT': rat})
        else:
            print(f"Erro: Não foi possível encontrar a tabela na página {pagina}.")
            continue
    else:
        print(f"Erro: Não foi possível acessar a página {pagina}.")
        continue

# Criar um DataFrame do pandas com todos os dados
df = pd.DataFrame(dados_totais)

# Salvar o DataFrame como um arquivo Excel
df.to_excel('dados_extraidos.xlsx', index=False)
