from django.urls import path, include
from .views import BbDetailView, BbByRubricView, index, edit, delete, profile_bb_add, profile, APIRubrics,\
    APIRubricDetail, APIRubricViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('rubrics', APIRubricViewSet)

urlpatterns = [
    path('add/', profile_bb_add, name='profile_bb_add'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('', index, name='index'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('profile/', profile, name='profile'),
    path('api/rubrics/', APIRubrics.as_view()),
    path('api/rubrics/<int:pk>', APIRubricDetail.as_view()),
    path('api/', include(router.urls)),
]
