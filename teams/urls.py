from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("<int:team_id>/viewTeam", views.view_team, name="viewTeam"),
    path('<int:team_id>/viewNFLTeam', views.view_nflTeam, name="viewNFLTeam"),
    path('submitTeam', views.submit_team, name="submitTeam"),
    path('<int:pos>/compare', views.compare, name="compare"),
    path('<int:pos>/updatePlayer', views.update_player, name="updatePlayer"),
    path('<int:pos>/stats', views.stats, name="stats"),
    path('viewPlayers', views.players, name="viewPlayers"),
    path('<int:pos>/updateStats', views.update_stats, name="updateStats"),
    path('updateGame', views.game, name="updateGame"),
    path('viewSchedule', views.schedule, name="viewSchedule"),
    path('<int:game>/updateSchedule', views.update_schedule, name="updateSchedule"),
    path('<int:pos>/savePlayerStats', views.save_player, name="savePlayerStats"),
    path('<int:pos>/saveGameStats', views.save_game, name="saveGameStats"),
    path('viewCompare', views.view_compare, name="viewCompare"),
    path("<int:pos>/selectPick", views.select_pick, name="selectPick"),
]
