# Lista de Links

Este é um projeto em Python que verifica os links de um site e fornece informações sobre cada um deles, como a página onde o link está alocado, o link com problema, o status de requisição desse link e o tipo de link.

## Requisitos

- Python 3.x
- Bibliotecas Python: requests, BeautifulSoup, pandas, openpyxl, tqdm

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/davidjeiel/lista-links.git
   ```

2. Acesse o diretório do projeto:
   ```bash
   cd lista-links
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Execute o arquivo `check_links.py`:
   ```bash
   python check_links.py
   ```

2. Será solicitado que você insira a URL do site que deseja verificar.

3. Escolha o tipo de resposta que deseja receber:
   - Digite `1` para gerar um arquivo de texto com os resultados.
   - Digite `2` para gerar um arquivo CSV com os resultados.
   - Digite `3` para gerar um arquivo Excel (xlsx) com os resultados.
   - Digite `4` para exibir os resultados em tela.

4. Dependendo da sua escolha, os resultados serão exibidos em tela, ou um arquivo de texto, CSV ou Excel será gerado contendo os resultados.

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou correções, fique à vontade para abrir um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---
