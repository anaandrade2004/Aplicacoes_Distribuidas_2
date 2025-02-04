from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from processoclinico.models import Agente, Utente, Medicamento, Stock, Fornecedor  # Ajuste conforme os modelos
from django.db import transaction
from django.db.models import Max, Count
from rest_framework import viewsets
from rest_framework.decorators import action
from processoclinico.serializers import *



class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    #permission_classes = [permissions.IsAuthenticated]
    

class AgenteViewSet(viewsets.ModelViewSet):
    queryset = Agente.objects.all()
    serializer_class = AgenteSerializer
    #permission_classes = [permissions.IsAuthenticated]

class UtenteViewSet(viewsets.ModelViewSet):
    queryset = Utente.objects.all()
    serializer_class = UtenteSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ReceitaViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer
    #permission_classes = [permissions.IsAuthenticated]

    
class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    #permission_classes = [permissions.IsAuthenticated]

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    #permission_classes = [permissions.IsAuthenticated]

    
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    #permission_classes = [permissions.IsAuthenticated]



#------------------------LOGIN----------------------



def login_page(request):
    if request.method == 'POST':
        nif = request.POST.get('nif')
        try:
            # Mapeamento de cargos para páginas iniciais
            cargo_to_home = {
                'médico': 'home_page_medico',
                'enfermeiro': 'home_page_medico',
                'farmacêutico': 'home_page_farma',
                'boss': 'home_page_boss',  
            }

            # Verifica se o NIF pertence a um Utente
            utente = Utente.objects.filter(id=nif).first()
            if utente:
                request.session['user_type'] = 'utente'
                request.session['utente_id'] = str(utente.id)  # Armazena o ID do utente na sessão
                return redirect('home_page_utente')

            # Verifica se o NIF pertence a um Agente
            agente = Agente.objects.filter(id=nif).first()
            if agente:
                request.session['user_type'] = agente.cargo.lower()  # Armazena o cargo do agente
                request.session['id_utlizador'] = str(agente.id)  # Armazena o ID do agente na sessão
                home_page = cargo_to_home.get(agente.cargo.lower())
                if home_page:
                    return redirect(home_page)

            # Caso seja um admin padrão
            if nif == "admin123456789":
                request.session['user_type'] = 'boss'
                request.session['id_utlizador'] = 'admin123456789'
                return redirect('home_page_boss')

            # Se o NIF não for encontrado
            messages.error(request, "ID inválido. Por favor, tente novamente.")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {e}")

    return render(request, 'login_page.html')








def home_utente(request):
    utente = Utente.objects.get(id=request.session.get('utente_id'))
    return render(request, 'paciente/home_page.html', {
        'nome_usuario': utente.nome  # Assumindo que o modelo 'Utente' tem o campo 'nome'
    })





def home_medico(request):
    agente = Agente.objects.get(id=request.session.get('id_utlizador'))
    nome_usuario = agente.nome  # Assumindo que o modelo 'Agente' tem o campo 'nome'

    # Verificar se o cargo é médico ou enfermeiro
    if agente.cargo.lower() == 'médico':
        saudacao = f"Bem-vindo, Dr(a). {nome_usuario}!"
    elif agente.cargo.lower() == 'enfermeiro':
        saudacao = f"Bem-vindo, Enfermeiro(a) {nome_usuario}!"
    else:
        saudacao = f"Bem-vindo, {nome_usuario}!"

    return render(request, 'medico/home_page.html', {
        'saudacao': saudacao  # Passar a saudação para o template
    })






def home_farma(request):
    agente = Agente.objects.get(id=request.session.get('id_utlizador'))
    medicamentos_com_stock_baixo = Stock.objects.filter(s_total__lt=models.F('s_min')).select_related('medicamento')
    return render(request, 'farmaceutico/home_page.html', {
        'nome_usuario': agente.nome,  # Assumindo que o modelo 'Agente' tem o campo 'nome'
        'medicamentos_com_stock_baixo': medicamentos_com_stock_baixo
    })





