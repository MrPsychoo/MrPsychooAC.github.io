import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import pandas as pd
from tqdm import tqdm

def check_links(url):
    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    #print(response)
    #print(response.text)
    #print(response.request)
    #print(response.links)
    #print(response.headers)
    #print(response.url)
	
    #if response.status_code != 200:
    #    print(f"Erro ao acessar {url}. Status de requisição: {response.status_code}")
    #    return

    # Analisa o HTML da página usando o BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Obtém o domínio da URL base
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc
    #print(parsed_url)
    #print(base_domain)
    # Lista para armazenar os resultados
    links = []

    # Encontra todos os elementos <a> no HTML
    for link in tqdm(soup.find_all('a'), desc="Processando links", unit="link"):
        href = link.get('href')
        #print(link)
        #print(href)
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
        elif href.startswith('https://www.fgts.gov.br'):
            link_type = 'internal'
        elif href.startswith('https://fgts.gov.br'):
            link_type = 'internal'
        else:
            link_type = 'external'
        #print(link_type)
        # Resolve links relativos para links absolutos
        if href.startswith('/') or href.startswith('#'):
            href = urljoin(url, href)
        #print("-----------------urljoin(url, href)-----------------")
        #print(href)
        # Remove fragmento da URL (parte após #)
        href = urldefrag(href)[0]
        #print("-----------------urldefrag(href)[0]-----------------")
        #print(href)
        # Verifica se o link está no mesmo domínio ou é um link externo
        parsed_href = urlparse(href)
        #print("-----------------parsed_href.netloc == base_domain or parsed_href.netloc == ''-----------------")
        #print("-----------------parsed_href-----------------")
        #print(parsed_href)
        #print(parsed_href.netloc)
        #print(base_domain)
        #if parsed_href.netloc == base_domain or parsed_href.netloc == '':
        if base_domain != '':
            # Ignora links do tipo "tel"
            if link_type == 'tel':
                continue

            # Faz a requisição HTTP para verificar o status do link
            link_response = requests.head(href, allow_redirects=True)
            link_status = link_response.status_code
			
            print("-----------------# Faz a requisição HTTP para verificar o status do link-----------------")
            #print(link_response)
            print(link_status)
			
            #print(link_response.text)
            #print(link_response.request)
            #print(link_response.links)
            #print(link_response.headers)

            #print("-----------------# verificar se a pagina possui link quebrado que apresenta como 200 mas esta offline e redireciona para home-----------------")
			# verificar se a pagina possui link quiebrado que apresenta como 200 mas esta offline e redireciona para home
			
            
            print("# URL chamada e URL retornada")
            print(href)
            print(link_response.url)

            if href == link_response.url:
                print("e igual")
            elif href.startswith('https://www.fgts.gov.br/_layouts/15/Authenticate.aspx'):
                link_status = 302
            elif href.startswith('http://www.caixa.gov.br/_layouts/15/Authenticate.aspx'):
                link_status = 302
            elif link_response.url.startswith('https://validate'):
                link_status = 302
            else:
                if href.startswith('http://www.caixa.gov.br') or href.startswith('https://www.caixa.gov.br'):
                    print(href)
                    #href1 = urljoin(href, '/Paginas/default.aspx')
                    #href2 = urljoin(href, '/Paginas/home-caixa.aspx')
                    #href2 = href2.replace("http", "https")

                    href1 = href+'/Paginas/default.aspx'
                    href2 = href+'/Paginas/home-caixa.aspx'
                    href2 = href2.replace("http", "https")
                    href3 = href1.replace("http", "https")

                    print("# novas hrefs CAIXA")
                    print(link_response.url)
                    print(href1)
                    print(href2)
                    if href1 == link_response.url:
                        href = href1
                        print("e igual")
                    elif href2 == link_response.url:
                        href = href2
                        print("e igual")
                    elif href3 == link_response.url:
                        href = href3
                        print("e igual")
                    else:
                        link_status = 404
                        print("não e igual")
                else:
                    link_status = 404
                    print("não e igual")

            # criar página com links quebrados e com links passando parametros para poder validar a URL e pegar a extensao
			#print("-----------------# split URL-----------------")
            #extensao = href.split(".")[-1]
            extensao = href.split("/")[-1]
            extensao = extensao.split("?")
            extensao = extensao[0].split(".")
            extensao = extensao[-1]
			
            #extensao = href.split(".")
            print("# extensao")
            #print(extensao[1])
            print(extensao)
            #print(extensao[-1])
			

            extensoes = ['br', 'jsf', 'fgtsdigital', 'pt-br', 'Caixa', 'Caixa', 'canalcaixa', 'details', 'id1038441027', 'convocacao-para-os-empregadores-participarem-do-periodo-de-testes-em-producao-limitada', '']
            #extensoes = ['aspx', 'xlsx', 'pdf']
            if extensao in extensoes:
                extensao = ''


            links.append({
                'page': url,
                'link': href,
                'tipo_url': extensao,
                'status': link_status,
                'type': link_type
            })
            #print("-----------------# Faz a requisição HTTP para verificar o status do link-----------------")
    return links

print('Por favor informe a URL iniciando com "http://" ou "https://"')
url = input() 
result = check_links(url)

# Geração de arquivo CSV
print(' - Seu arquivo "csv" está sendo gerado')        
df = pd.DataFrame(result)
df.to_csv('resultados.csv', index=False)