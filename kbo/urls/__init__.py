from django.urls import path, include

# All Season
# /hitter/
# /pitcher/
# /hitter/<int:player_id>/
# /pitcher/<int:player_id>/
# /team/<int:team_id>/hitter/
# /team/<int:team_id>/pitcher/

# A Specific Season
# /year/<int:year>/hitter/
# /year/<int:year>/pitcher/
# /year/<int:year>/hitter/<int:player_id>/
# /year/<int:year>/pitcher/<int:player_id>/
# /year/<int:year>/team/<int:team_id>/hitter/
# /year/<int:year>/team/<int:team_id>/pitcher/

urlpatterns = [
    path('fbv/', include('kbo.urls.function_urls')),
    path('cbv/', include('kbo.urls.class_urls')),
]