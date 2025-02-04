import random
from django.apps import AppConfig
from django.db.models.signals import post_migrate
import uuid
fornecedor_nomes = ["Johnson & Johnson", "Medinfar", "Medicanorte", "Bial", "Pfizer", "AbbVie"]

def generate_random_id():
    return f"{random.randint(100000000, 999999999)}"

def generate_random_fornecedor():
    return f"{random.choice(list)}"

class ProcessoclinicoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'processoclinico'

    def ready(self):
        post_migrate.connect(initialize_data, sender=self)

def initialize_data(sender, **kwargs):
    from .models import Agente, Utente, Medicamento, Stock, Fornecedor

    # Criar administrador
    admin_data = {
        'id': 'admin123456789',
        'nome': 'Admin',
        'cargo': 'boss',
        'data_nascimento': '2000-01-01'
    }
    if not Agente.objects.filter(id=admin_data['id']).exists():
        Agente.objects.create(**admin_data)
        print("Administrador padrão criado com sucesso.")

    # Criar agentes
    agentes = [
        {'nome': 'Filipa Alves', 'cargo': 'médico', 'data_nascimento': '1985-02-10'},
        {'nome': 'Ricardo Pinto', 'cargo': 'enfermeiro', 'data_nascimento': '1990-05-15'},
        {'nome': 'Ana Sousa', 'cargo': 'médico', 'data_nascimento': '1982-08-20'},
        {'nome': 'Carlos Silva', 'cargo': 'enfermeiro', 'data_nascimento': '1987-12-25'},
        {'nome': 'João Martins', 'cargo': 'médico', 'data_nascimento': '1980-04-30'},
        {'nome': 'Maria Oliveira', 'cargo': 'enfermeiro', 'data_nascimento': '1989-09-10'},
        {'nome': 'Paula Costa', 'cargo': 'médico', 'data_nascimento': '1992-01-05'},
        {'nome': 'Jorge Rocha', 'cargo': 'enfermeiro', 'data_nascimento': '1986-11-15'},
        {'nome': 'Sofia Santos', 'cargo': 'farmacêutico', 'data_nascimento': '1984-03-22'},
        {'nome': 'Pedro Pereira', 'cargo': 'farmacêutico', 'data_nascimento': '1991-06-18'},
    ]
    for agente in agentes:
        agente['id'] = generate_random_id()
        if not Agente.objects.filter(id=agente['id']).exists():
            Agente.objects.create(**agente)
            print(f"Agente '{agente['nome']}' criado com sucesso.")

    # Criar utentes
    utentes = [
        {'nome': 'Filipa', 'apelido': 'Martins Silva', 'genero': 'Feminino', 'morada': 'Rua A, 123', 'telemovel': '912345678', 'email': 'filipa@example.com', 'data_nascimento': '1992-05-12'},
        {'nome': 'Ricardo', 'apelido': 'Costa Pereira', 'genero': 'Masculino', 'morada': 'Rua B, 456', 'telemovel': '913456789', 'email': 'ricardo@example.com', 'data_nascimento': '1985-03-08'},
        {'nome': 'Joana', 'apelido': 'Alves Souza', 'genero': 'Outro', 'morada': 'Rua C, 789', 'telemovel': '914567890', 'email': 'joana@example.com', 'data_nascimento': '1989-11-22'},
        {'nome': 'Carlos', 'apelido': 'Rodrigues Oliveira', 'genero': 'Masculono', 'morada': 'Rua D, 101', 'telemovel': '915678901', 'email': 'carlos@example.com', 'data_nascimento': '1978-09-04'},
        {'nome': 'Ana', 'apelido': 'Martins Lopes', 'genero': 'Outro', 'morada': 'Rua E, 202', 'telemovel': '916789012', 'email': 'ana@example.com', 'data_nascimento': '1990-06-15'},
        {'nome': 'João', 'apelido': 'Ferreira Melo', 'genero': 'Masculino', 'morada': 'Rua F, 303', 'telemovel': '917890123', 'email': 'joao@example.com', 'data_nascimento': '1994-02-02'},
        {'nome': 'Maria', 'apelido': 'Costa Pinto', 'genero': 'Feminino', 'morada': 'Rua G, 404', 'telemovel': '918901234', 'email': 'maria@example.com', 'data_nascimento': '1987-12-25'},
        {'nome': 'Paula', 'apelido': 'Rocha Barbosa', 'genero': 'Feminino', 'morada': 'Rua H, 505', 'telemovel': '919012345', 'email': 'paula@example.com', 'data_nascimento': '1986-04-10'},
        {'nome': 'José', 'apelido': 'Silva Almeida', 'genero': 'Outro', 'morada': 'Rua I, 606', 'telemovel': '920123456', 'email': 'jose@example.com', 'data_nascimento': '1993-07-18'},
        {'nome': 'Sofia', 'apelido': 'Pinto Santos', 'genero': 'Feminino', 'morada': 'Rua J, 707', 'telemovel': '921234567', 'email': 'sofia@example.com', 'data_nascimento': '1991-01-01'},
    ]
    for utente in utentes:
        utente['id'] = generate_random_id()
        if not Utente.objects.filter(id=utente['id']).exists():
            Utente.objects.create(**utente)
            print(f"Utente '{utente['nome']} {utente['apelido']}' criado com sucesso.")

    # Criar medicamentos e os seus stocks
    for nome in fornecedor_nomes:
        if not Fornecedor.objects.filter(nome=nome).exists():
            Fornecedor.objects.create(nome=nome)
            print(f"Fornecedor '{nome}' criado com sucesso.")

    # Criar medicamentos e os seus stocks
    medicamentos = [
        {'nome': 'Paracetamol', 'descricao': 'Usado para alívio de dores e febre.'},
        {'nome': 'Ibuprofeno', 'descricao': 'Medicamento anti-inflamatório para dor e febre.'},
        {'nome': 'Aspirina', 'descricao': 'Usado para dor e febre, além de propriedades anticoagulantes.'},
        {'nome': 'Amoxicilina', 'descricao': 'Antibiótico utilizado no tratamento de infecções bacterianas.'},
        {'nome': 'Omeprazol', 'descricao': 'Usado para tratar úlceras gástricas e refluxo ácido.'},
        {'nome': 'Dipirona', 'descricao': 'Utilizado para aliviar dor e febre.'},
        {'nome': 'Clonazepam', 'descricao': 'Medicamento ansiolítico utilizado para tratar crises de ansiedade.'},
        {'nome': 'Loratadina', 'descricao': 'Antialérgico usado para tratar sintomas de alergias.'},
        {'nome': 'Losartana', 'descricao': 'Usado para tratar hipertensão e insuficiência cardíaca.'},
        {'nome': 'Metformina', 'descricao': 'Medicamento para controle de diabetes tipo 2.'},
    ]

    fornecedores = list(Fornecedor.objects.all())  # Lista de fornecedores disponíveis

    for medicamento in medicamentos:
        medicamento['id'] = str(uuid.uuid4())
        if not Medicamento.objects.filter(id=medicamento['id']).exists():
            med = Medicamento.objects.create(**medicamento)
            print(f"Medicamento '{medicamento['nome']}' criado com sucesso.")
            
            # Criar Stock e associar fornecedores aleatórios
            stock_data = {
                'id': str(uuid.uuid4()),
                'medicamento': med,
                's_min': random.randint(10, 20),
                's_max': random.randint(50, 100),
                's_total': random.randint(20, 50),
            }
            stock = Stock.objects.create(**stock_data)
            fornecedores_escolhidos = random.sample(fornecedores,1)
            stock.fornecedores.set(fornecedores_escolhidos)
            stock.save()
            print(f"Stock para '{medicamento['nome']}' criado com sucesso com fornecedores: {', '.join(f.nome for f in fornecedores_escolhidos)}.")