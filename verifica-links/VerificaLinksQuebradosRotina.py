#@title Captura de links do site escolhido {display-mode: "form"}
# This code will be hidden when the notebook is loaded.
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
from tqdm import tqdm

def check_links(url):
    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar {url}. Status de requisição: {response.status_code}")
        return []

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


def check_links_on_pages(pages):
    all_links = []

    for page in tqdm(pages, desc="Verificando links na página: ", unit="página"):
        page_links = check_links(page['link'])
        all_links.extend(page_links)

    return all_links

# Exemplo de uso
print('Por favor informe a URL iniciando com "http://" ou "https://"')
url = input()
pages = check_links(url)
result = check_links_on_pages(pages)

print('Escolha o tipo de resposta')
print('1 - Exibição em tela')
print('2 - Arquivo de texto')
print('3 - Arquivo csv')
print('4 - Arquivo xlsx')

tipo_resposta = int(input())

def switch(tipo_resposta):
  if tipo_resposta == 1:
    # Exibição dos resultados em tela
    for link in result:
        print(link)
  elif tipo_resposta == 2:
    # Geração de arquivo TXT
    with open('resultados.txt', 'w') as file:
        for link in result:
            file.write(str(link) + '\n')
  elif tipo_resposta == 3:
    # Geração de arquivo CSV
    df = pd.DataFrame(result)
    df.to_csv('resultados.csv', index=False)
  elif tipo_resposta == 4:
    # Geração de arquivo Excel (xlsx)
    df = pd.DataFrame(result)
    df.to_excel('resultados.xlsx', index=False)


switch(tipo_resposta)