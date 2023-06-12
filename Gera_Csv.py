# importando as bibliotecas
# Requests será para comunicar com a API dos dadosabertos
# Pandas será para criar nosso dataframe e depois salvar em csv os dados da API
# datetime será para pegar a última data e hora da geração do csv
import requests
import pandas as pd
from datetime import datetime

########### Primeira parte para coletar os dados gerais dos Deputados ########################

# Endereço da API
url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'

# Realizando GET da api para coletar os dados
response = requests.get(url).json()

# Criando uma matriz para guardar os dados desejados
lista_deputados = []

# Uma iteração que realiza o input linha a linha do retorno da API para a variável lista_deputados
for deputado in response['dados']:
  lista_deputados.append([deputado['id'], 
                          deputado['nome'], 
                          deputado['siglaPartido'],
                          deputado['siglaUf'],
                          deputado['urlFoto'], 
                          deputado['email']])

#Criando o dataframe com a lista criada anteriormente
deputados_df = pd.DataFrame(data = lista_deputados, columns = ['id','nome','siglaPartido','siglaUf','urlFoto', 'email'])

########### Aqui está criado e pronto para ser convertido para CSV nossos dados dos Deputados Gerais

########### Segunda parte para coletar os dados de informação de cada Deputado ########################

# Criando uma matriz para guardar os dados desejados
lista_deputados_info = []

# Contador que será usado para exibir no console quantidade de deputado já retornado
count = 0

# Iteração realizada para cada deputado que foi extraído na primeira chamada
for deputado in response['dados']:
  
  count += 1
  
  # Para cada 10 chamada, realizar um print para conferir onde está
  if(count == 1):
    print(str(count) + ' dados carregados')
  elif(count%10 == 0 ):
    print(str(count) + ' dados carregados')
  if(count == len(lista_deputados)): 
    print(str(count) + ' dados carregados')
    print(' ------- Último dado carregado ------- ')
  #Url com o id do deputado
  url_deputado_info = 'https://dadosabertos.camara.leg.br/api/v2/deputados/' + str(deputado.get('id'))

  # Realizando GET da api para coletar os dados
  response_2 = requests.get(url_deputado_info).json()

  # Criação da lista que será transformada em DataFrame
  lista_deputados_info.append([response_2['dados'].get('id'),
                               response_2['dados'].get('cpf'),
                               response_2['dados'].get('sexo'),
                               response_2['dados'].get('dataNascimento'),
                               response_2['dados'].get('dataFalecimento'),
                               response_2['dados'].get('escolaridade'),
                               response_2['dados']['ultimoStatus'].get('situacao'),
                               response_2['dados']['ultimoStatus'].get('condicaoEleitoral'),
                               response_2['dados']['ultimoStatus'].get('data')
  ])
  
  #Para fins de teste
  #if (count == 10): break

#Criando o dataframe com a lista criada anteriormente
deputados_info_df = pd.DataFrame(data = lista_deputados_info, columns = ['id','cpf','sexo','dataNascimento','dataFalecimento','escolaridade', 'situacao', 'condicaoEleitoral', 'data'])

#Transformação da tabela:
deputados_info_df.loc[deputados_info_df["sexo"] == "M", "sexo"] = 'Masculino'
deputados_info_df.loc[deputados_info_df["sexo"] == "F", "sexo"] = 'Feminino'
deputados_info_df.loc[deputados_info_df["escolaridade"] == "", "escolaridade"] = 'Não informado'
deputados_info_df["escolaridade"].fillna("Não informado", inplace=True)

########### Aqui está criado e pronto para ser convertido para CSV nossos dados dos Deputados Gerais

########### Terceira parte gerar o csv dos dados dos deputados ########################

#Salvando os dataframe em csv
deputados_df.to_csv(r'C:\Users\Leandro\OneDrive\Área de Trabalho\Deputados\Deputados_Gerais.csv',";",encoding='utf-8-sig',index=False)
deputados_info_df.to_csv(r'C:\Users\Leandro\OneDrive\Área de Trabalho\Deputados\Deputados_info.csv',";",encoding='utf-8-sig', index=False)

########### Quarta parte gerar o csv da data e hora que foi gerado o csv ########################

now = datetime.now()

datetime_df = pd.DataFrame(data = {now.strftime("%d/%m/%Y")}, columns = ['DateTime'])

datetime_df.to_csv(r'C:\Users\Leandro\OneDrive\Área de Trabalho\Deputados\Data_Geracao.csv',";",encoding='utf-8-sig', index=False)

print('Sucesso')