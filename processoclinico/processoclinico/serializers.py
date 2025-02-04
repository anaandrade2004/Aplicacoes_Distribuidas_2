from django.contrib.auth.models import Group, User
from processoclinico.models import *
from rest_framework import serializers
from django.db import models

# Serializer para Pessoa
class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ['id', 'data_nascimento']

# Serializer para Agente
class AgenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente
        fields = ['id', 'nome', 'data_nascimento', 'cargo']

# Serializer para Utente
class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['id', 'nome', 'apelido', 'morada', 'data_nascimento', 'telemovel', 'genero', 'email']


class UtenteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['id']

class AgenteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agente
        fields = ['id']

# Serializer para Fornecedor 
class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id', 'nome']  

# Serializer para Medicamento
class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ['id', 'nome', 'descricao'] 

# Serializer para Stock
class StockSerializer(serializers.ModelSerializer):
    medicamento = MedicamentoSerializer()  
    fornecedores = FornecedorSerializer(many=True)  # Lista de fornecedores

    class Meta:
        model = Stock
        fields = ['id', 'medicamento', 's_min', 's_max', 's_total', 'fornecedores']


# Serializer para Receita
class ReceitaSerializer(serializers.ModelSerializer):
    medicamentos = MedicamentoSerializer(many=True)  # Recebe vários medicamentos

    class Meta:
        model = Receita
        fields = ['id', 'descricao', 'medicamentos']

# Serializer para Consulta
class ConsultaSerializer(serializers.ModelSerializer):
    utente = serializers.PrimaryKeyRelatedField(queryset=Utente.objects.all())
    agente = serializers.PrimaryKeyRelatedField(queryset=Agente.objects.all())  # Retorna apenas o ID do Agente
    receitas = ReceitaSerializer(many=True)  # Relaciona as receitas

    class Meta:
        model = Consulta
        fields = ['id_consulta', 'utente', 'agente', 'data_hora', 'descricao', 'receitas']
