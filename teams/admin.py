from django.contrib import admin

from .models import player, gameTeam, playerStats, kickerStats, defStats, seasonSchedule, weeklyRankings
# Register your models here.
admin.site.register(player)
admin.site.register(gameTeam)
admin.site.register(playerStats)
admin.site.register(kickerStats)
admin.site.register(defStats)
admin.site.register(seasonSchedule)
admin.site.register(weeklyRankings)