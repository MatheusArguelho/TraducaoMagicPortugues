# Scripts de Tradução de Cartas de Magic: The Gathering

## Descrição

Estes scripts em Python permitem que você traduza o texto do oraculo e o flavour text das cartas de Magic: The Gathering do inglês para o português. O script `traducao_individual.py` traduz o texto de uma única carta, enquanto o script `traducao_set.py` traduz o texto de todas as cartas de uma coleção em específico. Ambos os scripts recuperam dados das cartas da API do Scryfall e usam a biblioteca Google Translator para realizar as traduções. O texto traduzido é então exibido junto com o texto original em arquivos HTML.

## Requisitos

- Python 3.x
- Biblioteca Pandas (`pip install pandas`)
- Biblioteca Deep Translator (`pip install deep-translator`)
- Biblioteca Requests (`pip install requests`)
- Biblioteca tqdm (`pip install tqdm`)
- Biblioteca webbrowser (`pip install webbrowser`)

## Uso

1. **traducao_individual.py**
    - Execute o script `traducao_individual.py`.
    - Digite o nome da carta de Magic: The Gathering que você deseja traduzir quando solicitado.
    - O script irá recuperar os dados da carta da API do Scryfall, traduzir o texto oracular e o texto de sabor para o português e gerar um arquivo HTML.
    - O arquivo HTML será aberto automaticamente em seu navegador padrão, exibindo o texto original e traduzido.

2. **traducao_set.py**
    - Execute o script `traducao_set.py`.
    - Digite o código de 3 digitos da coleção de Magic: The Gathering que você deseja traduzir quando solicitado.
    - O script irá recuperar os dados das cartas da API do Scryfall, traduzir o texto oracular para o português e gerar um arquivo CSV e um arquivo HTML contendo o texto original e traduzido.
    - O arquivo HTML será aberto automaticamente em seu navegador padrão e exibirá o texto traduzido em um formato de tabela estilizada.

## Observações

- Se algum dos scripts encontrar erros durante a execução, será exibida uma mensagem de erro.
- Certifique-se de ter uma conexão à internet ativa para buscar dados da API do Scryfall e realizar as traduções.
- Não sei um jeito legal de colocar isso num front end, caso alguem saiba como fazer, entre em contato comigo no Telegram @MatheusH1N1