def home_boss(request):
    agente = Agente.objects.get(id=request.session.get('id_utlizador'))
    medicamentos_com_stock_baixo = Stock.objects.filter(s_total__lt=models.F('s_min')).select_related('medicamento')
    return render(request, 'boss/home_page.html', {
        'nome_usuario': agente.nome,  # Assumindo que o modelo 'Agente' tem o campo 'nome'
        'medicamentos_com_stock_baixo': medicamentos_com_stock_baixo
    })








#------------------------UTENTE----------------------



def create_utente(request):
    # Recuperar o tipo de utilizador da sessão
    user_type = request.session.get('user_type', 'guest')  # 'guest' como valor padrão

    if request.method == 'POST':
        id = request.POST.get('id')
        nome = request.POST.get('nome')
        apelido = request.POST.get('apelido')
        genero = request.POST.get('genero')
        morada = request.POST.get('morada')
        telemovel = request.POST.get('telemovel')
        email = request.POST.get('email')
        data_nascimento = request.POST.get('data_nascimento')  

        if not all([id, nome, apelido, genero, morada, telemovel, email, data_nascimento]):
            return render(request, 'create_utente.html', {
                'message': 'Todos os campos são obrigatórios!',
                'user_type': user_type
            })

        try:
            utente = Utente.objects.create(
                id=id,
                nome=nome,
                apelido=apelido,
                genero=genero,
                morada=morada,
                telemovel=telemovel,
                email=email,
                data_nascimento=data_nascimento 
            )
            return render(request, 'create_utente.html', {
                'message': f'Utente {utente.nome} {utente.apelido} criado com sucesso!',
                'user_type': user_type
            })
        except Exception as e:
            return render(request, 'create_utente.html', {
                'message': 'Erro ao criar utente: O Número de Utente e o email têm de ser únicos.',
                'user_type': user_type
            })

    return render(request, 'create_utente.html', {'user_type': user_type})





def utente_info(request):
    user_type = request.session.get('user_type', 'guest')  # 'guest' como valor padrão
    try:
        # Verificar se o ID do utente está armazenado na sessão
        utente_id = request.session.get('utente_id')
        if not utente_id:
            messages.error(request, "Não foi possível encontrar as informações do utente.")
            return render(request, 'login_page.html', {
                'message': 'Utente não foi encontrado',
                'user_type': user_type
            })
        
        utente = Utente.objects.get(id=utente_id)

        consultas = Consulta.objects.filter(utente=utente).select_related('agente')

        # Verificar se o botão "Mostrar todas" foi pressionado
        mostrar_todas = request.GET.get('mostrar_todas') == 'true'
        if not mostrar_todas:
            # Aplicar filtro de data, se necessário
            consulta_data = request.GET.get('data')
            if consulta_data:
                consultas = consultas.filter(data_hora__date=consulta_data)

        return render(request, 'utente_info.html', {
            'message': f'Utente {utente.nome} encontrado com sucesso',
            'utente': utente,
            'consultas': consultas,  # Passar as consultas filtradas ou todas as associadas
            'user_type': user_type
        })
        
    except Utente.DoesNotExist:
        messages.error(request, "Utente não encontrado.")
        return render(request, 'login_page.html', {
            'message': 'Utente não foi encontrado',
            'user_type': user_type
        })
    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")
        return render(request, 'login_page.html', {
            'message': 'Ocorreu um erro ao processar a requisição.',
            'user_type': user_type
        })
    



    
def editar_utente(request):
    try:
        # Verificar se o ID do utente está armazenado na sessão
        utente_id = request.session.get('utente_id')
        if not utente_id:
            messages.error(request, "Não foi possível encontrar as informações do utente.")
            return redirect('login')

        # Procurar informações do utente com o ID armazenado
        utente = get_object_or_404(Utente, id=utente_id)

        if request.method == 'POST':
            # Receber os dados do formulário
            utente.nome = request.POST.get('nome', utente.nome)
            utente.apelido = request.POST.get('apelido', utente.apelido)
            utente.genero = request.POST.get('genero', utente.genero)
            utente.morada = request.POST.get('morada', utente.morada)
            utente.telemovel = request.POST.get('telemovel', utente.telemovel)
            utente.email = request.POST.get('email', utente.email)
            
            # Validar e guardar as alterações
            if utente.nome and utente.telemovel and utente.email:
                utente.save()
                messages.success(request, "Informações atualizadas com sucesso!")
                return redirect('utente_info')  # Redirecionar para a página de informações do utente
            else:
                messages.error(request, "Todos os campos são obrigatórios!")

        return render(request, 'editar_utente.html', {'utente': utente})

    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")
        return redirect('login')




