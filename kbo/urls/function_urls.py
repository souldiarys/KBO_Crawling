from django.urls import path

from ..views import hitter_all, hitter_id, hitter_year_all, hitter_year_id
from ..views import pitcher_all, pitcher_id, pitcher_year_all, pitcher_year_id
from ..views import team_hitter_all, team_pitcher_all, team_hitter_year, team_pitcher_year

urlpatterns = [
    path('hitter/', hitter_all),
    path('pitcher/', pitcher_all),
    path('hitter/<int:player_id>/', hitter_id),
    path('pitcher/<int:player_id>/', pitcher_id),
    path('year/<int:year>/hitter/', hitter_year_all),
    path('year/<int:year>/pitcher/', pitcher_year_all),
    path('year/<int:year>/hitter/<int:player_id>/', hitter_year_id),
    path('year/<int:year>/pitcher/<int:player_id>/', pitcher_year_id),
    path('team/<int:team_id>/hitter/', team_hitter_all),
    path('team/<int:team_id>/pitcher/', team_pitcher_all),
    path('year/<int:year>/team/<int:team_id>/hitter/', team_hitter_year),
    path('year/<int:year>/team/<int:team_id>/pitcher/', team_pitcher_year),
]