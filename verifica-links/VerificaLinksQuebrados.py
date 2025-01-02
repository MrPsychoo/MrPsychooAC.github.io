import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import pandas as pd
from tqdm import tqdm

def check_links(url):
    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar {url}. Status de requisição: {response.status_code}")
        return

    # Analisa o HTML da página usando o BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Obtém o domínio da URL base
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc

    # Lista para armazenar os resultados
    links = []

    # Encontra todos os elementos <a> no HTML
    for link in tqdm(soup.find_all('a'), desc="Processando links", unit="link"):
        href = link.get('href')

        if href is None:
            continue

        # Verifica o tipo de link
        link_type = None
        if href.startswith('tel:'):
            link_type = 'tel'
        elif href.startswith('mailto:'):
            link_type = 'mailto'
        elif href.startswith('#'):
            link_type = 'anchor'
        elif href.startswith('/'):
            link_type = 'internal'
        else:
            link_type = 'external'

        # Resolve links relativos para links absolutos
        if href.startswith('/') or href.startswith('#'):
            href = urljoin(url, href)

        # Remove fragmento da URL (parte após #)
        href = urldefrag(href)[0]

        # Verifica se o link está no mesmo domínio ou é um link externo
        parsed_href = urlparse(href)
        if parsed_href.netloc == base_domain or parsed_href.netloc == '':
            # Ignora links do tipo "tel"
            if link_type == 'tel':
                continue

            # Faz a requisição HTTP para verificar o status do link
            link_response = requests.head(href, allow_redirects=True)
            link_status = link_response.status_code
            links.append({
                'page': url,
                'link': href,
                'status': link_status,
                'type': link_type
            })

    return links

print('Por favor informe a URL iniciando com "http://" ou "https://"')
url = input() 
result = check_links(url)

print('Escolha o tipo de resposta')
print('1 - Arquivo de texto')
print('2 - Arquivo csv')
print('3 - Arquivo xlsx')
print('4 - Exibição em tela')

tipo_resposta = int(input())

def switch(tipo_resposta):
    if tipo_resposta == 1: # Geração de arquivo TXT
        print(' - Seu arquivo "txt" está sendo gerado')
        with open('resultados.txt', 'w') as file:
            for link in result:
                file.write(str(link) + '\n')
    elif tipo_resposta == 2: # Geração de arquivo CSV
        print(' - Seu arquivo "csv" está sendo gerado')        
        df = pd.DataFrame(result)
        df.to_csv('resultados.csv', index=False)
    elif tipo_resposta == 3: # Geração de arquivo Excel (xlsx)        
        print(' - Seu arquivo "xlsx" está sendo gerado')
        df = pd.DataFrame(result)
        df.to_excel('resultados.xlsx', index=False)
    elif tipo_resposta == 4: # Exibição dos resultados em tela        
        print(' - Seus dados foram gerados')
        for link in result:
            print(link)

# Chamada da função switch com o tipo_resposta
switch(tipo_resposta)