def procurar_utente(request):
    user_type = request.session.get('user_type', 'guest')
    query = request.GET.get('query', '').strip()
    mensagem = None
    utente = None
    utente_nao_existe = False  # Variável para indicar se o utente não existe

    if query:
        try:
            # Tenta procurar o utente pelo ID
            utente = Utente.objects.get(id=query)
        except Utente.DoesNotExist:
            # Procurar pelo nome
            utente = Utente.objects.filter(nome__icontains=query).first()

        if not utente:
            mensagem = "Utente não encontrado. Experimente outro ID."
            utente_nao_existe = True  # Marca como True caso não encontra o utente
        else:
            request.session['utente_id'] = str(utente.id)

    return render(request, 'procurar_utente.html', {
        'utente': utente,
        'mensagem': mensagem,
        'utente_nao_existe': utente_nao_existe,
        'user_type': user_type 
    })






#------------------------Consulta----------------------

def create_consulta(request):
    utentes = Utente.objects.all()
    medicamentos = Medicamento.objects.prefetch_related('stock_set')

    user_type = request.session.get('user_type')
    agente_id = request.session.get('id_utlizador')

    if user_type not in ['médico', 'boss']:
        return render(request, 'create_consulta.html', {
            'message': "Apenas médicos ou o administrador podem criar consultas.",
            'utentes': utentes,
            'medicamentos': medicamentos,
            'user_type': user_type
        })

    if request.method == 'POST':
        descricao_consulta = request.POST.get('descricao')
        utente_id = request.POST.get('utente')
        utente = get_object_or_404(Utente, id=utente_id)

        agente = get_object_or_404(Agente, id=agente_id)

        descricao_receita = request.POST.get('descricao_receita')
        medicamentos_ids = request.POST.getlist('medicamentos')

        receita = None  # Inicializa a variável de receita

        # Verificação se há medicamentos e se a receita foi fornecida
        if descricao_receita:
            if not medicamentos_ids:
                return render(request, 'create_consulta.html', {
                    'message': "Uma receita deve ter ao menos um medicamento associado.",
                    'utentes': utentes,
                    'medicamentos': medicamentos,
                    'user_type': user_type
                })

            # Primeiro verificamos os stocks dos medicamentos
            with transaction.atomic():
                for medicamento_id in medicamentos_ids:
                    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
                    stock = medicamento.stock_set.first()
                    quantidade = int(request.POST.get(f'quantidade_{medicamento_id}', 1))

                    # Verificar se a quantidade solicitada excede o stock disponível
                    if not stock or quantidade > stock.s_total:
                        return render(request, 'create_consulta.html', {
                            'message': f"Não há stock suficiente para {medicamento.nome}. Quantidade solicitada: {quantidade}.",
                            'utentes': utentes,
                            'medicamentos': medicamentos,
                            'user_type': user_type
                        })

                # Criação da receita
                receita = Receita.objects.create(descricao=descricao_receita)

                # Atualização de stock e associação dos medicamentos
                for medicamento_id in medicamentos_ids:
                    medicamento = get_object_or_404(Medicamento, id=medicamento_id)
                    stock = medicamento.stock_set.first()
                    quantidade = int(request.POST.get(f'quantidade_{medicamento_id}', 1))

                    # Atualização do stock
                    stock.s_total -= quantidade
                    stock.save()
                    receita.medicamentos.add(medicamento)

                receita.save()

        consulta = Consulta.objects.create(
                utente=utente,
                agente=agente,
                descricao=descricao_consulta,
                data_hora=now()
            )
        if receita:
            consulta.receitas.add(receita)

            return render(request, 'create_consulta.html', {
                'message': "Consulta criada com sucesso com receita associada!",
                'utentes': utentes,
                'medicamentos': medicamentos,
                'user_type': user_type
            })
        else:
            return render(request, 'create_consulta.html', {
                'message': "A consulta foi criada sem receita associada.",
                'utentes': utentes,
                'medicamentos': medicamentos,
                'user_type': user_type
            })

    return render(request, 'create_consulta.html', {
        'utentes': utentes,
        'medicamentos': medicamentos,
        'user_type': user_type
    })








