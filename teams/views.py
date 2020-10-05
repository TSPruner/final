from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

from .models import player, gameTeam, playerStats, kickerStats, defStats, seasonSchedule, weeklyRankings

# Create your views here.
def index(request):
    count = 0
    total = 0
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        username = None
        reg_user = False
        admin_user = False

    current_week =  seasonSchedule.objects.filter(week=1).only("currentWeek").first()
    week = current_week.currentWeek
    print(f"index week={week}, current_week={current_week}")
    games_started = False
    games_completed = False
    found = True
    try:
        team_all = gameTeam.objects.filter(week=week).order_by('userTeamId')
    except gameTeam.DoesNotExist:
        found = False
    print(f"team_all = {team_all}")
    if found:
        print(f"found = {found}")
        if team_all.exists():
            print(f"team_all.first().status={team_all.first().status}")
            if team_all.first().status == 3:
                games_started = True
                print(f"reg_user: games_started={games_started}")
                if reg_user:
                    team = gameTeam.objects.filter(week=week).filter(username=username).filter(status=3)
                else:
                    team = gameTeam.objects.filter(week=week).filter(status=3)
                if team.exists():
                    request.session['team_id'] = team.first().userTeamId
                    for position in team:
                        total = total + position.price
                        count = count + 1
                    request.session['team_count'] = count
                    request.session['team_total'] = str(total)
            elif team_all.first().status == 4:
                games_completed = True
                print(f"reg_user: games_started={games_started}")
                if reg_user:
                    team = gameTeam.objects.filter(week=week).filter(username=username).filter(status=4)
                else:
                    team = gameTeam.objects.filter(week=week).filter(status=4)
                if team.exists():
                    request.session['team_id'] = team.first().userTeamId
                    for position in team:
                        total = total + position.price
                        count = count + 1
                    request.session['team_count'] = count
                    request.session['team_total'] = str(total)

    if not games_started and not games_completed:
        if reg_user:
            team = gameTeam.objects.filter(username=username).filter(status=1)
            if team.exists():
                request.session['team_id'] = team.first().userTeamId
                for position in team:
                    total = total + position.price
                    count = count + 1
                request.session['team_count'] = count
                request.session['team_total'] = str(total)
            else:    
                request.session['team_count'] = 0
                request.session['team_total'] = 0
                found = True
                try:
                    team_all = gameTeam.objects.all().order_by('userTeamId')
                except gameTeam.DoesNotExist:
                    request.session['team_id'] = 0
                    found = False
                if found:
                    if team_all.exists():
                        request.session['team_id'] =  team_all.last().userTeamId + 1
                        if team_all.first().status == 3:
                            games_started = True
                            print(f"reg_user: games_started={games_started}")
                    else:
                        request.session['team_id'] = 0

    print(f"reg_user = {reg_user} and admin_user = {admin_user}")
    if reg_user or admin_user:
        print(f"games_completed={games_completed}")
        if games_completed:
            context = {
                "user": username,
                "reg_user": reg_user,
                "admin_user": admin_user,
                "team_id": 32,
                "completed": True,
                "teams": weeklyRankings.objects.all().order_by('ranking'),
            }
            return render(request, "teams/index.html", context)
        print(f"reg_user: reg_user={reg_user} and games_started={games_started}")
        if games_started:
            context = {
                "user": username,
                "reg_user": reg_user,
                "admin_user": admin_user,
                "team_id": 32,
                "started": True,
                "teams": weeklyRankings.objects.all().order_by('ranking'),
            }
            return render(request, "teams/index.html", context)
            
    if reg_user:
        team_id = request.session['team_id']
        count = request.session['team_count']
        print(f"reg_user: team_id = {team_id}, count = {count}")
        context = {
            "user": username,
            "reg_user": reg_user,
            "admin_user": admin_user,
            "team_id": team_id,
            "count": count,
            "teams": gameTeam.objects.filter(username=username).exclude(status=0).exclude(status=1).exclude(status=4).order_by('userTeamId'),
            "team_cart": gameTeam.objects.filter(username=username).filter(status=1).order_by('userTeamId').first(),
        }
    else:
        teams = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        context = {
            "user": username,
            "reg_user": reg_user,
            "admin_user": admin_user,
            "team_id": 32,
            "AFC": teams,
            "AFC0": player.objects.filter(teamId=0).order_by('position'),
            "AFC1": player.objects.filter(teamId=1).order_by('position'),
            "AFC2": player.objects.filter(teamId=2).order_by('position'),
            "AFC3": player.objects.filter(teamId=3).order_by('position'),
            "AFC4": player.objects.filter(teamId=4).order_by('position'),
            "AFC5": player.objects.filter(teamId=5).order_by('position'),
            "AFC6": player.objects.filter(teamId=6).order_by('position'),
            "AFC7": player.objects.filter(teamId=7).order_by('position'),
            "AFC8": player.objects.filter(teamId=8).order_by('position'),
            "AFC9": player.objects.filter(teamId=9).order_by('position'),
            "AFC10": player.objects.filter(teamId=10).order_by('position'),
            "AFC11": player.objects.filter(teamId=11).order_by('position'),
            "AFC12": player.objects.filter(teamId=12).order_by('position'),
            "AFC13": player.objects.filter(teamId=13).order_by('position'),
            "AFC14": player.objects.filter(teamId=14).order_by('position'),
            "AFC15": player.objects.filter(teamId=15).order_by('position'),
            "NFC": teams,
            "NFC0": player.objects.filter(teamId=16).order_by('position'),
            "NFC1": player.objects.filter(teamId=17).order_by('position'),
            "NFC2": player.objects.filter(teamId=18).order_by('position'),
            "NFC3": player.objects.filter(teamId=19).order_by('position'),
            "NFC4": player.objects.filter(teamId=20).order_by('position'),
            "NFC5": player.objects.filter(teamId=21).order_by('position'),
            "NFC6": player.objects.filter(teamId=22).order_by('position'),
            "NFC7": player.objects.filter(teamId=23).order_by('position'),
            "NFC8": player.objects.filter(teamId=24).order_by('position'),
            "NFC9": player.objects.filter(teamId=25).order_by('position'),
            "NFC10": player.objects.filter(teamId=26).order_by('position'),
            "NFC11": player.objects.filter(teamId=27).order_by('position'),
            "NFC12": player.objects.filter(teamId=28).order_by('position'),
            "NFC13": player.objects.filter(teamId=29).order_by('position'),
            "NFC14": player.objects.filter(teamId=30).order_by('position'),
            "NFC15": player.objects.filter(teamId=31).order_by('position'),
        }
    return render(request, "teams/index.html", context)

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first = request.POST["first"]
        last = request.POST["last"]
        try:
            user = User.objects.get(username=username)
            return render(request, "users/register.html", {"message": "Username already exists."})
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password, first_name=first, last_name=last)
            user.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/register.html", {"message": None})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/login.html", {"message": "Login with your credentials."})
       
def logout_view(request):
    request.session['order_count'] = 0
    request.session['order_total'] = 0
    request.session['order_id'] = 0
    logout(request)
    return render(request, "users/success.html", {"message": "User has been logged out."})

