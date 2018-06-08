## API de Projeto Transversal 2

Breve documentação sobre a API e os respectivos EndPoints.

## Sumário das Endpoints

- [Updating to New Releases](#updating-to-new-releases)
- [Get values differences].(#get_values_differences)
- [get_winner_companies].(#get_winner_companies)
- [get_empresas].(#get_empresas)
- [get_empresa].(#get_empresa)
- [get_processos].(#get_processos)
- [get_licitacoes].(#get_values_differences)

**get_values_differences**
----
  Retorna um json contendo os valores de cada item extraído das licitações, com o preço unitário multiplicado pela quantidade comprada e o valor total

* **URL**

  /get_values_differences

* **Method:**
  
  `GET`
  
* **URL Params**
  
  None

* **Data Params**

  None

* **Success Response:**
  
  * **Code:** 200 <br />
    **Conteúdo do Json retornado:** 
    ```
      "Total values analyze": 
      [
        {
          "File": SERVIÇO/ITEM/,
          "Expected aproximated total value": Valor calculado no DB do preço unitário vezes a quantidade de produtos.,
          "Real total value": Valor digitado na licitação.
        }
      ]
    ```
 
**get_winner_companies**
----
  Retorna um json contendo quantas vezes as empresas venceram o pregão da licitação.

* **URL**

  /get_winner_companies

* **Method:**
  
  `GET`
  
* **URL Params**
  
  None

* **Data Params**

  None

* **Success Response:**
  
  * **Code:** 200 <br />
    **Conteúdo do Json retornado:** 

    ```
    "Winner companies":
    [
      {
        "LDC Bortolozzi – Comercial - ME": {
        "wonBiddings": [
        "MATERIAIS DE MARCENARIA, CARPINTARIA E SERRALHERIA"
        ],
        "number_of_wins": 1,
        "total_value": "R$ 8.814,50"
      }
    ]
    ```
 
**get_empresas**
----
  Retorna um json contendo todas as informações de todas as empresas que estão no banco de dados.

* **URL**

  /get_empresas

* **Method:**
  
  `GET`
  
* **URL Params**
  
  None

* **Data Params**

  None

* **Success Response:**
  
  * **Code:** 200 <br />
    **Conteúdo do Json retornado:** 

    ```
    "Empresas":
    [
      {
        "valor_global": "R$ 69.016,80",
        "valor_estimado": "R$ 5.751,40",
        "termo_aditivo": Verifica se possui termo aditivo no pdf
        "nome_empresa": "F.E Máquinas Terraplanagem e Pavimentação LTDA",
        "ata": "1024/2016",
        "vigencia": "20/07/2016 - 19/07/2017"
      }
    ]        
    ```

**get_empresa**
----
  Recebe como parâmetro o nome de uma empresa específica e retorna um json com as informações referentes a empresa específica, assim como o número do processo a qual está participando.

* **URL**

  /get_empresa

* **Method:**
  
  `POST`
  
* **URL Params**
  
  None

* **Data Params**

  `{"nome_empresa" : "Nome da empresa a ser pesquisada}`

* **Success Response:**
  
  * **Code:** 200 <br />
    **Conteúdo do Json retornado:** 

    ```
    {
    "Empresa": [
        {
            "valor_global": "R$ 69.016,80",
            "valor_estimado": "R$ 5.751,40",
            "termo_aditivo": null,
            "nome_empresa": "F.E Máquinas Terraplanagem e Pavimentação LTDA",
            "ata": "1024/2016",
            "vigencia": "20/07/2016 - 19/07/2017"
        }
    ],
    "Processo": [
        "23106.008771/2015-57"
    ]
    }
    ```
 
**get_processos**
----
  Recebe como parâmetro o nome de uma empresa específica e retorna um json com apenas quais processos essa empresa está participando.

* **URL**

  /get_processos

* **Method:**
  
  `POST`
  
* **URL Params**
  
  None

* **Data Params**

  `{"nome_empresa" : "Nome da empresa a ser pesquisada}`

* **Success Response:**
  
  * **Code:** 200 <br />
    **Conteúdo do Json retornado:** 

    ```
    {
    "status": "ok",
    "Numero do processo": [
        "23106.008771/2015-57"
    ]
    }
    ```

**get_licitacoes**
----
  Retorna um json contendo todas as licitações do banco de dados, mostrando todas as informações a respeito (empresas, preço, data...)

* **URL**

  /get_licitacoes

* **Method:**
  
  `GET`
  
* **URL Params**
  
  None

* **Data Params**

  None

* **Success Response:**
  
  * **Code:** 200 <br />
    **Conteúdo do Json retornado:** 

    ```
    {
    "status": "ok",
    "licitacoes": [
        {
            "empresas": [
                {
                    "valor_global": "R$ 69.016,80",
                    "valor_estimado": "R$ 5.751,40",
                    "termo_aditivo": null,
                    "nome_empresa": "F.E Máquinas Terraplanagem e Pavimentação LTDA",
                    "ata": "1024/2016",
                    "vigencia": "20/07/2016 - 19/07/2017"
                },
                {
                    "valor_global": "R$ 91.840,00",
                    "valor_estimado": "R$ 7.653,33",
                    "termo_aditivo": null,
                    "nome_empresa": "CA Transporte, Comércio e Serviços Automotivos LTDA",
                    "ata": "1025/2016",
                    "vigencia": "20/07/2016 - 19/07/2017"
                }
            ],
            "demandante": "DIMAP",
            "materiais_e_servicos": "SRP 640/2016",
            "pdf_url": "https://www.google.com/url?q=http://prefeitura.unb.br/images/phocadownload/Atas/Relao%2520de%2520itens%2520Ata%2520PE%2520640-2016.pdf&sa=D&ust=1526535322513000&usg=AFQjCNE2VV_Y25B0Qjh6_DKdOYo3zL_FXA",
            "classificacao": "ATAS COM VIGÊNCIA EXPIRADA",
            "fiscal": "Marcio Mariano Lisboa Telefone: 3107-3330",
            "edital": "640/2016",
            "valor_total": "R$ 160.856,80",
            "contrato": null,
            "objeto": "LOCAÇÃO DE MÁQUINAS",
            "numero_processo": "23106.008771/2015-57"
        },
    ```
 
 