#------------------------AGENTE----------------------


def create_agente(request):
    user_type = request.session.get('user_type', 'guest')
    if request.method == 'POST':
        id = request.POST.get('id')
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')
        data_nascimento = request.POST.get('data_nascimento')

        if not nome or not cargo or not data_nascimento:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'create_agente.html')

        try:
            agente = Agente.objects.create(
                id=id, nome=nome, cargo=cargo, data_nascimento=data_nascimento
            )
            return render(request, 'create_agente.html', {
                'message': f'Agente {agente.nome} criado com sucesso!',
                'user_type': user_type
            })
        except Exception as e:
            return render(request, 'create_agente.html', {
                'message': 'Erro ao criar agente: O ID tem de ser único.',
                'user_type': user_type
            })

    return render(request, 'create_agente.html')




def agente_info(request):
    user_type = request.session.get('user_type', 'guest')  # Valor padrão: 'guest'
    
    try:
        agente_id = request.session.get('id_utlizador')
        if not agente_id or user_type not in ['médico', 'enfermeiro', 'farmacêutico', 'boss']:
            messages.error(request, "Não foi possível encontrar as informações do Agente.")
            return render(request, 'login_page.html', {
                'message': 'Agente não foi encontrado',
                'user_type': user_type
            })
        
        agente = Agente.objects.get(id=agente_id)

        consultas = Consulta.objects.filter(agente=agente).select_related('utente')

        mostrar_todas = request.GET.get('mostrar_todas', 'false').lower() in ['true', '1']
        if not mostrar_todas:
            # Filtro opcional de data
            consulta_data = request.GET.get('data')
            if consulta_data:
                consultas = consultas.filter(data_hora__date=consulta_data)

        return render(request, 'agente_info.html', {
            'message': f"{agente.cargo} {agente.nome} encontrado com sucesso",
            'agente': agente,
            'consultas': consultas,
            'user_type': user_type
        })
        
    except Agente.DoesNotExist:
        messages.error(request, "Agente não encontrado.")
        return render(request, 'login_page.html', {
            'message': 'Utente não foi encontrado',
            'user_type': user_type
        })
    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")
        return render(request, 'login_page.html', {
            'message': 'Ocorreu um erro ao processar a requisição.',
            'user_type': user_type
        })

def procurar_agente(request):
    query = request.GET.get('query', '').strip()
    mensagem = None
    agente = None
    agente_nao_existe = False
    user_type = request.session.get('user_type', 'guest')

    if query:
        try:
            agente = Agente.objects.get(id=query)
        except Agente.DoesNotExist:
            agente = Agente.objects.filter(nome__icontains=query).first()

        if agente:
            request.session['id_utlizador'] = str(agente.id)
            
        else:
            mensagem = "Agente não encontrado."
            agente_nao_existe = True
        
            

    return render(request, 'procurar_agente.html', {
        'agente': agente,
        'mensagem': mensagem,
        'agente_nao_existe': agente_nao_existe,
        'user_type': user_type,
    })


#--------------------FARMACEUTICO-----------------------------------

