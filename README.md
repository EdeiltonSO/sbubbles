# Sblubbluebleles

## Sumário

[1. O que é isso?](#o-que-e-isso)

[2. Como executar?](#como-executar)

[3. Quais rotas estão disponíveis?](#quais-rotas)

[4. Como criar um model?](#criar-model)

[5. Como criar um novo registro via shell?](#criar-registro)

[6. Como acessar as tabelas pelo Django Admin?](#acessar-tabelas)

<a id="o-que-e-isso"></a>
## 1. O que é isso?

Sblubbluebleles

<a id="como-executar"></a>
## 2. Como executar?

As instruções a seguir ainda podem estar incompletas.

### 2.1. Pra fazer só uma vez

- Instale o VirtualBox;
- Descompacte o `sd.zip` fornecido;
- Acesse a pasta descompactada;
- Atualize `ipAdrPrefix` no Vagrantfile para `192.168.56.101`;
- Se já existir uma máquina virtual sd*, execute `vagrant destroy`;
- Acesse o diretório do `Vagrantfile`;
- Execute `vagrant up`;
- Execute `vagrant ssh`;

(note que agora você está em vagrant@sd)

- Execute `cd /vagrant/web-folder/`;
- Faça o `git clone` deste repositório;
- Acesse a pasta criada com o clone;
- Execute `cp .env.example .env`;
- Preencha o `.env`;
- Execute `python manage.py runserver 0:8000`;
- Acesse `192.168.56.101:8000/`.

*confira no VirtualBox ou executando `vagrant global-status`

### 2.2. Pra fazer sempre que for usar

- Acesse o diretório que contém o `Vagrantfile`;
- Execute `vagrant up`;
- Execute `vagrant ssh`;

(note que agora você está em vagrant@sd)

- Execute `cd /vagrant/web-folder/enquetes-django/`;
- Execute `python manage.py runserver 0:8000`;
- Acesse `192.168.56.101:8000/`.

<a id="quais-rotas"></a>
## 3. Quais rotas estão disponíveis?

A partir da URL `192.168.56.101:8000`, os seguintes caminhos podem ser acessados:

### 3.1. Fluxo principal

- `/signup`, para a tela de cadastro;
- `/login`, para a tela de login;
- `/`, para a página principal;

### 3.2. Fluxo de alteração de senha

- `/password_reset`, para o formulário de redefinição de senha;
- `/password_reset/done`, para a mensagem de confirmação de envio de e-mail;
- `/reset/<uidb64>/<token>`, como destino do link para redefinição enviado via e-mail;
- `/reset/done`, para a mensagem de confirmação de alteração de senha;

### 3.3. Publicações

- `/post/create`, para criar um post;
- `/post/<post_id>/delete`, para apagar um post;
- `/post/<post_id>/like`, para curtir um post;
- `/post/<post_id>/repost`, para republicar um post;
- `/post/<post_id>/save`, para salvar um post;
- `/post/<post_id>/report`, para denunciar um post;
- `/collection`, para visualizar os próprios posts salvos.

Observações:

- A rota de visualização de posts é a rota raiz;
- Todas as rotas acima dependem da autenticação do usuário.

### 3.4. Perfis de usuário 

- `user/<username>`, para visualizar o perfil de um usuário;
- `user/<username>/follow`, para seguir um usuário;
- `user/<username>/likes`, para visualizar as curtidas de um usuário;
- `user/saved`, para visualizar os próprios posts salvos.
]
Observações:

- A rota de visualização de perfil pode retornar dois templates diferentes: um para usuários autenticados e outro para usuários anônimos;
- As rotas de follow e visualização de likes de usuários alheios são disponíveis apenas para usuários autenticados;
- A rota de visualização de posts salvos só mostrará os posts do usuário autenticado.

### 3.5. Notificações

- `/notifications`, para visualizar a página de notificações;
- `/notifications/<notif_id>/mark_as_checked`, para processar a ação de marcar como lida.

### 3.6. Painel administrativo

- `/admin`, para o painel administrativo;

<a id="criar-model"></a>
## 4. Como criar um model?

1. Vá até `app/models.py` e modele a nova classe;
2. Execute `python manage.py makemigrations app` para criar a migration com o novo model;
3. Se quiser ver o SQL da migration, execute `python manage.py sqlmigrate app <numero_da_migration>`;
4. Execute `python manage.py migrate` para aplicar as modificações das migrations ao banco de dados;

### 4.1. Observações

- Os números das migrations são os prefixos numéricos dos arquivos dentro da pasta `app/migrations`;
- Se estiver usando o Vagrant, lembre-se de executar os comandos `python` dentro da máquina virtual;
- Ao usar SQLite, o arquivo `db.sqlite3` é criado no passo 1, caso ainda não exista;

<a id="criar-registro"></a>
## 5. Como criar um novo registro via shell?

### 5.1. Passo a passo

1. Acesse o shell executando `python manage.py shell`;

2. Execute `from app.models import <Model>`;

3. Siga a estrutura `from <módulo> import <função>` para importar bibliotecas extras, caso necessário;

4. Siga a estrutura abaixo para criar os dados do registro;
```
new_data = <Model>(<campo_x>='<valor_x>', <campo_y>='<valor_y>')
```

5. Execute `new_data.save()` para salvar o novo registro no banco de dados;

6. Siga a estrutura abaixo para visualizar o novo registro;
```
item = <Model>.objects.get(<atributo>='<valor>')
for k, v in item.__dict__.items(): print(f"{k}: {v}")
```

Pressione `Ctrl+D` ou chame a função `exit()` para sair do shell.

### 5.2. Exemplo: criando um usuário

```shell
python manage.py shell
```

```python
from app.models import CustomUser
```

```python
from django.contrib.auth.hashers import make_password
```

```python
from datetime import date
```

```python
usuario = CustomUser(
    email='johndoe@example.com',
    password=make_password('johndoe123'),
    username='johndoeatvoid',
    first_name='John',
    last_name='Doe',
    bio='My name is Doe. John Doe.',
    birthdate=date(1999, 12, 31)
)
```

```python
usuario.save()
```

```python
u = CustomUser.objects.get(username='johndoeatvoid')
```

```python
for k, v in u.__dict__.items(): print(f"{k}: {v}")
```

```python
exit()
```

<a id="acessar-tabelas"></a>
## 6. Como acessar as tabelas pelo Django Admin?

Para ter acesso às tabelas, é preciso ter uma conta de usuário administrador (superuser). Esse tipo de usuário tem acesso ao painel administrativo da aplicação e pode manipular diretamente o banco de dados.

### 6.1. Acessando as tabelas pelo Django Admin

1. Execute `python manage.py createsuperuser` para criar uma conta superuser;
2. Execute `python manage.py runserver 0:8000` para iniciar o servidor;
3. Acesse `http://192.168.56.101:8000/admin`, faça login e confira os dados.