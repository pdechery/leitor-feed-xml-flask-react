## Desafio Back-End

Este app implementa uma visualização do *feed* disponível em:

http://revistaautoesporte.globo.com/rss/ultimas/feed.xml

### Tecnologias utilizadas

**Backend**

*  Python 3.6
*  Flask 1.1 

**Front-end**

*  React 16
*  LESS

### Executando

Após fazer o clone do repositório pode-se executar o projeto com o Docker ou pelo próprio servidor de testes do Flask.

**1) Docker**

Executar `docker-compose up` na raiz do diretório gerado e após o *build* acessar http://localhost:1337

**2) Flask**

Na raiz do diretório gerado executar:

1. `pip install -r requirements.txt`
2. `python run.py`

Em seguida acessar http://localhost:5000

Favor atentar para os requisitos de cada uma das formas de execução (ter Python 3 instalado ou Docker e Docker Compose).

### A tela

Ao acessar, será pedido um login. O usuário e senha são:

> desafio
> backend

Após a autenticação serão exibidos os dados do feed em HTML. Para visualização em JSON, como pedido no desafio, basta clicar no link "Ver JSON", no canto direito da tela.

Dica: rodando em Flask o JSON ficará melhor formatado. Com o Docker, recomendo usar um formatador de JSON online, como o https://jsonformatter.curiousconcept.com/ ou o console do Chrome ou Firefox.