def farmaceutico_info(request):
    user_type = request.session.get('user_type', 'guest')  # Valor padrão: 'guest'
    
    try:
        farma_id = request.session.get('id_utlizador')
        if not farma_id or user_type not in ['médico', 'enfermeiro', 'farmacêutico', 'boss']:
            messages.error(request, "Não foi possível encontrar as informações do Farmaceûtico.")
            return render(request, 'login_page.html', {
                'message': 'Farmacêutico não foi encontrado',
                'user_type': user_type
            })
        
        farma = Agente.objects.get(id=farma_id)

        return render(request, 'farmaceutico_info.html', {
            'message': f"{farma.cargo} {farma.nome} encontrado com sucesso",
            'agente': farma,
            'user_type': user_type
        })
        
    except Agente.DoesNotExist:
        messages.error(request, "Agente não encontrado.")
        return render(request, 'login_page.html', {
            'message': 'Farmacêutico não foi encontrado',
            'user_type': user_type
        })
    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")
        return render(request, 'login_page.html', {
            'message': 'Ocorreu um erro ao processar a requisição.',
            'user_type': user_type
        })





#------------------------MEDICAMENTO----------------------




def create_medicamento(request):
    # Recuperar o tipo de utilizador da sessão
    user_type = request.session.get('user_type', 'guest')  # Valor padrão: 'guest'

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        s_min = request.POST.get('s_min')
        s_max = request.POST.get('s_max')
        s_total = request.POST.get('s_total')
        fornecedor_nome = request.POST.get('fornecedor')  # Nome do fornecedor enviado no formulário

        if not all([nome, descricao, s_min, s_max, s_total, fornecedor_nome]):
            return render(request, 'create_medicamento.html', {
                'message': 'Todos os campos são obrigatórios!',
                'user_type': user_type
            })

        try:
            if Medicamento.objects.filter(nome=nome).exists():
                return render(request, 'create_medicamento.html', {
                    'message': f'O medicamento "{nome}" já existe na base de dados!',
                    'user_type': user_type
                })
            with transaction.atomic():
                # Verificar se o fornecedor existe; se não, criar um novo
                fornecedor, created = Fornecedor.objects.get_or_create(nome=fornecedor_nome)

                # Criar o medicamento
                medicamento = Medicamento.objects.create(nome=nome, descricao=descricao)

                # Criar o stock e associar o fornecedor
                stock = Stock.objects.create(
                    medicamento=medicamento,
                    s_min=int(s_min),
                    s_max=int(s_max),
                    s_total=int(s_total),
                )
                stock.fornecedores.add(fornecedor)

            message = f'Medicamento {medicamento.nome} criado com sucesso!'
            if created:
                message += f' Fornecedor "{fornecedor.nome}" foi adicionado à base de dados.'

            return render(request, 'create_medicamento.html', {
                'message': message,
                'user_type': user_type
            })
        except Exception as e:
            return render(request, 'create_medicamento.html', {
                'message': f'Erro ao criar medicamento: {str(e)}',
                'user_type': user_type
            })

    # Passar lista de fornecedores disponíveis para o template
    fornecedores = Fornecedor.objects.all()
    return render(request, 'create_medicamento.html', {
        'user_type': user_type,
        'fornecedores': fornecedores
    })







def medicamento_info(request):
    user_type = request.session.get('user_type', 'guest')
    medicamento_id = request.session.get('medicamento_id')

    if not medicamento_id:
        messages.error(request, "Medicamento não encontrado.")
        return redirect('procurar_medicamento')

    try:
        medicamento = Medicamento.objects.get(id=medicamento_id)
        stock = Stock.objects.filter(medicamento=medicamento).first()
        
        
        # Se houver stock, procurar os fornecedores
        fornecedores = stock.fornecedores.all() if stock else []
        print(fornecedores)

        return render(request, 'medicamento_info.html', {
            'medicamento': medicamento,
            'stock': stock,
            'fornecedores': fornecedores,
            'user_type': user_type,
        })
    except Medicamento.DoesNotExist:
        messages.error(request, "Medicamento não encontrado.")
        return redirect('procurar_medicamento')
    except Exception as e:
        messages.error(request, f"Erro ao buscar medicamento: {e}")
        return redirect('procurar_medicamento')

    






