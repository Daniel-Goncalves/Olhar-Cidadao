import pandas as pd

dfs = pd.read_excel("x0.xlsx", sheet_name="Sheet1")

# Delete rows with at least 2 null values
dfs = dfs.dropna(thresh=2)

first_pdf = False

objects = []
for i,(index, row) in enumerate(dfs.iterrows()):  # go through all rows
	if not (first_pdf and i == 0):		# If not columns names
		json = {"item":row[0],"quantidade":row[1],"unidade":row[2],"especificacoes":row[3],"valor_unitario":row[4],"fornecedor":row[5]}
		objects.append(json)

for objecto in objects:
	print(objecto)