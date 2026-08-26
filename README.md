#  JBot

Um bot multifuncional para o Discord focado na moderação de servidores e no gerenciamento automático de canais de voz, totalmente containerizado com Docker. 

##  Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **Biblioteca:** `discord.py`
* **Infraestrutura:** Docker

##  Funcionalidades

O bot possui comandos administrativos protegidos por hierarquia de permissões:

* `/kick @usuario [motivo]`: Expulsa um membro do servidor.
* `/ban @usuario [motivo]`: Bane um membro do servidor.
* `/clear [quantidade]`: Limpa mensagens de um chat em massa.
* `/lock` e `!unlock`: Bloqueia e desbloqueia o envio de mensagens em um canal específico.
* **Canais de Voz Dinâmicos:** /criarvoz Escuta eventos de voz para criar e limpar canais temporários automaticamente (evitando poluição visual no servidor).

##  Como Rodar o Projeto

Este projeto foi construído para rodar em um container isolado. Você não precisa instalar o Python ou as dependências na sua máquina, basta ter o **Docker** instalado.

### 1. Construa a Imagem
Clone este repositório e rode o comando abaixo na pasta raiz do projeto para criar a imagem Docker:
```bash
docker build -t jbot .

```
### 2. Execute o container
Para iniciar o bot, você precisa passar o Token de acesso fornecido pelo Discord Developer Portal através de uma variável de ambiente.

Execute o comando abaixo, substituindo SEU_TOKEN_AQUI pelo token real do seu bot: 
```bash
docker run -d --name jbot_container -e DISCORD_TOKEN="SEU_TOKEN_AQUI" jbot

```
### 3. Pare o bot
Se precisar desligar o bot, utilize:
```bash
docker stop jbot_container

```