def procurar_medicamento(request):
    user_type = request.session.get('user_type', 'guest')
    # Obtém o termo da pesquisa a partir do parâmetro GET
    query = request.GET.get('query', '').strip()
    medicamento = None
    stock = None
    fornecedores = []  # Inicializa a lista de fornecedores
    message = None

    if query:
        # Tenta procurar o medicamento pelo nome
        try:
            medicamento = Medicamento.objects.get(nome__icontains=query)
            request.session['medicamento_id'] = medicamento.id
            # Procura o stock relacionado ao medicamento
            stock = Stock.objects.filter(medicamento=medicamento).first()
            fornecedores = stock.fornecedores.all() if stock else []
            
            if not stock:
                message = "Nenhum stock encontrado para este medicamento."
        except Medicamento.DoesNotExist:
            message = "Medicamento não encontrado."

    if medicamento and stock:
        return render(request, 'medicamento_info.html', {
            'medicamento': medicamento,
            'stock': stock,
            'fornecedores': fornecedores,  # Adiciona fornecedores ao contexto
            'user_type': user_type
        })
    else:
        return render(request, 'procurar_medicamento.html', {
            'query': query,
            'message': message,
            'user_type': user_type
        })





def editar_medicamento(request):
    try:
        # Verificar se o ID do medicamento está armazenado na sessão
        medicamento_id = request.session.get('medicamento_id')
        if not medicamento_id:
            messages.error(request, "Não foi possível encontrar o medicamento.")
            return redirect('procurar_medicamento_ou_stock')

        # Procurar informações do medicamento e stocks associados
        medicamento = get_object_or_404(Medicamento, id=medicamento_id)
        stock = Stock.objects.filter(medicamento=medicamento).first()  # Primeiro registo de stock associado

        # Procurar fornecedores associados ao stock
        fornecedores = stock.fornecedores.all() if stock else []

        if request.method == 'POST':
            # Atualizar informações do medicamento
            medicamento.nome = request.POST.get('nome', medicamento.nome)
            medicamento.descricao = request.POST.get('descricao', medicamento.descricao)
            
            # Atualizar informações do stock
            if stock:
                stock.s_min = request.POST.get('s_min', stock.s_min)
                stock.s_max = request.POST.get('s_max', stock.s_max)
                stock.s_total = request.POST.get('s_total', stock.s_total)
                
                # Validar stock
                if not stock.s_min or not stock.s_max or not stock.s_total:
                    messages.error(request, "Todos os campos de stock são obrigatórios.")
                    return render(request, 'editar_medicamento.html', {
                        'medicamento': medicamento,
                        'stock': stock,
                        'fornecedores': fornecedores,
                    })

                # Guardar stock
                stock.save()

            # Guadar medicamento
            medicamento.save()
            messages.success(request, "Medicamento e stock atualizados com sucesso!")
            return redirect('medicamento_info')

        return render(request, 'editar_medicamento.html', {
            'medicamento': medicamento,
            'stock': stock,
            'fornecedores': fornecedores,  # Passar os fornecedores para o template
        })

    except Exception as e:
        messages.error(request, f"Ocorreu um erro: {e}")
        return redirect('procurar_medicamento_ou_stock')




#------------------------STOCK----------------------