def select_pick(request, pos):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    team_id = request.session.get('team_id')
    total = float(request.session.get('team_total'))
    count = request.session.get('team_count')
    pick = gameTeam.objects.get(positionChoice=pos, userTeamId=team_id)
    player_id = pick.positionId
    if request.method == "POST":
        new_player = request.POST.get('player')
        print(f"select_pick new_player = {new_player}")
        try:
            team_player = player.objects.get(pk=new_player)
        except player.DoesNotExist:
            context = {
                "reg_user": reg_user,
                "tab": "view",
                "team_id": 32,
                "message": message,
            }
            return render(request, "teams/error.html", context)

        total = total - float(pick.price)
        total = total + float(team_player.price)
        if total < 13000:
            if pos == 6:
                stats = defStats.objects.get(playerId=new_player)
                pick_desc = str(team_player)
            elif pos == 8:
                stats = kickerStats.objects.get(playerId=new_player)
                pick_desc = str(team_player)
            else:
                stats = playerStats.objects.get(playerId=new_player)
                pick_desc = str(team_player)
            print(f"select_pick: count={count}, team_id={team_id}, total={total}, desc={team_player}")
            pick.positionId = new_player 
            pick.price = team_player.price 
            pick.positionDesc = pick_desc 
            pick.ranking = stats.ranking
            pick.save()
            print(f"select_pick: playerId={new_player} addId={pick.id} price={pick.price} pts={stats.projPts}, ranking={stats.ranking}")
            request.session['team_total'] = str(total)
            print(f"select_pick: count={count}, team_id={team_id}, total={total}")

            context = {
                "user": username,
                "reg_user": reg_user,
                "tab": "view",
                "pos": pos,
                "player": team_player,
                "team": gameTeam.objects.filter(userTeamId=team_id),
                "team_id": team_id,
                "stats": stats,
            }
            return render(request, "teams/addPlayer.html", context)    

        context = {
            "reg_user": reg_user,
            "tab": "view",
            "team_id": team_id,
            "message": "Player is too expensive for team. Please try again.",
        }
        return render(request, "teams/error.html", context)

    else:
        current_week =  seasonSchedule.objects.filter(week=1).only("currentWeek").first()
        week = current_week.currentWeek
        if pos == 0:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": playerStats.objects.get(playerId=player_id),
                "QB_players": player.objects.filter(position=0).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "stats": playerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 1:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": playerStats.objects.get(playerId=player_id),
                "RB_players": player.objects.filter(position=1).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "FB_players": player.objects.filter(position=2).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "stats": playerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 2:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": playerStats.objects.get(playerId=player_id),
                "RB_players": player.objects.filter(position=1).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "FB_players": player.objects.filter(position=2).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "stats": playerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 3:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": playerStats.objects.get(playerId=player_id),
                "WR_players": player.objects.filter(position=3).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "stats": playerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 4:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": playerStats.objects.get(playerId=player_id),
                "WR_players": player.objects.filter(position=3).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "stats": playerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 5:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": playerStats.objects.get(playerId=player_id),
                "TE_players": player.objects.filter(position=4).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "stats": playerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 6:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": defStats.objects.get(playerId=player_id),
                "DEF_players": player.objects.filter(position=8).only("position", "number", "teamId", "price", "id"),
                "stats": defStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 7:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": playerStats.objects.get(playerId=player_id),
                "QB_players": player.objects.filter(position=0).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "RB_players": player.objects.filter(position=1).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "FB_players": player.objects.filter(position=2).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "WR_players": player.objects.filter(position=3).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "TE_players": player.objects.filter(position=4).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "K_players": player.objects.filter(position=7).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                "stats": playerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif pos == 8:
            context = {
                "user": username,
                "team_id": team_id,
                "reg_user": reg_user,
                "pick": player.objects.get(pk=player_id),
                "pick_stats": kickerStats.objects.get(playerId=player_id),
                "K_players": player.objects.filter(position=7).only("position", "number", "teamId", "price", "id"),
                "stats": kickerStats.objects.only("projPts", "ranking"),
                "game_player": pick,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        else:
            context = {
                "reg_user": reg_user,
                "tab": "view",
                "team_id": team_id,
                "message": "No player selection found. Please try again.",
            }
            return render(request, "teams/error.html", context)

        return render(request, "teams/selectPick.html", context)

def view_team(request, team_id):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    teamId = request.session.get('team_id')
    total = float(request.session.get('team_total'))
    count = request.session.get('team_count')
    if request.method == "POST":
        new_player = int(request.POST.get('player'))
        print(f"view_team new_player = {new_player}")
        position = int(request.POST.get('pos'))
        print(f"view_team position = {position}")

        if new_player == 0:
            context = {
                "reg_user": reg_user,
                "tab": "view",
                "team_id": teamId,
                "message": "No player selected. Please try again.",
            }
            return render(request, "teams/error.html", context)

        pick = player.objects.get(pk=new_player)
        pick_desc = str(pick)
        print(f"view_team: count={count}, teamId={teamId}, total={total}, desc={pick_desc}")
        total = total + float(pick.price)
        if total < 13000:
            if position == 8:
                stats = kickerStats.objects.get(playerId=new_player)
                add_player = gameTeam(username=username, userTeamId=teamId, positionId=new_player, positionChoice=position, price=pick.price, positionDesc=pick_desc, pts=0)
                add_player.save()
            elif position == 6:
                stats = defStats.objects.get(playerId=new_player)
                add_player = gameTeam(username=username, userTeamId=teamId, positionId=new_player, positionChoice=position, price=pick.price, positionDesc=pick_desc, pts=0)
                add_player.save()
            elif position == 7:
              if pick.position == 8:
                stats = defStats.objects.get(playerId=new_player)
              elif pick.position == 7:
                stats = kickerStats.objects.get(playerId=new_player)
              else:
                stats = playerStats.objects.get(playerId=new_player)
              add_player = gameTeam(username=username, userTeamId=teamId, positionId=new_player, positionChoice=position, price=pick.price, positionDesc=pick_desc, pts=0)
              add_player.save()
            else:
              stats = playerStats.objects.get(playerId=new_player)
              add_player = gameTeam(username=username, userTeamId=teamId, positionId=new_player, positionChoice=position, price=pick.price, positionDesc=pick_desc, pts=0)
              add_player.save()
            print(f"view_team: playerId={new_player} addId={add_player.id} price={pick.price} pts={stats.projPts}, ranking={stats.ranking}")
            count = count + 1
            request.session['team_count'] = count
            request.session['team_total'] = str(total)
            print(f"view_team: count={count}, teamId={teamId}, total={total}")
            return HttpResponseRedirect(reverse("viewTeam", args=(team_id,)))
            
        context = {
            "reg_user": reg_user,
            "tab": "view",
            "team_id": team_id,
            "message": "Player is too expensive for team. Please try again.",
        }
        return render(request, "teams/error.html", context)
    else:
        if team_id == 32:
            team_id = teamId
        team_found = True
        players_exist = False
        current_week =  seasonSchedule.objects.filter(week=1).only("currentWeek").first()
        week = current_week.currentWeek
        weekly_games = gameTeam.objects.filter(week=week).exclude(status=0).exclude(status=1).exclude(status=2)

        print(f"view_team: count={count}, team_id={team_id}, total={total}")
        games_started = True
        games_completed = True
        if weekly_games.exists():
            print(f"view_team game team object found: {weekly_games}")
            try:
                team_started = gameTeam.objects.filter(week=week).filter(userTeamId=team_id).filter(status=3).first()
            except gameTeam.DoesNotExist:
                games_started = False

            try:
                team_completed = gameTeam.objects.filter(week=week).filter(userTeamId=team_id).filter(status=4).first()
            except gameTeam.DoesNotExist:
                games_completed = False

            if team_completed and team_started:
                context = {
                    "reg_user": reg_user,
                    "tab": "view",
                    "team_id": team_id,
                    "message": "Weekly games have started. Select a team that has been submitted.",
                }
                return render(request, "teams/error.html", context)

            if team_started is not None:
                team_all = gameTeam.objects.filter(week=week).filter(userTeamId=team_id).filter(status=3)
                if team_all.exists():
                    total = 0
                    ranking = 0
                    games_found = True
                    try:
                        game_ranking = weeklyRankings.objects.get(teamId=team_id)
                    except weeklyRankings.DoesNotExist:
                        games_found = False

                    if games_found:
                        print(f"view_team game_ranking exists {game_ranking}")
                        if game_ranking is not None:
                            total = game_ranking.total
                            ranking = game_ranking.ranking
                    count = 9

                    print(f"view_team ranking= {ranking}, count= {count} and total= {total}")
                    print(f"view_team team exists {team_id} and status is started {team_started.status}")

                    context = {
                        "user": username,
                        "reg_user": reg_user,
                        "admin_user": admin_user,
                        "team_id": team_id,
                        "game": True,
                        "count": count,
                        "total": total,
                        "ranking": ranking,
                        "QB_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=0, status=3),
                        "RB1_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=1, status=3),
                        "RB2_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=2, status=3),
                        "WR1_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=3, status=3),
                        "WR2_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=4, status=3),
                        "TE_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=5, status=3),
                        "DEF_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=6, status=3),
                        "FLEX_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=7, status=3),
                        "K_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=8, status=3),
                    }
            elif team_completed is not None:
                team_all = gameTeam.objects.filter(week=week).filter(userTeamId=team_id).filter(status=4)
                if team_all.exists():
                    total = 0
                    ranking = 0
                    games_found = True
                    try:
                        game_ranking = weeklyRankings.objects.get(teamId=team_id)
                    except weeklyRankings.DoesNotExist:
                        games_found = False

                    if games_found:
                        print(f"view_team game_ranking exists {game_ranking}")
                        if game_ranking is not None:
                            total = game_ranking.total
                            ranking = game_ranking.ranking
                    count = 9

                    print(f"view_team ranking= {ranking}, count= {count} and total= {total}")
                    print(f"view_team team exists {team_id} and status is started {team_completed.status}")

                    context = {
                        "user": username,
                        "reg_user": reg_user,
                        "admin_user": admin_user,
                        "team_id": team_id,
                        "game": True,
                        "count": count,
                        "total": total,
                        "ranking": ranking,
                        "QB_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=0, status=4),
                        "RB1_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=1, status=4),
                        "RB2_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=2, status=4),
                        "WR1_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=3, status=4),
                        "WR2_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=4, status=4),
                        "TE_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=5, status=4),
                        "DEF_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=6, status=4),
                        "FLEX_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=7, status=4),
                        "K_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=8, status=4),
                    }
                else:
                    context = {
                        "reg_user": reg_user,
                        "tab": "view",
                        "team_id": team_id,
                        "message": "Weekly games have started, but team selected not found.",
                    }
                    return render(request, "teams/error.html", context)
            else:
                context = {
                    "reg_user": reg_user,
                    "tab": "view",
                    "team_id": team_id,
                    "message": "Weekly games have started. Select a team that has been submitted.",
                }
                return render(request, "teams/error.html", context)
        else:
            team = gameTeam.objects.filter(userTeamId=team_id).exclude(status=0).exclude(status=4)
            players_exist = False
            print(f"view_team team object does exist")
            if team.exists():
                print(f"view_team team object found: {team}")
                if team.first().status == 2:
                    players_exist = True
                    print(f"view_team game team exists and status is submitted: {players_exist}")
                    context = {
                        "user": username,
                        "reg_user": reg_user,
                        "admin_user": admin_user,
                        "team_id": team_id, 
                        "game": True,
                        "other_team": teamId,
                        "count": count,
                        "QB_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=0, status=2),
                        "RB1_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=1, status=2),
                        "RB2_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=2, status=2),
                        "WR1_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=3, status=2),
                        "WR2_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=4, status=2),
                        "TE_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=5, status=2),
                        "DEF_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=6, status=2),
                        "FLEX_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=7, status=2),
                        "K_player": gameTeam.objects.get(userTeamId=team_id, positionChoice=8, status=2),
                    }
                else:
                    players_exist = True
                    print(f"view_team game team exists and status is cart: {players_exist}")
                    print(f"view_team total = {total}, count = {count}")
                    try:    
                        QB_pick = team.get(userTeamId=team_id, positionChoice=0, status=1)
                    except gameTeam.DoesNotExist:
                        QB_pick = team.filter(userTeamId=team_id, positionChoice=0, status=1)
                    try:
                        RB1_pick = team.get(userTeamId=team_id, positionChoice=1, status=1)
                    except gameTeam.DoesNotExist:
                        RB1_pick = team.filter(userTeamId=team_id, positionChoice=1, status=1)
                    try:    
                        RB2_pick = team.get(userTeamId=team_id, positionChoice=2, status=1)
                    except gameTeam.DoesNotExist:
                        RB2_pick = team.filter(userTeamId=team_id, positionChoice=2, status=1)
                    try:
                        WR1_pick = team.get(userTeamId=team_id, positionChoice=3, status=1)
                    except gameTeam.DoesNotExist:
                        WR1_pick = team.filter(userTeamId=team_id, positionChoice=3, status=1)
                    try:    
                        WR2_pick = team.get(userTeamId=team_id, positionChoice=4, status=1)
                    except gameTeam.DoesNotExist:
                        WR2_pick = team.filter(userTeamId=team_id, positionChoice=4, status=1)
                    try:
                        TE_pick = team.get(userTeamId=team_id, positionChoice=5, status=1)
                    except gameTeam.DoesNotExist:
                        TE_pick = team.filter(userTeamId=team_id, positionChoice=5, status=1)
                    try:    
                        DEF_pick = team.get(userTeamId=team_id, positionChoice=6, status=1)
                    except gameTeam.DoesNotExist:
                        DEF_pick = team.filter(userTeamId=team_id, positionChoice=6, status=1)
                    try:
                        FLEX_pick = team.get(userTeamId=team_id, positionChoice=7, status=1)
                    except gameTeam.DoesNotExist:
                        FLEX_pick = team.filter(userTeamId=team_id, positionChoice=7, status=1)                            
                    try:
                        K_pick = team.get(userTeamId=team_id, positionChoice=8, status=1)
                    except gameTeam.DoesNotExist:
                        K_pick = team.filter(userTeamId=team_id, positionChoice=8, status=1)
                    context = {
                        "user": username,
                        "reg_user": reg_user,
                        "admin_user": admin_user,
                        "team_id": team_id,
                        "total": total,
                        "count": count,
                        "game": True,
                        "QB_player": QB_pick,
                        "RB1_player": RB1_pick,
                        "RB2_player": RB2_pick,
                        "WR1_player": WR1_pick,
                        "WR2_player": WR2_pick,
                        "TE_player": TE_pick,
                        "DEF_player": DEF_pick,
                        "FLEX_player": FLEX_pick,
                        "K_player": K_pick,
                        "QB_players": player.objects.filter(position=0).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                        "RB_players": player.objects.filter(position=1).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                        "FB_players": player.objects.filter(position=2).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                        "WR_players": player.objects.filter(position=3).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                        "TE_players": player.objects.filter(position=4).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                        "DEF_players": player.objects.filter(position=8).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                        "K_players": player.objects.filter(position=7).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                    }

            if players_exist == False:
                print(f"view_team players_exist = {players_exist}")
                context = {
                    "user": username,
                    "reg_user": reg_user,
                    "admin_user": admin_user,
                    "team_id": team_id,
                    "total": total,
                    "count": count,
                    "QB_players": player.objects.filter(position=0).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                    "RB_players": player.objects.filter(position=1).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                    "FB_players": player.objects.filter(position=2).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                    "WR_players": player.objects.filter(position=3).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                    "TE_players": player.objects.filter(position=4).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                    "DEF_players": player.objects.filter(position=8).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                    "K_players": player.objects.filter(position=7).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
                }

        print(f"view_team players_exist={players_exist}")
        return render(request, "teams/viewTeam.html", context)

def view_nflTeam(request, team_id):
    if request.method == "POST":
        username = request.user
        view_team = request.POST.get('teamId')

        if view_team is not None:
            try:
                team = player.objects.filter(teamId=view_team).first()
            except player.DoesNotExist:
                context = {
                    "reg_user": False,
                    "tab": "view",
                    "team_id": view_team,
                    "message": "Team to view does not exist.",
                }
                return render(request, "teams/error.html", context)

            return HttpResponseRedirect(reverse("viewNFLTeam", args=(view_team,)))

        context = {
            "reg_user": False,
            "tab": "view",
            "team_id": view_team,
            "message": "Team to view does not exist.",
        }
        return render(request, "teams/error.html", context)
    else:
        if request.user.is_authenticated:
            username = request.user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, "users/register.html", {"message": "User does not exists."})
            admin_user = user.is_superuser
        else:
            username = None
            admin_user = False

        teams = [1, 2, 3]
        if team_id < 32:
            context = {
                "user": username,
                "admin_user": admin_user,
                "team_id": team_id,
                "teams": teams,
                "offense": player.objects.filter(teamId=team_id).filter(teamType="Offense").order_by('position'),
                "kicker": player.objects.filter(teamId=team_id).filter(position=7),
                "def": player.objects.filter(teamId=team_id).filter(position=8),
            }
        else:
            context = {
                "user": username,
                "team_id": team_id,
            }
        return render(request, "teams/viewNFLTeam.html", context)
        
