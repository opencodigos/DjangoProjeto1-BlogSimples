# Django CRUD Blog Simples

Primeiro vídeo tutorial de como criar um blog Simples com Django. Nesses tutorial vamos trabalhar com CRUD para que usuário iniciante tenha seu primeiro contato com esse framework incrível. 

Playlist 10 Vídeos [Link](https://www.youtube.com/playlist?list=PL2bJNatYYfGTo-V4u4hMQW76ZulF77K_8)

Vamos desenvolver um Blog com Django. Para conhecer mais a plataforma e conceitos.

<details><summary><b>Ambiente Virtual Linux/Windows</b></summary>

- **Ambiente Virtual Linux/Windows**
    
    
    Lembrando… Precisa ter Python instalado no seu ambiente.
    
    [https://www.python.org/downloads/](https://www.python.org/downloads/)
    
    **Criar o ambiente virtual Linux/Windows**
    
    ```python
    ## Windows
    python -m venv .venv
    source .venv/Scripts/activate # Ativar ambiente
    
    ## Linux 
    ## Caso não tenha virtualenv. "pip install virtualenv"
    virtualenv .venv
    source .venv/bin/activate # Ativar ambiente
    ```
    
    Instalar os seguintes pacotes.
    
    ```python
    pip install django
    pip install pillow
    ```
    
    Para criar o arquivo *requirements.txt*
    
    ```python
    pip freeze > requirements.txt
    ```
    
</details>

<details><summary><b>Criando o Projeto</b></summary>

- **Criando o Projeto**
    
    ## **Criando o projeto**
    
    “core” é nome do seu projeto e quando colocamos um “.” depois do nome do projeto significa que é para criar os arquivos na raiz da pasta. Assim não cria subpasta do projeto.
    
    ```python
    django-admin startproject core .
    ```
    
    **Testar a aplicação**
    
    ```python
    python manage.py runserver
    ```

 
</details>

<details><summary><b>Criando App</b></summary>

- **Criando App**
    
    **Vamos criar nosso aplicativo no Django.**
    
    Para criar a aplicação no Django rode comando abaixo. “*posts_app*” é nome do seu App.
    
    ```python
    python manage.py startapp posts_app
    ```
    
    Agora precisamos registrar nossa aplicação no *INSTALLED_APPS* localizado em *settings.py*.
    
    *posts_app/models.py*
    
    ```python
    from django.db import models
    
    # Create your models here.
    class Posts(models.Model):
        title = models.CharField(max_length=100)
        description = models.TextField()
        image = models.ImageField(upload_to='images/')
        create_at = models.DateTimeField(auto_now_add=True)
    ```
    
    *posts_app/admin.py*
    
    Temos que registrar nosso modelo Posts para aparecer no dashboard do Django.
    
    ```python
    from django.contrib import admin
    from .models import Posts
    
    # Register your models here.
    admin.site.register(Posts)
    ```
    
    ## M**igrações.**
    
    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```
    
    Vamos acessar o Dashboard Admin do Django precisamos ter um usuário.
    
    ```python
    python manage.py createsuperuser
    ```
    
    agora acessar a plataforma.
    
    ```python
    python manage.py runserver
    
    # http://127.0.0.1:8000/admin/
    ```
    
    Conseguimos fazer os testes no dashboard do Django e criar algumas postagens.
    
    Ao tentar acessar link da imagem aparece esse erro.
    
    Esse erro por que precisamos configurar nossos arquivos static no projeto. 
    
 
</details>

<details><summary><b>Arquivos Static</b></summary>

- **Arquivos Static**
    
    ## **Vamos configurar nossos arquivos** *static*
    
    ```python
    import os 
    
    # base_dir config
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
    STATIC_DIR=os.path.join(BASE_DIR,'static')
    
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
        }
    }
    
    # Passando para portugues BR
    LANGUAGE_CODE = 'pt-br'
    TIME_ZONE = 'America/Sao_Paulo'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    
    STATIC_ROOT = os.path.join(BASE_DIR,'static')
    STATIC_URL = '/static/' 
    
    MEDIA_ROOT=os.path.join(BASE_DIR,'media')
    MEDIA_URL = '/media/'
    ```
    
    *core/urls.py*
    
    ```python
    from django.contrib import admin
    from django.conf import settings
    from django.conf.urls.static import static
    from django.urls import path
    
    urlpatterns = [
        path('admin/', admin.site.urls),
    ]
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Adicionar Isto
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adicionar Isto
    ```
    
    **Acessar a aplicação e testar.**
    
    Agora as imagens serão encontradas na raiz do seu projeto. Pois já configuramos e dizemos para nosso App buscar lá. Isso é valido para qualquer arquivos estático. **Incluindo Templates.**
    
    Outro detalhes que vamos configurar é aqui. Como você pode ver na imagem abaixo todos os registros de criamos ficaram com nomenclatura de *object*. Em grandes continuidades isso pode gerar confusão. Vamos organizar isso.
    
    *posts_app/models.py* 
    Adicionar **str** e **Meta.**
    
    ```python
    from django.db import models
    
    # Create your models here.
    class Posts(models.Model):
        title = models.CharField(max_length=100)
        description = models.TextField()
        image = models.ImageField(upload_to='images/')
        create_at = models.DateTimeField(auto_now_add=True)
        
        def __str__(self): # adicionar isso
            return self.title
        
        class Meta:  # adicionar isso
            verbose_name = 'Post'
            verbose_name_plural = 'Posts'
            ordering = ['id']
    ```
    
    Já temos nossa lista de registro com nomes. 

 
</details>

<details><summary><b>Templates</b></summary>

- **Templates**
    
    Vamos configurar nossas views e Templates para deixar as coisas mais visual. 
    Em nosso ***posts_app*** vamos criar uma pasta chamada **“*templates*”**
    
    **Porque *templates* ?** No arquivo *settings.py* definimos que “*TEMPLATE_DIR*” é onde vamos buscar nossos templates. Podemos criar pasta *templates* em qualquer lugar da nossa aplicação que nosso projeto vai entender e buscar esses templates. Isso vale para arquivos static tambem. 
    
    ## Template Base
    
    1 - criar um arquivo base ***base.html*** onde vamos renderizar nosso conteúdo. 
    
    ```python
    {% load static %} # Adicionar isso
    <!DOCTYPE html>
    <html lang="en">
    <head>
    		<meta charset="UTF-8">
    		<meta http-equiv="X-UA-Compatible" content="IE=edge">
    		<meta name="viewport" content="width=device-width, initial-scale=1.0">
    		<title>{% block title %}{% endblock %}</title> # Adicionar isso
    </head>
    <body>
    		{% block content %} # adicionar isso
    		{% endblock %} 
    </body>
    </html>
    ```

 
</details>

<details><summary><b>Listar Posts</b></summary>

- **Listar Posts**
    
    ## Listar Postagens
    
    Arquivo ***post-list.html*** vamos listar as postagens que criamos.
    
    ```python
    {% extends 'base.html' %}
    
    {% block title %}Lista Postagens{% endblock %}
    
    {% block content %}
    	<h1>Todos os Posts</h1>
    
    	<!-- lista os posts aqui -->
    
    {% endblock content %}
    ```
    
    *posts_app/views.py*
    
    ```python
    from django.shortcuts import render
    from posts_app.models import Posts
    
    # Create your views here.
    def post_list(request):
        template_name = 'post-list.html' # template
        posts = Posts.objects.all() # query com todas as postagens
        context = { # cria context para chamar no template
            'posts': posts
            }
        return render(request, template_name, context) # render
    ```
    
    No nosso app **posts_app/urls.py** criar arquivo *urls.py.*
    
    ```python
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('', views.post_list, name='post-list'),
    ]
    ```
    
    Não podemos esquecer de registrar as rotas da aplicação no projeto. 
    Então no arquivo urls.py do projeto. core/urls.py.
    
    ```python
    from django.urls import path, include ## adicionar include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
    	 	path('', include('posts_app.urls')), # Adicionar isso.
    ] 
    ```
    
    No template ***post-list.html*** vamos chamar nosso contexto que definimos na view. “**posts**”.
    
    Chamando dessa maneira **{{posts}}** em nosso template ele retorna uma **query** com vários registro.
    
    Então precisamos fazer um for para “*indentar*” essas informações no template.
    Vou deixar **{{post.description}}** comentado. Por ser uma lista essa informação ficaria interessante na rota detalhes do post.
    
    ```python
    {% extends 'base.html' %}
    {% block title %}Lista Postagens{% endblock %}
    {% block content %}
    	<h1>Todos os Posts</h1>
    	# Adiciona esse for
    	{% for post in posts %} 
    			<img src="{{post.image.url}}" width="150" alt="{{post.title}}">
    			<p>{{post.title}}</p>
    			<!-- <p>{{post.description}}</p> --> 
    	{% endfor %}
    {% endblock content %}
    ```

 
</details>

<details><summary><b>Criar Posts</b></summary>

- **Criar Posts**
    
    ## Criar Posts
    
    *posts_app/forms.py* **criar arquivo forms.py**
    
    ```python
    from django import forms
    from .models import Post
    
    class PostForm(forms.ModelForm):
        class Meta:
            model = Post # nosso modelo
            fields = ['title', 'description', 'image'] # campos do nosso modelo poderia ser '__all__'
    ```
    
    *posts_app/views.py* 
    
    ```python
    from django.contrib import messages
    from django.urls import reverse
    from django.http import HttpResponseRedirect
    from posts_app.forms import PostsForm
    
    def post_create(request):
        if request.method == 'POST': # para metodo POST
            form = PostsForm(request.POST, request.FILES) # pega as informações do form
            if form.is_valid(): # se for valido
                form = form.save(commit=False)
                form.save() # salva
                
                messages.success(request, 'O post foi criado com sucesso') # mensagem quando cria o post
                return HttpResponseRedirect(reverse('post-list')) # coloquei para retornar post-list
            
        form = PostsForm() # senão carrega o formulario  
        return render(request, 'post-form.html', {"form": form}) # nesse template
    ```
    
    *posts_app/*urls.py
    
    ```python
    path('post-create', views.post_create, name='post-create'),
    ```
    
    Criar arquivo *posts_app/templates/post-form.html*.
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Criar/Atualizar Postagem{% endblock %}
    
    {% block content %} 
    	
    	<form method="post" 
    		action="{% if request.method == 'POST' %}{% url 'post-create' %}{% endif %}" 
    		enctype="multipart/form-data">
    
    		{% csrf_token %}
    		{{ form.as_p }}
    		<button type="submit">Criar</button> 
    	</form>
    
    {% endblock content %}
    ```
    
    *posts_app/templates/post-list.html* Adiciona a chamada para criar um post
    
    ```python
    <a href="{% url 'post-create' %}">Criar um Post</a> # adiciona
    ```
    
    **Configura mensagem.**
    *posts_app/templates/_message.html*
    
    ```python
    {% if messages %}
    <div class="messages">
        {% for message in messages %}
        <div {% if message.tags %} class="alert {{ message.tags }}"{% endif %} role="alert">{{ message }}</div>
        {% endfor %}
    </div>
    {% endif %}
    ```
    
    Adiciona na base
    
    ```python
    <body> 
    	{% include '_message.html' %} ## adiciona isso.
    	{% block content %}
    	{% endblock %} 
    </body>
    ```
 