def adicionar_stock(request):
    if request.method == "POST":
        medicamento_id = request.POST.get("medicamento")
        quantidade = int(request.POST.get("quantidade"))

        # Verifica se o medicamento existe
        medicamento = get_object_or_404(Medicamento, id=medicamento_id)
        stock = Stock.objects.filter(medicamento=medicamento).first()

        if not stock:
            messages.error(request, "Não há stock associado a este medicamento.")
            return redirect("adicionar_stock")

        # Verifica se a adição ultrapassa o limite máximo
        if stock.s_total + quantidade > stock.s_max:
            messages.error(
                request, 
                f"Não é possível adicionar {quantidade} unidades ao stock de {medicamento.nome}. O stock máximo é {stock.s_max}."
            )
            return redirect("adicionar_stock")
        
        fornecedor_selecionado = request.POST.get("fornecedor")
        if fornecedor_selecionado not in [fornecedor.nome for fornecedor in stock.fornecedores.all()]:
            messages.error(
                request,
                f"O fornecedor selecionado ({fornecedor_selecionado}) não corresponde a um dos fornecedores registados."
            )
            return redirect("adicionar_stock")

        # Atualiza o stock total
        stock.s_total += quantidade
        stock.save()

        # Mensagem de sucesso
        messages.success(request, f"Foram adicionadas {quantidade} unidades ao stock de {medicamento.nome}.")
        return redirect("adicionar_stock")

    # Obtém todos os medicamentos e seus stocks para o formulário
    medicamentos = Medicamento.objects.all()
    medicamentos_com_stock = []
    for med in medicamentos:
        stock = Stock.objects.filter(medicamento=med).first()
        if stock:
            # Se o fornecedor for uma relação muitos-para-muitos, extraímos os nomes dos fornecedores
            fornecedores = [fornecedor.nome for fornecedor in stock.fornecedores.all()]
            medicamentos_com_stock.append({
                "medicamento": med,
                "stock": stock,
                "fornecedores": fornecedores,  # Passamos uma lista de nomes de fornecedores
            })

    # Obtém o tipo de utilizador (user_type) da sessão
    user_type = request.session.get('user_type', '')  # Default para uma string vazia se não existir

    # Passa os medicamentos, fornecedores e o tipo de utilizador para o template
    return render(request, "adicionar_stock.html", {
        "medicamentos_com_stock": medicamentos_com_stock,
        "user_type": user_type,  # Adiciona o user_type ao contexto
    })




def vender_medicamento(request):
    user_type = request.session.get('user_type', 'guest')
    if request.method == "POST":
        medicamento_id = request.POST.get("medicamento")
        quantidade = int(request.POST.get("quantidade"))

        # Verifica se o medicamento existe
        medicamento = get_object_or_404(Medicamento, id=medicamento_id)
        stock = Stock.objects.filter(medicamento=medicamento).first()

        if not stock:
            messages.error(request, "Não há stock associado a este medicamento.")
            return redirect("vender_medicamento")

        # Verifica se a adição ultrapassa o limite máximo
        if stock.s_total - quantidade < 0:
            messages.error(request, f"Não é possível vender {quantidade} unidades de {medicamento.nome}. Só tem disponível {stock.s_total}.")
            return redirect("vender_medicamento")

        # Atualiza o stock total
        stock.s_total -= quantidade
        stock.save()

        # Mensagem de sucesso
        messages.success(request, f"Foram adicionadas {quantidade} unidades ao stock de {medicamento.nome}.")
        return redirect("vender_medicamento")

    # Obtém todos os medicamentos e seus stocks para o formulário
    medicamentos = Medicamento.objects.all()
    medicamentos_com_stock = [
        {"medicamento": med, "stock": Stock.objects.filter(medicamento=med).first()} for med in medicamentos
    ]
    return render(request, "vender_medicamento.html", {"medicamentos_com_stock": medicamentos_com_stock, "user_type" : user_type })




#------------------------ADMIN----------------------



def listar_opcao(request):
    # Obtém a opção selecionada no formulário
    opcao = request.GET.get('opcao', '').strip()
    message = None
    dados = None

    # Define a lógica para cada opção
    if opcao == 'utentes':
        dados = Utente.objects.all()
    elif opcao == 'agentes':
        dados = Agente.objects.all()
    elif opcao == 'medicamentos':
        dados = Medicamento.objects.all()
    elif opcao:
        message = "Opção inválida. Por favor, selecione uma válida."

    return render(request, 'listar.html', {
        'opcao': opcao,
        'dados': dados,
        'message': message,
    })