def submit_team(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    team_id = request.session.get('team_id')
    total = float(request.session.get('team_total'))
    count = request.session.get('team_count')
    current_week =  seasonSchedule.objects.filter(week=1).only("currentWeek").first()
    week = current_week.currentWeek
    print(f"index week={week}, current_week={current_week}")
    if request.method == "POST":
        weekly_game = gameTeam.objects.filter(userTeamId=team_id).filter(status=1)
        if not weekly_game.exists():
            context = {
                "reg_user": False,
                "tab": "game",
                "team_id": 32,
                "message": "Game to submit not found.",
            }
            return render(request, "teams/error.html", context)

        print(f"submitTeam teams started count = {weekly_game.count()}")
        for player in weekly_game:
            player.status = 2
            player.week = week
            player.save()
            print(f"submitTeam player = {player}")

        context = {
            "reg_user": reg_user,
            "tab": "game",
            "team_id": team_id,
            "message": "Fantasy team has been successfully submitted.",
        }
        return render(request, "teams/success.html", context)
    else:
        weekly_games = gameTeam.objects.filter(status=3)
        if weekly_games.exists():
            context = {
                "reg_user": reg_user,
                "tab": "game",
                "team_id": team_id,
                "message": "Weekly games have started - no new games can be submitted.",
            }
            return render(request, "teams/error.html", context)

        team = gameTeam.objects.filter(userTeamId=team_id).exclude(status=0).exclude(status=4)
        if team.exists():
            if team.first().status == 2:
                context = {
                    "reg_user": reg_user,
                    "tab": "game",
                    "team_id": team_id,
                    "message": "Weekly games have started.",
                }
                return render(request, "teams/error.html", context)
            else:
                print(f"submit_team game team exists and status is cart")
                print(f"submit_team total = {total}, count = {count}")
                if count == 9:
                    context = {
                        "user": username,
                        "team_id": team_id,
                        "total": total,
                        "count": count,
                        "game": True,
                        "QB_player": team.get(positionChoice=0, status=1),
                        "RB1_player": team.get(positionChoice=1, status=1),
                        "RB2_player": team.get(positionChoice=2, status=1),
                        "WR1_player": team.get(positionChoice=3, status=1),
                        "WR2_player": team.get(positionChoice=4, status=1),
                        "TE_player": team.get(positionChoice=5, status=1),
                        "DEF_player": team.get(positionChoice=6, status=1),
                        "FLEX_player": team.get(positionChoice=7, status=1),
                        "K_player": team.get(positionChoice=8, status=1),
                    }
                    return render(request, "teams/submitTeam.html", context)
                else:
                    context = {
                        "reg_user": reg_user,
                        "tab": "game",
                        "team_id": team_id,
                        "message": "Team must have 9 players to be submitted.",
                    }
                    return render(request, "teams/error.html", context)

        context = {
            "reg_user": reg_user,
            "tab": "game",
            "team_id": team_id,
            "message": "Teams cannot be submitted currently. Please try again later",
        }
        return render(request, "teams/error.html", context)
         
def update_player(request, pos):
    message = "Player to update does not exist."
    if request.method == "POST":
        username = request.user
        first = request.POST.get('first')
        last = request.POST.get('last')
        number = request.POST.get('num')
        position = request.POST.get('pos')
        feet = request.POST.get('heightFeet')
        inches = request.POST.get('heightInches')
        weight = request.POST.get('weight')
        experience = request.POST.get('exp')
        college = request.POST.get('college')
        teamType = request.POST.get('teamType')
        teamId = request.POST.get('teamId')
        div = request.POST.get('div')
        status = request.POST.get('status')

        try:
            update_player = player.objects.get(pk=pos)
        except player.DoesNotExist:
            context = {
                "reg_user": False,
                "tab": "player",
                "team_id": 32,
                "message": message,
            }
            return render(request, "teams/error.html", context)

        if first is not None:
            update_player.firstName = first
        if last is not None:
            update_player.lastName = last
        if number is not None:
            update_player.number = number
        if position is not None:
            update_player.position = position
        if feet is not None:
            update_player.heightFeet = feet
        if inches is not None:
            update_player.heightInches = inches
        if weight is not None:
            update_player.weight = weight
        if experience is not None:
            update_player.experience = experience
        if college is not None:
            update_player.college = college
        if teamType is not None:
            update_player.teamType = teamType
        if teamId is not None:
            update_player.teamId = teamId
        if div is not None:
            if div == "AFC":
                update_player.AFC = True
                update_player.NFC = False
            if div == "NFC":
                update_player.AFC = False
                update_player.NFC = True
        if status is not None:
            update_player.status = status

        update_player.save()

        stats = None
        if update_player.position == 8:
            try:
                stats = defStats.objects.get(playerId=pos)
            except defStats.DoesNotExist:
                statsFound = False       
        elif update_player.position == 7:
            try:
                stats = kickerStats.objects.get(playerId=pos)
            except kickerStats.DoesNotExist:
                statsFound = False
        else:
            try:
                stats = playerStats.objects.get(playerId=pos)
            except playerStats.DoesNotExist:
                statsFound = False
        context = {
            "user": username,
            "pick": pos,
            "team_id": update_player.teamId,
            "player_info": update_player,
            "player": stats,
        }
        return render(request, "teams/stats.html", context)
    else:
        if request.user.is_authenticated:
            username = request.user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, "users/register.html", {"message": "User does not exists."})
            admin_user = user.is_superuser
            reg_user = not admin_user
        else:
            return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

        try:
            update_player = player.objects.get(pk=pos)
        except player.DoesNotExist:
            context = {
                "reg_user": False,
                "tab": "player",
                "tea,_id": 32,
                "message": message,
            }
            return render(request, "teams/error.html", context)

        print(f"update_player= {update_player}, pos= {pos}")
        context = {
            "user": username,
            "pick": pos,
            "team_id": update_player.teamId,
            "player_info": update_player,
        }
        return render(request, "teams/updatePlayer.html", context)
  
def stats(request, pos):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    try:
        update_player = player.objects.get(pk=pos)
    except player.DoesNotExist:
        context = {
            "reg_user": False,
            "tab": "player",
            "team_id": 32,
            "message": message,
        }
        return render(request, "teams/error.html", context)

    print(f"stats= {update_player}, pos= {pos}")
    print(f"stats: position = {update_player.position}")
    statsFound = True
    stats = None
    if update_player.position == 8:
        try:
            stats = defStats.objects.get(playerId=pos)
        except defStats.DoesNotExist:
            statsFound = False       
    elif update_player.position == 7:
        try:
            stats = kickerStats.objects.get(playerId=pos)
        except kickerStats.DoesNotExist:
            statsFound = False
    else:
        try:
            stats = playerStats.objects.get(playerId=pos)
        except playerStats.DoesNotExist:
            statsFound = False

    context = {
        "user": username,
        "pick": pos,
        "team_id": update_player.teamId,
        "player_info": update_player,
        "player": stats,
    }
    return render(request, "teams/stats.html", context)

