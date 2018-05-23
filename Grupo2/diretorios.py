
# coding: utf-8

# ### IMPORTS

# In[1]:


import pandas as pd
import os
import xlrd


# ### FUNÇÕES

# In[2]:


#CRIA COLUNAS NOS DATAFRAMES COM O NOME PASSADO NO PARAMETRO
def create_column(df,nm):
    df[f'{nm}']=[]


# In[3]:


# LEITURA DE ARQUIVO EXCEL RETORNANDO COMO DATAFRAME A ABA [0]
def le_excel(file):
    return pd.ExcelFile(file).parse(pd.ExcelFile(file).sheet_names[0])


# ### CAMINHO DO ARQUIVO

# In[4]:


#CAMINHO
path="//Excel"


# ### DATAFRAMES NECESSÁRIOS

# In[5]:


#DATAFRAMES:
df1 = pd.DataFrame({})
tabela_unica = pd.DataFrame({})


# ## SCRIPT

# In[6]:


#cria as colunas no dataframe1:
create_column(df1,'Licitações')
create_column(df1,'Lotes')


# In[7]:


#le a pasta path e obtem o nome das pastas das licitações como uma string
arr_licitacoes=os.listdir(path)


# In[8]:


#lê cada pasta de licitações e obtem os lotes como strings
arr_lotes=[]
for diretorio in arr_licitacoes:
    arr_lotes+=[os.listdir(f'{path}//{diretorio}')]


# ### GRAVA NO DATAFRAME1 OS NOMES DE LICITAÇÕES E LOTES

# In[9]:


for i in range(len(arr_licitacoes)):
	if arr_licitacoes[i] in list(df1.Licitações):
		continue
	for k in range(len(arr_lotes[i])):
		df1 = df1.append({'Licitações':arr_licitacoes[i],'Lotes':arr_lotes[i][k]}, ignore_index=True)


# In[10]:


# SAIDA DO DATAFRAME 1 | CONTEM TODAS AS PASTAS E LOTES COMO UM INDICE QUE SERA USADO DEPOIS
df1


# ### CRIA AS COLUNAS NA TABELA_UNICA BASEADO NUME PRIMEIRA LEITURA DO PRIMEIRO LOTE

# In[11]:


lote = le_excel(f'{path}//{df1.Licitações[0]}//{df1.Lotes[0]}')


# In[12]:


for nm in df1.columns:
    create_column(tabela_unica,nm)

for nm in lote.columns:
    create_column(tabela_unica,nm)


# ### ABRE CADA LOTE DO FORMATO EXCEL E COPIA AS LINHAS DO LOTE PARA A TABELA UNICA

# In[13]:

for i in range(len(df1)):
	if df1.Licitações[i] in list(tabela_unica.Licitações):
		continue
	lote = le_excel(f'{path}//{df1.Licitações[i]}//{df1.Lotes[i]}')
	for k in range(len(lote)):
        	tabela_unica = tabela_unica.append({'Licitações':df1.Licitações[i],'Lotes':df1.Lotes[i],'Item':lote.Item[k],'Descrição':lote.Descrição[k],'Quantidade':lote.Quantidade[k],'Mercadoria':lote.Mercadoria[k]},ignore_index=True)


# In[14]:


tabela_unica

writer = pd.ExcelWriter('tabela_unica.xlsx', engine = 'xlsxwriter')

tabela_unica.to_excel(writer, sheet_name='Sheet1')

writer.save()

