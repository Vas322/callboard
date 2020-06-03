from django.urls import path
from .views import BbDetailView, BbEditView, BbAddView, BbByRubricView, BbDeleteView, \
    BbIndexView, index, edit, delete

urlpatterns = [
    path('add/', BbAddView.as_view(), name='add'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('', index, name='index'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', delete, name='delete'),
]
