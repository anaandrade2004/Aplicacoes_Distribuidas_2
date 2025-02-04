from django.db import models
import uuid

# Create your models here.

class Pessoa(models.Model):
    id = models.CharField(max_length=36, primary_key=True, unique=True)
    data_nascimento = models.DateField()

    def __str__(self):
        return f"Pessoa {self.id}"

class Agente(Pessoa):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Utente(Pessoa):
    nome = models.CharField(max_length=100)
    apelido = models.CharField(max_length=100)
    genero = models.CharField(max_length=20)
    morada = models.CharField(max_length=255)
    telemovel = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nome} {self.apelido}"

class Receita(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, editable=False, primary_key=True)
    descricao = models.CharField(max_length=255)
    medicamentos = models.ManyToManyField('Medicamento', related_name='receitas', blank=True)  # Relaciona com medicamentos

    def __str__(self):
        return self.descricao


class Consulta(models.Model):
    id_consulta = models.CharField(max_length=36, default=uuid.uuid4, editable=False, primary_key=True)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    agente = models.ForeignKey(Agente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    receitas = models.ManyToManyField(Receita, related_name='consultas', blank=True)

    def __str__(self):
        return f"Consulta ID: {self.id_consulta}, Utente: {self.utente}, Agente: {self.agente}, DataHora: {self.data_hora}"

class Medicamento(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, editable=False, primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    s_min = models.IntegerField()
    s_max = models.IntegerField()
    s_total = models.IntegerField()
    fornecedores = models.ManyToManyField(Fornecedor, related_name='stocks')
    def __str__(self):
        return f"Medicamento: {self.medicamento.nome} - Total: {self.s_total}"
