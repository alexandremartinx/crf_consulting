import requests
import pandas as pd
import random
from libs.cnpjs import cnpj_list, cnpj_list_format

user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:10.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Maemo; Linux armv7l; rv:10.0) Gecko/20100101 Firefox/10.0 Fennec/10.0',
]

cnpj_pontos = cnpj_list()
cnpjs = cnpj_list_format()

def crfrj():
    data_list_rj = []
    for cnpj in cnpjs:
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}

        params = {
            'cnpj':  cnpj,
            'razao': '',
    }

        try:
            response = requests.get('http://siscon.ddns.net:8956/ws/sql-estabelecimentos.php', params=params, headers=headers, verify=False)
            data_dict = {}
            data = response.json()
            inscricao = data[1]['1']
            validade = data[1]['3']
            status = data[1]['4']
            data_dict['cnpj'] = cnpj
            data_dict['inscricao'] = inscricao
            data_dict['validade'] = validade
            data_dict['status'] = status
            data_list_rj.append(data_dict)
            print(data_dict)
        except:
            print('Loja não registrada')
            continue
    return data_list_rj

crfrj_numeros = crfrj()
df_crfrj = pd.DataFrame(crfrj_numeros) 
df_crfrj.to_csv('crfrj.csv', sep=',', encoding='utf-8', index=False)

