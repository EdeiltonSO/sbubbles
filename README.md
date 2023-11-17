# Sblubbluebleles

## O que é isso?

Sblubbluebleles

## Como executar?

As instruções a seguir ainda podem estar incompletas.

### Pra fazer só uma vez

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

### Pra fazer sempre que for usar

- Acesse o diretório que contém o `Vagrantfile`;
- Execute `vagrant up`;
- Execute `vagrant ssh`;

(note que agora você está em vagrant@sd)

- Execute `cd /vagrant/web-folder/enquetes-django/`;
- Execute `python manage.py runserver 0:8000`;
- Acesse `192.168.56.101:8000/`.

## Quais rotas estão disponíveis?

A partir da URL `192.168.56.101:8000`, os seguintes caminhos podem ser acessados:

- `/admin`;

## Como criar um model?

1. Vá até `app/models.py` e modele a nova classe;
2. Execute `python manage.py makemigrations app` para criar a migration com o novo model;
3. Se quiser ver o SQL da migration, execute `python manage.py sqlmigrate app <numero_da_migration>`;
4. Execute `python manage.py migrate` para aplicar as modificações das migrations ao banco de dados;

### Observações

- Os números das migrations são os prefixos numéricos dos arquivos dentro da pasta `app/migrations`;
- Se estiver usando o Vagrant, lembre-se de executar os comandos `python` dentro da máquina virtual;
- Ao usar SQLite, o arquivo `db.sqlite3` é criado no passo 1, caso ainda não exista;

## Como criar um novo registro no banco de dados via shell?

### Passo a passo

1. Acesse o shell executando `python manage.py shell`;
2. Execute `from app.models import <Model>`;
3. Execute `from <módulo> import <função>` para importar bibliotecas extras, caso necessário;
4. Execute `<var> = <Model>(<atributo_x>='<valor_x>', <atributo_y>='<valor_y>')` para criar uma variável com os dados do registro;
5. Execute `<var>.save()` para salvar o novo registro no banco de dados;
6. Execute `item = <Model>.objects.get(<atributo>='<valor>')` e `for k, v in item.__dict__.items(): print(f"{k}: {v}")` para visualizar o novo registro;

Pressione `Ctrl+D` para sair do shell.

### Exemplo: criando um usuário

`$ python manage.py shell`

`> from app.models import User`

`> from django.contrib.auth.hashers import make_password`

`> from datetime import date`

```
> usuario = User(
    email='johndoe@example.com',
    password=make_password('johndoe123'),
    username='johndoeatvoid',
    usertitle='John Doe',
    bio='My name is Doe. John Doe.',
    birthdate=date(1999, 12, 31)
)
```

`> usuario.save()`

`> u = User.objects.get(email='johndoe@example.com')`

`> for k, v in u.__dict__.items(): print(f"{k}: {v}")`

`> exit()`