</details>

<details><summary><b>Ver Post</b></summary>
       
- **Ver Post**
    
    ## Detalhes do post
    
    *posts_app/views.py* 
    
    ```python
    def post_detail(request, id):
        template_name = 'post-detail.html' # template
        post = Posts.objects.get(id=id) # Metodo Get
        context = { # cria context para chamar no template
            'post': post
            }
        return render(request, template_name, context) # render
    ```
    
    *posts_app/urls.py*
    
    ```python
    path('post-detail/<int:id>/', views.post_detail, name='post-detail'),
    ```
    
    Criar template *posts_app/templates/post-detail.html*
    
    ```python
    {% extends 'base.html' %}
    {% block title %}Detalhes Postagem{% endblock %}
    {% block content %}
    		<h1>Detalhes do Post: {{post.title}}</h1>
    		<p>{{post.create_at}}</p>
    		<img src="{{post.image.url}}" width="300" alt="{{post.title}}">
    		<p>{{post.description}}</p>  
    {% endblock content %}
    ```
    
    Para criar o clique para ir para detalhe da postagem. Modificar o template post-list.html
    Passamos um ID para rota e acessamos detalhes da postagem.
    
    ```python
    	{% for post in posts %}  
    			<a href="{% url 'post-detail' post.id %}">Ver</a> ## Adicionar isso
    			<img src="{{post.image.url}}" width="150" alt="{{post.title}}">
    			<p>{{post.title}}</p> 
    	{% endfor %}
    ```
 
