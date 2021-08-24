from .views import KBOHitterViewSet, KBOPitcherViewSet, KBOTeamViewSet

from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hitter', KBOHitterViewSet, basename='hitter')
router.register('pitcher', KBOPitcherViewSet, basename='pitcher')
router.register('team', KBOTeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
]