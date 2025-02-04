from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from processoclinico.views import *

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Agente', AgenteViewSet)
router.register(r'Utente', UtenteViewSet)
router.register(r'Receita', ReceitaViewSet)
router.register(r'Consulta', ConsultaViewSet)
router.register(r'Stock', StockViewSet)
router.register(r'Medicamento', MedicamentoViewSet)
router.register(r'Fornecedores', FornecedorViewSet)
urlpatterns = [
    path('register/', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('create-agente/', create_agente, name='create_agente'),
    path('create-consulta/', create_consulta, name='create_consulta'),
    path('create-medicamento/', create_medicamento, name='create_medicamento'),
    path('create-utente/', create_utente, name='create_utente'),
    path('utente-info/', utente_info, name='utente_info'),
    path('home/utente/', home_utente, name='home_page_utente'),
    path('home/medico/', home_medico, name='home_page_medico'),
    path('home/farmacêutico/', home_farma, name='home_page_farma'),
    path('home/boss/', home_boss, name='home_page_boss'),
    path('estatisticas/', estatisticas, name='estatisticas'),
    path('editar-utente/', editar_utente, name='editar_utente'),
    path('procurar-utente/', procurar_utente, name='procurar_utente'),
    path('procurar-agente/', procurar_agente, name='procurar_agente'),
    path('procurar-medicamento/', procurar_medicamento, name='procurar_medicamento'),
    path('medicamento-info/', medicamento_info, name='medicamento_info'),
    path('editar-medicamento/', editar_medicamento, name='editar_medicamento'),
    path('adicionar-stock/',adicionar_stock, name='adicionar_stock'),
    path('vender-medicamento/',vender_medicamento, name='vender_medicamento'),
    path('listar-opcao/', listar_opcao, name='listar_opcao'),
    path('adicionar-fornecedor/',adicionar_fornecedor,name='adicionar_fornecedor'),
    path('agente-info/', agente_info, name='agente_info'),
    path('farmaceutico-info/', farmaceutico_info, name='farmaceutico_info'),
    path('', login_page, name='login')
]