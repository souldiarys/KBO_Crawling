from django.urls import path

from ..views.class_views import hitter_all, hitter_id, hitter_year_all, hitter_year_id
from ..views.class_views import pitcher_all, pitcher_id, pitcher_year_all, pitcher_year_id
from ..views.class_views import team_hitter_all, team_pitcher_all, team_hitter_year, team_pitcher_year

urlpatterns = [
    path('hitter/', hitter_all.as_view()),
    path('pitcher/', pitcher_all.as_view()),
    path('hitter/<int:player_id>/', hitter_id.as_view()),
    path('pitcher/<int:player_id>/', pitcher_id.as_view()),
    path('year/<int:year>/hitter/', hitter_year_all.as_view()),
    path('year/<int:year>/pitcher/', pitcher_year_all.as_view()),
    path('year/<int:year>/hitter/<int:player_id>/', hitter_year_id.as_view()),
    path('year/<int:year>/pitcher/<int:player_id>/', pitcher_year_id.as_view()),
    path('team/<int:team_id>/hitter/', team_hitter_all.as_view()),
    path('team/<int:team_id>/pitcher/', team_pitcher_all.as_view()),
    path('year/<int:year>/team/<int:team_id>/hitter/', team_hitter_year.as_view()),
    path('year/<int:year>/team/<int:team_id>/pitcher/', team_pitcher_year.as_view()),
]