def estatisticas(request):
    message = ""
    selected_option = ""

    if request.method == 'POST':
        option = request.POST.get('option', '')
        selected_option = option

        if option == 'total_utentes':
            total_utentes = Utente.objects.count()
            message = f"Temos {total_utentes} utentes."

        elif option == 'total_agentes':
            total_agentes = Agente.objects.count()
            message = f"Temos {total_agentes} agentes."

        elif option == 'medicamento_mais_stock':
            stock_info = Stock.objects.annotate(
                total_stock=Max('s_total')
            ).order_by('-total_stock').first()
            if stock_info:
                message = (f"O medicamento com maior stock é {stock_info.medicamento.nome} "
                        f"com {stock_info.s_total} unidades.")
            else:
                message = "Não há medicamentos no stock."

        elif option == 'utentes_mais_consultas':
            utentes = Utente.objects.annotate(
                total_consultas=Count('consulta')
            ).order_by('-total_consultas')
            if utentes.exists():
                max_consultas = utentes.first().total_consultas
                utentes_com_mais_consultas = utentes.filter(total_consultas=max_consultas)
                nomes = ", ".join([f"{u.nome} {u.apelido}" for u in utentes_com_mais_consultas])
                message = (f"Os utentes com mais consultas ({max_consultas} consultas): {nomes}")
            else:
                message = "Nenhum utente possui consultas registadas."
                
        elif option == 'maior_fornecedor':
            fornecedores = Fornecedor.objects.annotate(
                total_medicamentos = Count('stocks')
            ).order_by('-total_medicamentos')
            if fornecedores.exists():
                max_medicamentos = fornecedores.first().total_medicamentos
                fornecedor_com_mais_medicamentos = fornecedores.filter(total_medicamentos=max_medicamentos)
                nomes1 = ", ".join([f"{f.nome}" for f in fornecedor_com_mais_medicamentos])
                message = (f"O fornecedor que mais fornece medicamentos ({max_medicamentos} medicamentos): {nomes1}")
            else:
                message = "Nenhum fornecedor possui venda de medicamentos."
                
        elif option == 'medicamento_mais_usado':
            medicamentos = Medicamento.objects.annotate(
                uso_total=Count('receitas')
            ).order_by('-uso_total') 

            if medicamentos.exists():
                max_uso = medicamentos.first().uso_total
                medicamentos_mais_usados = medicamentos.filter(uso_total=max_uso) 
                nomes_medicamentos = ", ".join([m.nome for m in medicamentos_mais_usados])
                message = f"O(s) medicamento(s) mais usado(s) ({max_uso} usos): {nomes_medicamentos}"
            else:
                message = "Nenhum medicamento foi usado em receitas."

        else:
            message = "Opção inválida. Por favor, tente novamente."

    return render(request, 'estatisticas.html', {'message': message, 'selected_option': selected_option})





def adicionar_fornecedor(request):
    if request.method == "POST":
        medicamento_id = request.POST.get("medicamento")
        fornecedor_nome = request.POST.get("fornecedor")

        if medicamento_id and fornecedor_nome:
            medicamento = get_object_or_404(Medicamento, id=medicamento_id)

            # Verificar se existe um Stock associado ao Medicamento
            stock = Stock.objects.filter(medicamento=medicamento).first()
            if not stock:
                mensagem = f"Erro: Não há stock associado ao medicamento '{medicamento.nome}'."
                return render(request, "adicionar_fornecedor.html", {
                    "mensagem": mensagem,
                    "medicamentos": Medicamento.objects.all()
                })

            # Criar o fornecedor se não existir
            fornecedor, created = Fornecedor.objects.get_or_create(nome=fornecedor_nome)

            # Adicionar o fornecedor ao Stock
            stock.fornecedores.add(fornecedor)

            # Mensagem de sucesso
            mensagem = f"Fornecedor '{fornecedor.nome}' adicionado ao medicamento '{medicamento.nome}' com sucesso."
            if created:
                mensagem += f" Fornecedor '{fornecedor.nome}' foi criado."
        else:
            mensagem = "Erro: Preencha todos os campos corretamente."

        return render(request, "adicionar_fornecedor.html", {
            "mensagem": mensagem,
            "medicamentos": Medicamento.objects.all()
        })

    # Carregar a lista de medicamentos disponíveis
    medicamentos = Medicamento.objects.all()
    return render(request, "adicionar_fornecedor.html", {"medicamentos": medicamentos})
    
