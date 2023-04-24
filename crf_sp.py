import requests
import time
import pandas as pd
import random
from libs.cnpjs import cnpj_list_format

user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
]

cnpj_pontos = cnpj_list_format()

def crfsp():
    crfsp_numbers = []
    crfsp_fail = []
    for cnpj in cnpj_pontos:
        #rotaciona os user agents a cada chamada
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}

        print('consultando: ', cnpj)
        data_dict = {}
        #inseri o cep como parâmetro na querry
        data = {
            'cnpj': cnpj,
            'consultar': 'Consultar',
        }

#tratamento em caso de quebra na conexão
        for i in range(5):
            try:
                response = requests.post('https://ecat.crfsp.org.br/consultar-cr', data=data, headers=headers, timeout=3)
                print(response)
                if response.status_code in range(200,300):
                    certo = True
                    break
            except:
                time.sleep(1)
                continue
        if certo:
            req = response.text
        else:
            continue
        #scrap na página desejada
        try:
            if 'Gerar Relatório' in req:
                crfsp  = req.split('CRFSP:</td>')[-1].split('</td>')[0].split('<td>')[-1]
                crfsp_number = crfsp.split('<strong>')[1].split('</strong>')[0]
                crfpj  = req.split('CRFPJ:</td>')[-1].split('</td>')[0].split('<td>')[-1]
                crfpj_number = crfpj.split('<strong>')[1].split('</strong>')[0]
                if crfpj_number != 'I. Acesso e Utilização':
                    data_dict['cnpj'] = cnpj
                    data_dict['crfsp'] = crfsp_number
                    data_dict['crfpj'] = crfpj_number
                    crfsp_numbers.append(data_dict)
                    time.sleep(1)
            if 'Este estabelecimento não possui Certidão de Regularidade.'in req:
                data_dict['cnpj'] = cnpj
                data_dict['crfsp'] = 'Não encontrado'
                data_dict['crfpj'] = 'Não encontrado'
                crfsp_fail.append(data_dict)
                continue
            if 'Este estabelecimento teve sua Certidão de Regularidade cancelada.' in req:
                data_dict['cnpj'] = cnpj
                data_dict['crfsp'] = 'Não encontrado'
                data_dict['crfpj'] = 'Não encontrado'
                crfsp_fail.append(data_dict)
                continue
        except:
            print('error')
            continue
        #transforma dados em csv
    df_crfsp = pd.DataFrame(crfsp_numbers) 
    df_crfsp.to_csv('crfsp.csv', sep=',', encoding='utf-8', index=False)
    df_crfsp_fail = pd.DataFrame(crfsp_fail) 
    df_crfsp_fail.to_csv('crfsp_fail.csv', sep=',', encoding='utf-8', index=False)
    return crfsp_numbers

crfsp()