def compare(request, pos):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    team_id = request.session.get('team_id')
    if request.method == "POST":
        player1 = int(request.POST.get('player1'))
        print(f"compare player1 = {player1}")
        player2 = int(request.POST.get('player2'))
        print(f"compare player2 = {player2}")
        player3 = int(request.POST.get('player3'))
        print(f"compare player3 = {player3}")
        player1_found = True
        player2_found = True
        player3_found = True
        pick = player.objects.get(pk=pos)

        if player1 == 0:
            player1_found = False
        if player2 == 0:
            player2_found = False
        if player3 == 0:
            player3_found = False

        print(f"compare player1_found = {player1_found}")
        print(f"compare player2_found = {player2_found}")
        print(f"compare player3_found = {player3_found}")
        current_week =  seasonSchedule.objects.filter(week=1).only("currentWeek").first()
        week = current_week.currentWeek
        if player1_found == True and player2_found == True and player3_found == True:
            print(f"compare player1, player2, and player3 found")
            if pick.position == 8:
                player1_stats = defStats.objects.get(playerId=player1)
                player2_stats = defStats.objects.get(playerId=player2)
                player3_stats = defStats.objects.get(playerId=player3)
                pick_stats = defStats.objects.get(playerId=pos)
            elif pick.position == 7: 
                player1_stats = kickerStats.objects.get(playerId=player1)
                player2_stats = kickerStats.objects.get(playerId=player2)
                player3_stats = kickerStats.objects.get(playerId=player3)
                pick_stats = kickerStats.objects.get(playerId=pos)
            else:
                player1_stats = playerStats.objects.get(playerId=player1)
                player2_stats = playerStats.objects.get(playerId=player2)
                player3_stats = playerStats.objects.get(playerId=player3)
                pick_stats = playerStats.objects.get(playerId=pos)

            context = {
                "user": username,
                "reg_user": reg_user,
                "pick": pick,
                "pick_stats": pick_stats,
                "player1": player.objects.get(pk=player1),
                "player1_stats": player1_stats,
                "player2": player.objects.get(pk=player2),
                "player2_stats": player2_stats,
                "player3": player.objects.get(pk=player3),
                "player3_stats": player3_stats,
                "team_id": team_id,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif player2_found == True and player1_found == True and player3_found == False:
            print(f"compare player1 and player2 found")
            if pick.position == 8:
                player1_stats = defStats.objects.get(playerId=player1)
                player2_stats = defStats.objects.get(playerId=player2)
                pick_stats = defStats.objects.get(playerId=pos)
            elif pick.position == 7: 
                player1_stats = kickerStats.objects.get(playerId=player1)
                player2_stats= kickerStats.objects.get(playerId=player2)
                pick_stats = kickerStats.objects.get(playerId=pos)
            else:
                player1_stats = playerStats.objects.get(playerId=player1)
                player2_stats = playerStats.objects.get(playerId=player2)
                pick_stats = playerStats.objects.get(playerId=pos)

            context = {
                "user": username,
                "reg_user": reg_user,
                "pick": pick,
                "pick_stats": pick_stats,
                "player1": player.objects.get(pk=player1),
                "player1_stats": player1_stats,
                "player2": player.objects.get(pk=player2),
                "player2_stats": player2_stats,
                "team_id": team_id,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif player3_found == True and player1_found == True and player2_found == False:
            print(f"compare player1 and player3 found")
            if pick.position == 8:
                player1_stats = defStats.objects.get(playerId=player1)
                player2_stats = defStats.objects.get(playerId=player3)
                pick_stats = defStats.objects.get(playerId=pos)
            elif pick.position == 7: 
                player1_stats = kickerStats.objects.get(playerId=player1)
                player2_stats = kickerStats.objects.get(playerId=player3)
                pick_stats = kickerStats.objects.get(playerId=pos)
            else:
                player1_stats = playerStats.objects.get(playerId=player1)
                player2_stats = playerStats.objects.get(playerId=player3)
                pick_stats = playerStats.objects.get(playerId=pos)

            context = {
                "user": username,
                "reg_user": reg_user,
                "pick": pick,
                "pick_stats": pick_stats,
                "player1": player.objects.get(pk=player1),
                "player1_stats": player1_stats,
                "player2": player.objects.get(pk=player3),
                "player2_stats": player2_stats,
                "team_id": team_id,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif player3_found == True and player2_found == True and player1_found == False:
            print(f"compare player3 and player2 found")
            if pick.position == 8:
                player1_stats = defStats.objects.get(playerId=player2)
                player2_stats = defStats.objects.get(playerId=player3)
                pick_stats = defStats.objects.get(playerId=pos)
            elif pick.position == 7: 
                player1_stats = kickerStats.objects.get(playerId=player2)
                player2_stats = kickerStats.objects.get(playerId=player3)
                pick_stats = kickerStats.objects.get(playerId=pos)
            else:
                player1_stats = playerStats.objects.get(playerId=player2)
                player2_stats = playerStats.objects.get(playerId=player3)
                pick_stats = playerStats.objects.get(playerId=pos)

            context = {
                "user": username,
                "reg_user": reg_user,
                "pick": pick,
                "pick_stats": pick_stats,
                "player1": player.objects.get(pk=player2),
                "player1_stats": player1_stats,
                "player2": player.objects.get(pk=player3),
                "player2_stats": player2_stats,
                "team_id": team_id,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif player1_found == True and player2_found == False and player3_found == False:
            print(f"compare player1")
            if pick.position == 8:
                player1_stats = defStats.objects.get(playerId=player1)
                pick_stats = defStats.objects.get(playerId=pos)
            elif pick.position == 7: 
                player1_stats = kickerStats.objects.get(playerId=player1)
                pick_stats = kickerStats.objects.get(playerId=pos)
            else:
                player1_stats = playerStats.objects.get(playerId=player1)
                pick_stats = playerStats.objects.get(playerId=pos)

            context = {
                "user": username,
                "reg_user": reg_user,
                "pick": pick,
                "pick_stats": pick_stats,
                "player1": player.objects.get(pk=player1),
                "player1_stats": player1_stats,
                "team_id": team_id,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif player2_found == True and player1_found == False and player3_found == False:
            print(f"compare player2")
            if pick.position == 8:
                player1_stats = defStats.objects.get(playerId=player2)
                pick_stats = defStats.objects.get(playerId=pos)
            elif pick.position == 7: 
                player1_stats = kickerStats.objects.get(playerId=player2)
                pick_stats = kickerStats.objects.get(playerId=pos)
            else:
                player1_stats = playerStats.objects.get(playerId=player2)
                pick_stats = playerStats.objects.get(playerId=pos)

            context = {
                "user": username,
                "reg_user": reg_user,
                "pick": pick,
                "pick_stats": pick_stats,
                "player1": player.objects.get(pk=player2),
                "player1_stats": player1_stats,
                "team_id": team_id,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        elif player3_found == True and player2_found == False and player1_found == False:
            print(f"compare player3")
            if pick.position == 8:
                player1_stats = defStats.objects.get(playerId=player3)
                pick_stats = defStats.objects.get(playerId=pos)
            elif pick.position == 7: 
                player1_stats = kickerStats.objects.get(playerId=player3)
                pick_stats = kickerStats.objects.get(playerId=pos)
            else:
                player1_stats = playerStats.objects.get(playerId=player3)
                pick_stats = playerStats.objects.get(playerId=pos)

            context = {
                "user": username,
                "reg_user": reg_user,
                "pick": pick,
                "pick_stats": pick_stats,
                "player1": player.objects.get(pk=player3),
                "player1_stats": player1_stats,
                "team_id": team_id,
                "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
            }
        else:
            context = {
                "reg_user": reg_user,
                "tab": "player",
                "team_id": team_id,
                "message": "No player selection found to compare. Please try again.",
            }
            return render(request, "teams/error.html", context)

        return render(request, "teams/viewCompare.html", context)
    else:
        pick = player.objects.get(pk=pos)
        position = pick.position
        context = {
            "user": username,
            "reg_user": reg_user,
            "team_id": team_id,
            "pick": pick,
            "players": player.objects.filter(position=position).only("firstName", "lastName", "position", "number", "teamId", "price", "id"),
        }
        return render(request, "teams/compare.html", context)

def view_compare(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    team_id = request.session.get('team_id')
    total = float(request.session.get('team_total'))
    count = request.session.get('team_count')

    new_player = request.POST.get('player')
    print(f"view_compare new_player = {new_player}")
    position = int(request.POST.get('pos'))
    print(f"view_compare position = {position}")

    if new_player is None:
        context = {
            "reg_user": reg_user,
            "tab": "view",
            "team_id": team_id,
            "message": "No player selected. Please try again.",
        }
        return render(request, "teams/error.html", context)

    if position == 10:
        context = {
            "reg_user": reg_user,
            "tab": "view",
            "team_id": team_id,
            "message": "No player selected. Please try again.",
        }
        return render(request, "teams/error.html", context)

    try:
        pick = player.objects.get(pk=new_player)
    except player.DoesNotExist:
        context = {
            "reg_user": reg_user,
            "tab": "player",
            "team_id": team_id,
            "message": "Player to add does not exist.",
        }
        return render(request, "teams/error.html", context)

    game = gameTeam.objects.filter(userTeamId=team_id)

    if pick.position == 8:
        stats = defStats.objects.get(playerId=new_player)
        pick_desc = str(pick)
    elif pick.position == 7:
        stats = kickerStats.objects.get(playerId=new_player)
        pick_desc = str(pick)
    else:
        stats = playerStats.objects.get(playerId=new_player)
        pick_desc = str(pick)
    print(f"view_compare: count={count}, team_id={team_id}, total={total}, desc={pick_desc}")
    print(f"view_compare: position={position} new_player={new_player}")

    player_found = False
    if not game.exists():
        add_player = gameTeam(username=username, userTeamId=team_id, positionId=new_player, positionChoice=position, price=pick.price, positionDesc=pick_desc, pts=0)
        add_player.save()
        print(f"view_compare: playerId={new_player} addId={add_player.id} price={pick.price} pts={stats.projPts}, ranking={stats.ranking}")
        count = count + 1
    else:      
        for player_pos in game:
            print(f"view_compare player_pos= {player_pos}")
            if player_pos.positionChoice == position:
                print(f"view_compare price before: {player_pos.price} and price after: {pick.price}")
                total = total - float(player_pos.price)
                print(f"view_compare total before= {total}")
                total = total + float(pick.price)
                print(f"view_compare total after= {total}")
                if total >= 13000:
                    context = {
                        "reg_user": reg_user,
                        "tab": "view",
                        "team_id": team_id,
                        "message": "Player is too expensive for team. Please try again.",
                    }
                    return render(request, "teams/error.html", context)
                player_pos.positionId = new_player
                player_pos.price = pick.price
                player_pos.positionDesc = pick_desc
                player_pos.ranking = stats.ranking
                player_pos.save()
                print(f"view_compare: playerId={new_player} addId={player_pos.id} price={pick.price} pts={stats.projPts}, ranking={stats.ranking}")
                player_found =  True           
        if not player_found:
            print(f"view_compare player_found={player_found}")
            total = total + float(pick.price)
            if total >= 13000:
                context = {
                    "reg_user": reg_user,
                    "tab": "view",
                    "team_id": team_id,
                    "message": "Player is too expensive for team. Please try again.",
                }
                return render(request, "teams/error.html", context)
            add_player = gameTeam(username=username, userTeamId=team_id, positionId=new_player, positionChoice=position, price=pick.price, positionDesc=pick_desc, pts=0)
            add_player.save()
            print(f"view_compare: playerId={new_player} addId={add_player.id} price={pick.price} pts={stats.projPts}, ranking={stats.ranking}")
            count = count + 1                

    request.session['team_count'] = count
    request.session['team_total'] = str(total)
    print(f"view_compare: count={count}, team_id={team_id}, total={total}")

    context = {
        "user": username,
        "reg_user": reg_user,
        "tab": "view",
        "pos": position,
        "player": pick,
        "stats": stats,
        "team": gameTeam.objects.filter(userTeamId=team_id),
        "team_id": team_id,
    }
    return render(request, "teams/addPlayer.html", context)

def players(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    if request.method == "POST":
        position = int(request.POST.get('pos'))
        print(f"players position = {position}")

        if position == 8:
            def_stats = defStats.objects.all().only("fanPts", "projPts", "ranking").order_by('playerId')
            kick_stats = None
            off_stats = None
            print(f"kick: stats={kick_stats}")
            print(f"def: stats={def_stats}")
            print(f"off: stats={off_stats}")
        elif position == 7: 
            kick_stats = kickerStats.objects.all().only("fanPts", "projPts", "ranking").order_by('playerId')
            def_stats = None
            off_stats = None
            print(f"kick: stats={kick_stats}")
            print(f"def: stats={def_stats}")
            print(f"off: stats={off_stats}")
        else:
            off_stats = playerStats.objects.all().only("fanPts", "projPts", "ranking").order_by('playerId')
            def_stats = None
            kick_stats = None
            print(f"kick: stats={kick_stats}")
            print(f"def: stats={def_stats}")
            print(f"off: stats={off_stats}")

        weekly_games = gameTeam.objects.filter(status=3)
        if weekly_games.exists():
            player_first = player.objects.filter(position=position).first()
            if position == 8:
                posDesc = "Defense/Special Teams"
            elif position == 7:
                posDesc = "Kicker"
            else:
                posDesc = player_first.get_position_display
            context = {
                "user": username,
                "admin": admin_user,
                "posDesc": posDesc,
                "pos": position,
                "players": player.objects.filter(position=position).only("firstName", "lastName", "position", "number", "teamId", "price", "id").order_by('-price'),
                "stats": 0,
                "team_id": 32,
            }
            return render(request, "teams/saveGameStats.html", context)

        current_week =  seasonSchedule.objects.filter(week=1).only("currentWeek").first()
        week = current_week.currentWeek
        print(f"players week = {week}")
        context = {
            "user": username,
            "admin": admin_user,
            "pos": position,
            "players": player.objects.filter(position=position).only("firstName", "lastName", "position", "number", "teamId", "price", "id").order_by('-price'),
            "off_stats": off_stats,
            "def_stats": def_stats,
            "kick_stats": kick_stats,
            "team_id": 32,
            "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
        }
        return render(request, "teams/savePlayerStats.html", context)
    else:
        print(f"viewPlayers")
        context = {
            "user": username,
            "reg_user": reg_user,
            "pos": 10,
            "team_id": 32,
        }
        return render(request, "teams/viewPlayers.html", context)

def save_game(request, pos):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    player_choice = request.POST.get('player')
    if player_choice is not None:
        print(f"save_game player_choice is not None")
        pick = player.objects.get(pk=player_choice)
        if pos == 8:
            def_stats = defStats.objects.get(playerId=player_choice)
            posDesc = "Defense/Special Teams"
            kick_stats = False
            off_stats = False
        elif pos == 7:
            kick_stats = kickerStats.objects.get(playerId=player_choice)
            posDesc = "Kicker"
            def_stats = False
            off_stats = False
        else:
            off_stats = playerStats.objects.get(playerId=player_choice)
            def_stats = False
            kick_stats = False
            posDesc = pick.get_position_display
        context = {
            "user": username,
            "admin": admin_user,
            "posDesc": posDesc,
            "pos": pos,
            "player_info": pick,
            "off_stats": off_stats,
            "def_stats": def_stats,
            "kick_stats": kick_stats,
            "team_id": 32,
        }
        return render(request, "teams/saveGameStats.html", context)
    else:
        playerId = request.POST.get('playId')
        print(f"save_game playerId = {playerId}")
        if pos == 8:
            ptsAll = int(request.POST.get('ptsAll'))
            sack = int(request.POST.get('sack'))
            safe = int(request.POST.get('safe'))
            ints = int(request.POST.get('ints'))
            fumRec = int(request.POST.get('fumRec'))
            TD = int(request.POST.get('TD'))
            blkKick = int(request.POST.get('blkKick'))
            retnYds = int(request.POST.get('retnYds'))
            retnTD = int(request.POST.get('retnTD'))
            stats = defStats.objects.get(playerId=playerId)
            print(f"save_game stats = {stats}")
            fanPts = stats.fanPts
            if fanPts == 0:
                fanPts = 10
            if ptsAll:
                fanPts = fanPts - 10
                stats.ptsAll = stats.ptsAll + ptsAll
                print(f"save_game ptsAll = {ptsAll}, fanPts before = {fanPts}")
                if stats.ptsAll > 34:
                    fanPts = fanPts - 4
                elif stats.ptsAll > 27:
                    fanPts = fanPts - 1
                elif stats.ptsAll > 20:
                    fanPts = fanPts + 0
                elif stats.ptsAll > 13:
                    fanPts = fanPts + 1
                elif stats.ptsAll > 6:
                    fanPts = fanPts + 4
                elif stats.ptsAll > 0:
                    fanPts = fanPts + 7
                else:
                    fanPts = fanPts + 10
                print(f"save_game fanPts after = {fanPts}")
            if sack:
                fanPts = fanPts + sack
                stats.sack = stats.sack + sack 
            if safe:
                new_pts = safe * 2
                fanPts = fanPts + new_pts
                stats.safe = stats.safe + safe
            if ints:
                new_pts = ints * 2
                fanPts = fanPts + new_pts
                stats.ints = stats.ints + ints  
            if fumRec:
                new_pts = fumRec * 2
                fanPts = fanPts + new_pts
                stats.fumRec = stats.fumRec + fumRec
            if TD:
                new_pts = TD * 6
                fanPts = fanPts + new_pts
                stats.TD = stats.TD + TD 
            if blkKick:
                new_pts = blkKick * 2
                fanPts = fanPts + new_pts
                stats.blkKick = stats.blkKick + blkKick
            if retnYds:
                new_pts = float(retnYds) * .04
                fanPts = float(fanPts) + float(new_pts)
                stats.retnYds = stats.retnYds + retnYds
            if retnTD:
                new_pts = retnTD * 6
                fanPts = fanPts + new_pts 
                stats.retnTD = stats.retnTD + retnTD
            print(f"save_game sack={sack}, safe={safe}, ints={ints}, fumRec={fumRec}, TD={TD}, blkKick={blkKick}, retnYds={retnYds}, retnTD={retnTD}")
            stats.fanPts = fanPts 
            stats.save()
            print(f"save_game fanPts after ALL = {fanPts}")
        elif pos == 7: 
            under20 = int(request.POST.get('under20'))
            under30 = int(request.POST.get('under30'))
            under40 = int(request.POST.get('under40'))
            under50 = int(request.POST.get('under50'))
            over50 = int(request.POST.get('over50'))
            made = int(request.POST.get('made'))
            stats = kickerStats.objects.get(playerId=playerId)
            print(f"save_game stats = {stats}")
            fanPts = stats.fanPts
            if under20:
                new_pts = under20 * 3
                fanPts = fanPts + new_pts 
                stats.under20 = stats.under20 + under20 
            if under30:
                new_pts = under30 * 3
                fanPts = fanPts + new_pts
                stats.under30 = stats.under30 + under30
            if under40:
                new_pts = under40 * 3
                fanPts = fanPts + new_pts
                stats.under40 = stats.under40 + under40
            if under50:
                new_pts = under50 * 4
                fanPts = fanPts + new_pts 
                stats.under50 = stats.under50 + under50    
            if over50:
                new_pts = over50 * 5
                fanPts = fanPts + new_pts
                stats.over50 = stats.over50 + over50 
            if made:
                fanPts = fanPts + made
                stats.made = stats.made + made
            print(f"save_game under20={under20}, under30={under30}, under40={under40}, under50={under50}, over50={over50}, made={made}")
            stats.fanPts = fanPts 
            stats.save()
            print(f"save_game fanPts after ALL = {fanPts}")
        else:
            passYds = int(request.POST.get('passYds'))
            passTD = int(request.POST.get('passTD'))
            passInt = int(request.POST.get('passInt'))
            rushAtts = int(request.POST.get('rushAtts'))
            rushYds = int(request.POST.get('rushYds'))
            rushTD = int(request.POST.get('rushTD'))
            recvTgt = int(request.POST.get('recvTgt'))
            recvRec = int(request.POST.get('recvRec'))
            recvYds = int(request.POST.get('recvYds'))
            recvTD = int(request.POST.get('recvTD'))
            retnYds = int(request.POST.get('retnYds'))
            retnTD = int(request.POST.get('retnTD'))
            twoPT = int(request.POST.get('twoPT'))
            fumTot = int(request.POST.get('fumTot'))
            fumLost = int(request.POST.get('fumLost'))
            stats = playerStats.objects.get(playerId=playerId)
            print(f"save_game stats = {stats}")
            fanPts = stats.fanPts
            if passYds > 0:
                new_pts = float(passYds) * .04
                fanPts = float(fanPts) + float(new_pts)
                stats.passYds = stats.passYds + passYds
            if passTD > 0:
                new_pts = passTD * 6
                fanPts = fanPts + new_pts
                stats.passTD = stats.passTD + passTD
            if passInt > 0:
                fanPts = fanPts - passInt
                stats.passInt = stats.passInt + passInt
            if rushAtts > 0:
                stats.rushAtts = stats.rushAtts + rushAtts  
            if rushYds > 0:
                new_pts = float(rushYds) * .1
                fanPts = float(fanPts) + float(new_pts)
                stats.rushYds = stats.rushYds + rushYds 
            if rushTD > 0:
                new_pts = rushTD * 6
                fanPts = fanPts + new_pts
                stats.rushTD = stats.rushTD + rushTD
            if recvTgt > 0:
                stats.recvTgt = stats.recvTgt + recvTgt
            if recvRec > 0:
                fanPts = fanPts + recvRec  
                stats.recvRec = stats.recvRec + recvRec
            if recvYds > 0:
                new_pts = float(recvYds) * .1
                fanPts = float(fanPts) + float(new_pts)
                stats.recvYds = stats.recvYds + recvYds                 
            if recvTD > 0:
                new_pts = recvTD * 6
                fanPts = fanPts + new_pts 
                stats.recvTD = stats.recvTD + recvTD
            if retnYds > 0:
                new_pts = float(retnYds) + .04
                fanPts = float(fanPts) + float(new_pts)
                stats.retnYds = stats.retnYds + retnYds 
            if retnTD > 0:
                new_pts = retnTD * 6
                fanPts = fanPts + new_pts 
                stats.retnTD = stats.retnTD + retnTD
            if twoPT > 0:
                new_pts = twoPT * 2
                fanPts = fanPts + new_pts 
                stats.twoPT = stats.twoPT + twoPT
            if fumTot > 0:
                fanPts = fanPts - fumTot      
                stats.fumTot = stats.fumTot + fumTot   
                stats.fumTot = stats.fumTot + fumLost           
            if fumLost > 0:
                new_pts = fumLost * 2
                fanPts = fanPts - new_pts    
                stats.fumLost = stats.fumLost + fumLost  
            print(f"save_game passYds={passYds}, passTD={passTD}, passInt={passInt}, rushAtts={rushAtts}, rushYds={rushYds}, rushTD={rushTD}, recvTD={recvTD}, recvTgt={recvTgt}, recvRec={recvRec}, recvYds={recvYds}, retnYds={retnYds}, retnTD={retnTD}, twoPT={twoPT}, fumTot={fumTot}, fumLost={fumLost}")
            stats.fanPts = fanPts 
            stats.save()
            print(f"save_game fanPts after ALL = {fanPts}")

        player_games = gameTeam.objects.filter(positionId=playerId)
        if player_games.exists():
            print(f"save_game player_games count = {player_games.count()}")
            for game in player_games:
                game.pts = float(stats.fanPts)
                game.save()
                print(f"save_game game in player_games={game.pts} {game.userTeamId}")

        weekly_games = gameTeam.objects.filter(status=3).order_by('userTeamId')
        if weekly_games.exists():
            print(f"save_game weekly_games count = {weekly_games.count()}")
            user_team = gameTeam.objects.filter(status=3).order_by('userTeamId').first()
            team = user_team.userTeamId
            total = 0
            user = None
            for game in weekly_games:
                print(f"save_game game = {game.id}")
                if team == game.userTeamId:
                    total = total + game.pts
                    if user != game.username:
                        user = game.username
                else:
                    game_team = weeklyRankings.objects.get(username=user, teamId=team)
                    game_team.total = total
                    game_team.save()
                    total = 0
                    team = game.userTeamId
                    print(f"save_game game_team={game_team}")
                    total = total + game.pts        
                    print(f"save_game game in player_games={game.pts} and total={total}")
            game_team = weeklyRankings.objects.get(username=user, teamId=team)
            game_team.total = total
            game_team.save()
            print(f"save_game END game_team={game_team}")

        ranking_games = weeklyRankings.objects.all().order_by('-total')
        index = 1
        if ranking_games.exists():
            print(f"save_game ranking_games count = {ranking_games.count()}")
            for team in ranking_games:
                team.ranking = index
                team.save()
                index = index + 1
                print(f"save_game team in ranking_games={team}")

        context = {
            "reg_user": False,
            "tab": "player",
            "team_id": 32,
            "message": "Game stats for player have been successfully updated.",
        }
        return render(request, "teams/success.html", context)

def save_player(request, pos):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    price = request.POST.get('price')
    fanPts = request.POST.get('fanPts')
    projPts = request.POST.get('projPts')
    ranking = request.POST.get('ranking')
    playerId = request.POST.get('playId')

    print(f"save_player price = {price}")
    print(f"save_player projPts = {projPts}")
    print(f"save_player ranking = {ranking}")
    print(f"save_player playerId = {playerId}")
    pick = player.objects.get(pk=playerId)
    pick.price = price
    pick.save()
    
    if pos == 8:
        stats = defStats.objects.get(playerId=playerId)
        print(f"save_player stats = {stats}")
        stats.projPts = projPts 
        stats.ranking = ranking
        stats.save()
        kick_stats = None
        off_stats = None
        def_stats = defStats.objects.all().only("fanPts", "projPts", "ranking").order_by('playerId')
        print(f"save_player def_stats = {def_stats}")
    elif pos == 7: 
        stats = kickerStats.objects.get(playerId=playerId)
        print(f"save_player stats = {stats}")
        stats.projPts = projPts 
        stats.ranking = ranking
        stats.save()            
        def_stats = None
        off_stats = None
        kick_stats = kickerStats.objects.all().only("fanPts", "projPts", "ranking").order_by('playerId')
        print(f"save_player kick_stats = {kick_stats}")
    else:
        stats = playerStats.objects.get(playerId=playerId)
        print(f"save_player stats = {stats}")
        stats.projPts = projPts 
        stats.ranking = ranking
        stats.save()  
        print(f"save_player after stats = {stats}")
        def_stats = None
        kick_stats = None
        off_stats = playerStats.objects.all().only("fanPts", "projPts", "ranking").order_by('playerId')
        print(f"save_player off_stats = {off_stats}")

    current_week =  seasonSchedule.objects.filter(week=1).only("currentWeek").first()
    week = current_week.currentWeek
    print(f"players week = {week}")
    context = {
        "user": username,
        "admin": admin_user,
        "pos": pos,
        "players": player.objects.filter(position=pos).only("firstName", "lastName", "position", "number", "teamId", "price", "id").order_by('-price'),
        "off_stats": off_stats,
        "def_stats": def_stats,
        "kick_stats": kick_stats,
        "team_id": 32,
        "games": seasonSchedule.objects.filter(week=week).only("homeTeam", "awayTeam").order_by('day'),
    }
    return render(request, "teams/savePlayerStats.html", context)

def update_stats(request, pos):
    message = "Player to update does not exist."
    if request.method == "POST":
        username = request.user
        try:
            update_player = player.objects.get(pk=pos)
        except player.DoesNotExist:
            context = {
                "reg_user": False,
                "tab": "player",
                "message": message,
            }
            return render(request, "teams/error.html", context)

        stats_found = True
        price = request.POST.get('price')
        projPts = request.POST.get('projPts')
        ranking = request.POST.get('ranking')
        if update_player.position == 8:
            ptsAll = request.POST.get('ptsAll')
            sack = request.POST.get('sack')
            safe = request.POST.get('safe')
            ints = request.POST.get('ints')
            fumRec = request.POST.get('fumRec')
            TD = request.POST.get('TD')
            blkKick = request.POST.get('blkKick')
            retnYds = request.POST.get('retnYds')
            retnTD = request.POST.get('retnTD')
            try:
                stats = defStats.objects.get(playerId=update_player.id)
            except defStats.DoesNotExist:
                stats_found = False
            if stats_found == False or stats is None:
                new_player = defStats(projPts=projPts, ranking=ranking, ptsAll=ptsAll, sack=sack, safe=safe, ints=ints, fumRec=fumRec, TD=TD, blkKick=blkKick, retnYds=retnYds, retnTD=retnTD, playerId=pos)
                new_player.save()
                stats_found = False
        elif update_player.position == 7:
            under20 = request.POST.get('under20')
            under30 = request.POST.get('under30')
            under40 = request.POST.get('under40')
            under50 = request.POST.get('under50')
            over50 = request.POST.get('over50')
            made = request.POST.get('made')
            try:
                stats = kickerStats.objects.get(playerId=update_player.id)
            except kickerStats.DoesNotExist:
                stats_found = False
            if stats_found == False or stats is None:
                new_player = kickerStats(projPts=projPts, ranking=ranking, under20=under20, under30=under30, under40=under40, under50=under50, over50=over50, made=made, playerId=pos)
                new_player.save()
                stats_found = False
        else:
            passYds = request.POST.get('passYds')
            passTD = request.POST.get('passTD')
            passInt = request.POST.get('passInt')
            rushAtts = request.POST.get('rushAtts')
            rushYds = request.POST.get('rushYds')
            rushTD = request.POST.get('rushTD')
            recvYds = request.POST.get('recvYds')
            recvTD = request.POST.get('recvTD')
            recvTgt = request.POST.get('recvTgt')
            recvRec = request.POST.get('recvRec')
            retnYds = request.POST.get('retnYds')
            retnTD = request.POST.get('retnTD')
            twoPT = request.POST.get('twoPT')
            fumTot = request.POST.get('fumTot')
            fumLost = request.POST.get('fumLost')
            try:
                stats = playerStats.objects.get(playerId=update_player.id)
            except playerStats.DoesNotExist:
                stats_found = False
            if stats_found == False or stats is None:
                new_player = playerStats(projPts=projPts, ranking=ranking, passYds=passYds, passTD=passTD, passInt=passInt, rushAtts=rushAtts, rushYds=rushYds, rushTD=rushTD, recvTgt=recvTgt, recvRec=recvRec, recvTD=recvTD, recvYds=recvYds, retnYds=retnYds, retnTD=retnTD, twoPT=twoPT, fumTot=fumTot, fumLost=fumLost, playerId=pos)
                new_player.save()
                stats_found = False

        if not stats_found:
            team_id = update_player.teamId
            print(f"update_stats POST: playerId = {update_player.id}")
            print(f"update_stats POST: add new stats= {new_player}")
            context = {
                "user": request.user,
                "pick": pos,
                "team_id": team_id,
                "player_info": update_player,
                "player": new_player,
            }
        else:
            if projPts is not None:
                stats.projPts = projPts
            if ranking is not None:
                stats.ranking = ranking
            print(f"POST stats = {stats}")
            if update_player.position == 8:
                if ptsAll is not None:
                    stats.ptsAll = ptsAll
                if sack is not None:
                    stats.sack = sack
                if safe is not None: 
                    stats.safe = safe
                if ints is not None:
                    stats.ints = ints
                if fumRec is not None: 
                    stats.fumRec = fumRec
                if TD is not None:
                    stats.TD = TD
                if blkKick is not None:
                    stats.blkKick = blkKick
                if retnYds is not None:
                    stats.retnYds = retnYds
                if retnTD is not None:
                    stats.retnTD = retnTD
                stats.save()
            elif update_player.position == 7:
                if under20 is not None:
                    stats.under20 = under20
                if under30 is not None:
                    stats.under30 = under30
                if under40 is not None: 
                    stats.under40 = under40
                if under50 is not None:
                    stats.under50 = under50
                if over50 is not None: 
                    stats.over50 = over50
                if made is not None:
                    stats.made = made
                stats.save()
            else:
                if passYds is not None:
                    stats.passYds = passYds
                if passTD is not None:
                    stats.passTD = passTD
                if passInt is not None:
                    stats.passInt = passInt
                if rushAtts is not None:
                    stats.rushAtts = rushAtts
                if rushYds is not None:
                    stats.rushYds = rushYds
                if rushTD is not None:
                    stats.rushTD = rushTD
                if recvYds is not None:
                    stats.recvYds = recvYds
                if recvTD is not None:
                    stats.recvTD = recvTD
                if recvTgt is not None:
                    stats.recvTgt = recvTgt
                if recvRec is not None:
                    stats.recvRec = recvRec
                if retnYds is not None:
                    stats.retnYds = retnYds
                if retnTD is not None:
                    stats.retnTD = retnTD
                if twoPT is not None:
                    stats.twoPT = twoPT
                if fumTot is not None:
                    stats.fumTot = fumTot
                if fumLost is not None:
                    stats.fumLost = fumLost
                stats.save()
            print(f"stats: stats = {stats}")
            context = {
                "user": username,
                "pick": pos,
                "team_id": update_player.teamId,
                "player_info": update_player,
                "player": stats,
            }
        return render(request, "teams/stats.html", context)
    else:
        if request.user.is_authenticated:
            username = request.user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, "users/register.html", {"message": "User does not exists."})
            admin_user = user.is_superuser
            reg_user = not admin_user
        else:
            return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

        try:
            update_player = player.objects.get(pk=pos)
        except player.DoesNotExist:
            context = {
                "reg_user": reg_user,
                "tab": "player",
                "team_id": 32,
                "message": message,
            }
            return render(request, "teams/error.html", context)
        print(f"update_stats GET= {update_player}, pos= {pos}")
        print(f"update_stats GET: position = {update_player.position}")
        statsFound = True
        stats = None
        if update_player.position == 8:
            try:
                stats = defStats.objects.get(playerId=pos)
            except defStats.DoesNotExist:
                statsFound = False       
        elif update_player.position == 7:
            try:
                stats = kickerStats.objects.get(playerId=pos)
            except kickerStats.DoesNotExist:
                statsFound = False
        else:
            try:
                stats = playerStats.objects.get(playerId=pos)
            except playerStats.DoesNotExist:
                statsFound = False

        print(f"stats: stats = {stats}")
        context = {
            "user": username,
            "pick": pos,
            "team_id": update_player.teamId,
            "player_info": update_player,
            "player": stats,
        }
        return render(request, "teams/updateStats.html", context)

def game(request):
    if request.method == "POST":
        username = request.user

        week = request.POST.get('week')
        print(f"updateGame week = {week}")
        action = request.POST.get('action')
        print(f"updateGame action = {action}")

        if action is not None:
            print(f"updateGame action is not None")
            if action == "0":
                all_players = player.objects.all().order_by('teamId')
                if not all_players.exists():
                    context = {
                        "reg_user": False,
                        "tab": "game",
                        "team_id": 32,
                        "message": "Player pricing updates for current week not found.",
                    }
                    return render(request, "teams/error.html", context)
 
                print(f"updateGame players count = {all_players.count()}")
                for pick in all_players:
                    print(f"updateGame player position = {pick.id} : {pick.position}")
                    kickerFound = True
                    defFound = True
                    offFound = True
                    if pick.position == 7:
                        try:
                            current_player = kickerStats.objects.get(playerId=pick.id) 
                        except kickerStats.DoesNotExist:
                            kickerFound = False
                    elif pick.position == 8:
                        try:
                            current_player = defStats.objects.get(playerId=pick.id) 
                        except defStats.DoesNotExist:
                            defFound = False
                    elif pick.position == 5 or pick.position == 9:
                        offFound = False
                    else:
                        try:
                            current_player = playerStats.objects.get(playerId=pick.id) 
                        except playerStats.DoesNotExist:
                            offFound = False

                    if kickerFound and defFound and offFound:
                        print(f"updateGame player stats = {current_player}")
                        if current_player.projPts > 0:
                            pick.price = 115 * current_player.projPts
                            if current_player.ranking < 150:
                                adj = 2 * float(current_player.ranking)
                                adj = adj - float(current_player.ranking)
                                pick.price = 1.15 * float(pick.price)
                                pick.price = float(pick.price) + float(adj)
                            elif current_player.ranking < 250:
                                adj = 2.2 * float(current_player.ranking)
                                adj = adj - float(current_player.ranking)
                                pick.price = 1.10 * float(pick.price)
                                pick.price = float(pick.price) + float(adj)
                            elif current_player.ranking < 400:
                                adj = 2.25 * float(current_player.ranking)
                                adj = adj - float(current_player.ranking)
                                pick.price = 1.1 * float(pick.price)
                                pick.price = float(pick.price) + float(adj)
                            elif current_player.ranking < 500:
                                adj = 2.25 * float(current_player.ranking)
                                adj = adj - float(current_player.ranking)
                                pick.price = 1.15 * float(pick.price)
                                pick.price = float(pick.price) + float(adj)
                        elif current_player.ranking < 200:
                            pick.price = 1200 - float(current_player.ranking)
                        elif current_player.ranking < 300:
                            pick.price = 1100 - float(current_player.ranking)
                        elif current_player.ranking < 400:
                            pick.price = 1050 - float(current_player.ranking)
                        elif current_player.ranking < 500:
                            pick.price = 1000 - float(current_player.ranking)             
                        elif current_player.ranking < 600:
                            adj = .95 * float(current_player.ranking)
                            pick.price = 950 - float(current_player.ranking)
                        elif current_player.ranking < 700:
                            adj = .85 * float(current_player.ranking)
                            pick.price = 900 - float(current_player.ranking)                      
                        elif current_player.ranking < 800:
                            adj = .75 * float(current_player.ranking)
                            pick.price = 750 - float(adj)   
                        elif current_player.ranking < 900:
                            adj = .6 * float(current_player.ranking)
                            pick.price = 600 - float(adj)   
                        elif current_player.ranking < 1000:
                            adj = .25 * float(current_player.ranking)
                            pick.price = 300 - float(adj)   
                        elif current_player.ranking > 1200:
                            adj = .05 * float(current_player.ranking)
                            pick.price = 100 - float(adj)   
                        else:
                            adj = .15 * float(current_player.ranking)
                            pick.price = 200 - float(adj)   
                        pick.save()
                        print(f"updateGame pick = {pick.price}")
                    else:
                        print(f"updateGame current_player stats NOT found")

                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Prices for all players have been successfully updated.",
                }
                return render(request, "teams/success.html", context)
            elif action == "1":
                weekly_games = gameTeam.objects.filter(status=2).order_by('userTeamId')
                if not weekly_games.exists():
                    context = {
                        "reg_user": False,
                        "tab": "game",
                        "team_id": 32,
                        "message": "Games for current week not found to start.",
                    }
                    return render(request, "teams/error.html", context)

                print(f"updateGame remove last week's rankings")
                ranked_teams = weeklyRankings.objects.all()
                if ranked_teams.exists():
                    ranked_teams.delete()
                    print(f"updateGame ranked_teams deleted = {ranked_teams}")
                print(f"updateGame teams started count = {weekly_games.count()}")
                team = -1
                for game in weekly_games:
                    game.status = 3
                    game.save()
                    print(f"updateGame game = {game.id}")
                    if team != game.userTeamId:
                        team = game.userTeamId
                        new_team = weeklyRankings(username=game.username, teamId=game.userTeamId)
                        new_team.save()
                        print(f"updateGame new_team={new_team}")

                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Games for current week have been successfully started.",
                }
                return render(request, "teams/success.html", context)
            elif action == "2":
                weekly_games = gameTeam.objects.filter(status=3)
                if not weekly_games.exists():
                    context = {
                        "reg_user": False,
                        "tab": "game",
                        "team_id": 32,
                        "message": "Games for current week not found to complete.",
                    }
                    return render(request, "teams/error.html", context)

                print(f"updateGame teams completed count = {weekly_games.count()}")
                for game in weekly_games:
                    game.status = 4
                    game.save()
                    print(f"updateGame game = {game.id}")

                ranking_games = weeklyRankings.objects.all().order_by('-total')
                index = 1
                if ranking_games.exists():
                    print(f"update_game ranking_games count = {ranking_games.count()}")
                    for team in ranking_games:
                        team.ranking = index
                        team.save()
                        index = index + 1
                        print(f"update_game team in ranking_games={team}")

                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Games for current week have been successfully completed.",
                }
                return render(request, "teams/success.html", context)
            elif action == "3":
                weekly_games = gameTeam.objects.filter(status=3)
                if not weekly_games.exists():
                    context = {
                        "reg_user": False,
                        "tab": "game",
                        "team_id": 32,
                        "message": "Games for current week not found to reset.",
                    }
                    return render(request, "teams/error.html", context)

                print(f"updateGame teams reset count = {weekly_games.count()}")
                team = 0
                for game in weekly_games:
                    game.status = 2
                    game.save()
                    print(f"updateGame game = {game.id}")
                
                ranked_teams = weeklyRankings.objects.all()
                if ranked_teams.exists():
                    ranked_teams.delete()
                    print(f"updateGame ranked_teams deleted = {ranked_teams}")

                context = {
                    "reg_user": False, 
                    "tab": "game",
                    "team_id": 32,
                    "message": "Games for current week have been successfully reset.",
                }
                return render(request, "teams/success.html", context)
            elif action == "4":
                stats = defStats.objects.all()
                if not stats.exists():
                    context = {
                        "reg_user": False,
                        "tab": "game",
                        "team_id": 32,
                        "message": "Defense stats for current week not found.",
                    }
                    return render(request, "teams/error.html", context)

                print(f"updateGame teams def stats count = {stats.count()}")
                for pick in stats:
                    pick.fanPts = 0
                    pick.ptsAll = 0
                    pick.sack = 0
                    pick.safe = 0
                    pick.ints = 0 
                    pick.fumRec = 0
                    pick.TD = 0
                    pick.blkKick = 0
                    pick.retnYds = 0
                    pick.retnTD = 0
                    pick.save()
                    print(f"updateGame defense stats = {pick}")

                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Defense stats for current week have been successfully cleared.",
                }
                return render(request, "teams/success.html", context)
            elif action == "5":
                stats = kickerStats.objects.all()
                if not stats.exists():
                    context = {
                        "reg_user": False,
                        "tab": "game",
                        "team_id": 32,
                        "message": "Kicker stats for current week not found.",
                    }
                    return render(request, "teams/error.html", context)

                print(f"updateGame teams kicker stats count = {stats.count()}")
                for pick in stats:
                    pick.fanPts = 0
                    pick.under20 = 0
                    pick.under30 = 0
                    pick.under40 = 0
                    pick.under50 = 0 
                    pick.over50 = 0
                    pick.made = 0
                    pick.save()
                    print(f"updateGame kicker stats = {pick}")

                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Kicker stats for current week have been successfully cleared.",
                }
                return render(request, "teams/success.html", context)
            elif action == "6":
                stats = playerStats.objects.all()
                if not stats.exists():
                    context = {
                        "reg_user": False,
                        "tab": "game",
                        "team_id": 32,
                        "message": "Player stats for current week not found.",
                    }
                    return render(request, "teams/error.html", context)

                print(f"updateGame teams player stats count = {stats.count()}")
                for pick in stats:
                    pick.fanPts = 0
                    pick.passYds = 0
                    pick.passTD = 0
                    pick.passInt = 0
                    pick.rushAtts = 0 
                    pick.rushYds = 0
                    pick.rushTD = 0
                    pick.recvTgt = 0
                    pick.recvRec = 0
                    pick.recvYds = 0
                    pick.recvTD = 0 
                    pick.retnYds = 0
                    pick.retnTD = 0
                    pick.twoPT = 0 
                    pick.fumTot = 0
                    pick.fumLost = 0
                    pick.save()
                    print(f"updateGame player stats = {pick}")
                    
                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Player stats for current week have been successfully cleared.",
                }
                return render(request, "teams/success.html", context)
            elif action == "7":
                player_games = gameTeam.objects.filter(status=3).order_by('userTeamId')
                user_team = gameTeam.objects.filter(status=3).order_by('userTeamId').first()
                user_team_id = user_team.userTeamId
                user_team_total = 0
                team_username = None
                if player_games.exists():
                    print(f"update_game player_games count = {player_games.count()}")
                    for game in player_games:
                        print(f"update_game position = {game.positionChoice}, {game.positionId}")
                        if game.positionChoice == 6:
                            stats = defStats.objects.get(playerId=game.positionId)
                            print(f"update_game stats fanPts={stats.fanPts}")
                        elif game.positionChoice == 8:
                            stats = kickerStats.objects.get(playerId=game.positionId)
                            print(f"update_game stats fanPts={stats.fanPts}")
                        else:
                            stats = playerStats.objects.get(playerId=game.positionId)
                            print(f"update_game stats fanPts={stats.fanPts}")

                        print(f"update_game game={game.userTeamId}, team={user_team_id}")
                        if user_team_id == game.userTeamId:
                            if team_username != game.username:
                                team_username = game.username
                            game.pts = float(stats.fanPts)
                            game.save()
                            user_team_total = user_team_total + game.pts
                            print(f"update_game game in player_games={game.pts} and total={user_team_total}")
                        else:
                            game_team = weeklyRankings.objects.get(username=team_username, teamId=user_team_id)
                            game_team.total = user_team_total
                            game_team.save()
                            user_team_total = 0
                            user_team_id = game.userTeamId
                            print(f"update_game game_team={game_team}")
                            game.pts = float(stats.fanPts)
                            game.save()
                            user_team_total = user_team_total + game.pts
                            print(f"update_game game in player_games={game.pts} and total={user_team_total}")
                    game_team = weeklyRankings.objects.get(username=team_username, teamId=user_team_id)
                    game_team.total = user_team_total
                    game_team.save()
                    print(f"update_game game_team={game_team}")
                
                ranking_games = weeklyRankings.objects.all().order_by('-total')
                index = 1
                if ranking_games.exists():
                    print(f"update_game ranking_games count = {ranking_games.count()}")
                    for team in ranking_games:
                        team.ranking = index
                        team.save()
                        index = index + 1
                        print(f"update_game team in ranking_games={team}")
                                    
                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Rankings for current week have been successfully updated.",
                }
                return render(request, "teams/success.html", context)
        else:
            schedule = seasonSchedule.objects.all().order_by('week')
            if not schedule.exists():
                context = {
                    "reg_user": False,
                    "tab": "game",
                    "team_id": 32,
                    "message": "Season schedule for current week not found.",
                }
                return render(request, "teams/error.html", context)

            print(f"updateGame game count = {schedule.count()}")
            first_game = schedule.first()
            print(f"updateGame currentWeek = {first_game.currentWeek}")
            for game in schedule:
                game.currentWeek = week
                game.save()
                print(f"updateGame game = {game.id}")

            context = {
                "reg_user": False,
                "tab": "game",
                "team_id": 32,
                "message": "Current week has been successfully updated.",
            }
            return render(request, "teams/success.html", context)
    else:
        if request.user.is_authenticated:
            username = request.user
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, "users/register.html", {"message": "User does not exists."})
            admin_user = user.is_superuser
            reg_user = not admin_user
        else:
            return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

        schedule = seasonSchedule.objects.all().first()
        print(f"updateGame GET week = {schedule.currentWeek}")
        print(f"updateGame GET day = {schedule.currentDay}")
        context = {
            "user": username,
            "admin": admin_user,
            "week": schedule.currentWeek,
            "day": schedule.currentDay,
            "team_id": 32,
        }

        return render(request, "teams/updateGame.html", context)