</details>

<details><summary><b>Atualizar Post</b></summary>
        
- **Atualizar Post**
    
    ## Atualizar Post
    
    Vamos aproveitar o mesmo template que utilizamos para criar uma postagem. Então não precisa criar template HTML.
    
    *posts_app/views.py*
    
    ```python
    def post_update(request, id):
        post = get_object_or_404(Posts, id=id) # id do post
        form = PostsForm(request.POST or None, request.FILES or None, instance=post) # pega as informações do form
        if form.is_valid(): # se for valido
            form.save() # salva
            
            messages.success(request, 'O post foi atualizado com sucesso') # mensagem quando cria o post
            return HttpResponseRedirect(reverse('post-detail', args=[post.id])) # coloquei para retornar post-list
             
        return render(request, 'post-form.html', {"form": form}) # nesse template
    ```
    
    *posts_app/urls.py*
    
    ```python
    path('post-update/<int:id>', views.post_update, name='post-update'),
    ```
    
    *posts_app/templates/post-form.html*
    
    ```html
    action="{% if request.method == 'POST' %}{% url 'post-create' %}{% endif %}"
    ```
    
    *posts_app/templates/post-detail.html*
    
    ```python
    <a href="{% url 'post-update' post.id %}">Atualizar</a>
    ```
 