def schedule(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})

    if request.method == "POST":
        week = request.POST.get('week')
        print(f"week = {week}")

        days = [0, 1, 2, 3]
        context = {
            "user": username,
            "admin": admin_user,
            "schedule": seasonSchedule.objects.filter(week=week).filter(day=0),
            "schedule1": seasonSchedule.objects.filter(week=week).filter(day=1),
            "schedule2": seasonSchedule.objects.filter(week=week).filter(day=2),
            "schedule3": seasonSchedule.objects.filter(week=week).filter(day=3),
            "year": 2019,
            "week": week,
            "team_id": 32,
            "days": days,
        }
        print(f"schedule admin = {admin_user}")
        return render(request, "teams/viewSchedule.html", context)
    else:
        print(f"teams = {seasonSchedule.objects.all().order_by('week')}")
        context = {
            "user": username,
            "admin": admin_user,
            "schedule": seasonSchedule.objects.all().order_by('week'),
            "year": 2019,
            "week": 0,
            "team_id": 32,
        }
        return render(request, "teams/viewSchedule.html", context)

def update_schedule(request, game):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        return render(request, "users/login.html", {"message": "User must be logged in to view teams."})
    
    message = "Game to update does not exist."
    if request.method == "POST":
        day = request.POST.get('day')
        month = request.POST.get('month')
        date = request.POST.get('date')
        awayTeam = request.POST.get('away')
        homeTeam = request.POST.get('home')

        print(f"updateSchedule: {day} {month} {date} away({awayTeam}) home({homeTeam}) #{game}")
        try:
            schedule = seasonSchedule.objects.get(pk=game)
        except seasonSchedule.DoesNotExist:
            context = {
                "reg_user": reg_user,
                "tab": "schedule",
                "team_id": 32,
                "message": message,
            }
            return render(request, "teams/error.html", context)

        schedule.day = int(day)
        schedule.month = int(month)
        schedule.date = int(date)
        schedule.awayTeam = int(awayTeam)
        schedule.homeTeam = int(homeTeam)
        schedule.save()

        print(f"updateSchedule POST: {schedule}")
        days = [0, 1, 2, 3]
        week = schedule.week
        context = {
            "user": username,
            "admin": admin_user,
            "schedule": seasonSchedule.objects.filter(week=week).filter(day=0),
            "schedule1": seasonSchedule.objects.filter(week=week).filter(day=1),
            "schedule2": seasonSchedule.objects.filter(week=week).filter(day=2),
            "schedule3": seasonSchedule.objects.filter(week=week).filter(day=3),
            "year": 2019,
            "week": week,
            "team_id": 32,
            "days": days,
        }
        return render(request, "teams/viewSchedule.html", context)
    else:
        try:
            schedule = seasonSchedule.objects.get(pk=game)
        except seasonSchedule.DoesNotExist:
            context = {
                "reg_user": reg_user,
                "tab": "schedule",
                "team_id": 32,
                "message": message,
            }
            return render(request, "teams/error.html", context)

        context = {
            "user": username,
            "admin": admin_user,
            "game": schedule,
            "team_id": 32,
        }
        return render(request, "teams/updateSchedule.html", context)