</details>

<details><summary><b>Deletar Post</b></summary>
        
- **Deletar Post**
    
    ## Deletar Postagem
    
    *posts_app/views.py*
    
    ```python
    from django.urls import reverse
    from django.http import HttpResponseRedirect
    
    def post_delete(request, id): 
        post = Posts.objects.get(id=id) # pelo ID pega o objeto
        post.delete() # deletar
        messages.success(request, 'O post foi deletado com sucesso') # quando deleta post
        return HttpResponseRedirect(reverse('post-list')) # retorna rota post-list
    ```
    
    *posts_app/*urls.py
    
    ```python
    path('post-delete/<int:id>/', views.post_delete, name='post-delete'),
    ```
    
    *posts_app/templates/*post-detail.html
    
    ```python
    <a href="{% url 'post-delete' post.id %}">Deletar</a> # adicionar botão delete
    ```
    
    Para colocar mensagem de confirme
    
    ```python
    def post_delete(request, id): 
        post = Posts.objects.get(id=id) # pelo ID pega o objeto
        if request.method == 'POST':         
            post.delete()
            messages.success(request, 'O post foi deletado com sucesso') # quando deleta post 
            return HttpResponseRedirect(reverse('post-list')) # retorna rota post-list
        return render(request, 'post-delete.html') # nesse template
    ```
    
    myapp/post-delete.html
    
    ```html
    {% extends 'base.html' %}
    {% block title %}Deletar Postagem{% endblock %}
    {% block content %}
    <form method="post">
        {% csrf_token %}
        <p>Deseja deletar esse post ?</p>
        <button type="submit">Deletar</button>
    </form> 
    {% endblock content %}
    ```
 
</details>

<details><summary><b>Bootstrap Configuração</b></summary>

- **Bootstrap Configuração**
    
    ## Bootstrap configuração
    
    Doc: [https://getbootstrap.com/docs/5.2/getting-started/introduction/](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
    
    Com Base na documentação para utilizar os recursos Boostrap basta adicionar as tags de CSS e JS. No HTML da Pagina Base.
    
    ```jsx
    <!-- CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    
    <!-- JS-->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
    ```
    
    *posts_app/templates/base.html*
    
    ```html
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
    	<meta charset="UTF-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    	<title>{% block title %}{% endblock %}</title>
    
    	<!-- CSS -->
    	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    
    </head>
    <body> 
    	{% include '_messages.html' %}
    	
    	{% block content %}
    	{% endblock %} 
     
    	<!-- JS-->
    	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
    </body>
    </html>
    ```

</details>

<details><summary><b>Bootstrap Templates</b></summary>

- **Bootstrap Templates** 
    
    *posts_app/templates/post-list.html*
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Lista Postagens{% endblock %}
    
    {% block content %}
    	<a class="btn btn-success" href="{% url 'post-create' %}">Criar um Post</a>
    
    	<h1>Todos os Posts</h1>
    	<div class="row row-cols-1 row-cols-md-3 g-4">
    		{% for post in posts %} 
    		<div class="col">
    			<div class="card h-100 text-bg-light">
    				<img src="{{post.image.url}}" class="card-img-top" alt="{{post.title}}">
    				<div class="card-body">
    					<p class="card-text">{{post.title}}</p>
    					<a class="btn btn-info" href="{% url 'post-detail' post.id %}">Ver</a>
    				</div>
    			</div> 
    		</div>
    		{% endfor %} 
    	</div>	 
    {% endblock content %}
    ```
    
    *posts_app/templates/post-detail.html*
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Detalhes Postagem{% endblock %}
    
    {% block content %}
    	<div class="text-center">
    
    		<a class="btn btn-warning" href="{% url 'post-update' post.id %}">Atualizar</a>
    		<a class="btn btn-danger" href="{% url 'post-delete' post.id %}">Deletar</a>
    
    		<h1>Detalhes do Post: {{post.title}}</h1>
    	
    		<p>{{post.create_at}}</p> 
    	
    		<img src="{{post.image.url}}" width="100%" alt="{{post.title}}">
    	 
    		<p>{{post.description}}</p>  
    
    	</div>
    {% endblock content %}
    ```
    
    *posts_app/templates/*post-form.html
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Criar/Atualizar Postagem{% endblock %}
    
    {% block content %}  
    
    <div class="row justify-content-center">
    	<div class="col-md-6">
    		<h1>{% if request.path == '/post-create' %}Criar Postagem{% else %}Atualizar Post{% endif %}</h1>
    		
    		<form method="post" action="{% if request.method == 'POST' %}{% url 'post-create' %}{% endif %}" 
    			enctype="multipart/form-data">
    			{% csrf_token %}
    			{{ form.as_p }}
    			<button class="btn btn-success" type="submit">Criar</button> 
    		</form>
    
    	</div>
    	
    </div>
    
    {% endblock content %}
    ```
    
    *posts_app/forms.py*
    
    Aplicar as classes boostrap
    
    ```python
    from django import forms
    from .models import Posts
    
    class PostsForm(forms.ModelForm):
        class Meta:
            model = Posts
            fields = ['title', 'description', 'image']
    
        def __init__(self, *args, **kwargs): # Adiciona 
            super().__init__(*args, **kwargs)  
            for field_name, field in self.fields.items():   
                  field.widget.attrs['class'] = 'form-control'
    ```
    
    *myapp/settings.py*
    
    ```
    import os
    from django.contrib.messages import constants as messages
    
    MESSAGE_TAGS = {
            messages.DEBUG: 'alert-secondary',
            messages.INFO: 'alert-info',
            messages.SUCCESS: 'alert-success',
            messages.WARNING: 'alert-warning',
            messages.ERROR: 'alert-danger',
     }
    ```

</details>