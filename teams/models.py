from django.db import models

# Create your models here.
class player(models.Model):
    TEAMS = (
        (0, 'Buffalo Bills'),
        (1, 'Miami Dolphins'),
        (2, 'New England Patriots'),
        (3, 'New York Jets'),
        (4, 'Baltimore Ravens'),
        (5, 'Cincinnati Bengals'),
        (6, 'Cleveland Browns'),
        (7, 'Pittsburgh Steelers'),
        (8, 'Houston Texans'),
        (9, 'Indianapolis Colts'),
        (10, 'Jacksonville Jaguars'),
        (11, 'Tennessee Titans'),
        (12, 'Denver Broncos'),
        (13, 'Kansas City Chiefs'),
        (14, 'Los Angeles Chargers'),
        (15, 'Oakland Raiders'),
        (16, 'Dallas Cowboys'),
        (17, 'New York Giants'),
        (18, 'Philadelphia Eagles'),
        (19, 'Washington Redskins'),
        (20, 'Chicago Bears'),
        (21, 'Detroit Lions'),
        (22, 'Green Bay Packers'),
        (23, 'Minnesota Vikings'),
        (24, 'Atlanta Falcons'),
        (25, 'Carolina Panthers'),
        (26, 'New Orleans Saints'),
        (27, 'Tampa Bay Buccaneers'),
        (28, 'Arizona Cardinals'),
        (29, 'Los Angeles Rams'),
        (30, 'San Francisco 49ers'),
        (31, 'Seattle Seahawks'),
    )

    POSITIONS = (
        (0, 'QB'),
        (1, 'RB'),
        (2, 'FB'),        
        (3, 'WR'),
        (4, 'TE'),
        (5, 'OL'),
        (6, 'DEF'),
        (7, 'PK'),
        (8, 'P'),
        (9, 'LS'),
    )

    TYPES = (
        ('Offense', 'Offense'),
        ('Defense', 'Defense'),
        ('Special Teams', 'Special Teams'),
    )

    STATE = (
        (0, 'Injured'),
        (1, 'Questionable'),
        (2, 'Probable'),
        (3, 'Out'),
        (4, 'PUP'),
        (5, 'Suspended'),
        (6, 'Active'),
    )

    position = models.IntegerField(default=0, choices=POSITIONS)
    teamType = models.CharField(max_length=15, choices=TYPES)
    teamId = models.IntegerField(default=0, choices=TEAMS)
    AFC = models.BooleanField(default=True)
    NFC = models.BooleanField(default=False)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    number = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    heightFeet = models.IntegerField(default=0)
    heightInches = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    experience = models.IntegerField(default=1)
    college = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    status = models.IntegerField(choices=STATE, default=6)
  
    def __str__(self):
        if self.position == 5:
            phrase = f"Offensive Line"
        elif self.position == 6 or self.position == 8:
            phrase = f"Defense/Special Teams"
        else:
            phrase = f"{self.firstName} {self.lastName} #{self.number}, {dict(player.POSITIONS)[self.position]}"
        return f"{phrase} for {dict(player.TEAMS)[self.teamId]} -{dict(player.STATE)[self.status]}"

class playerStats(models.Model):
    fanPts = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    projPts = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ranking = models.IntegerField(default=0)
    passYds = models.IntegerField(default=0)
    passTD = models.IntegerField(default=0)
    passInt = models.IntegerField(default=0)
    rushAtts = models.IntegerField(default=0)
    rushYds = models.IntegerField(default=0)
    rushTD = models.IntegerField(default=0)
    recvTgt = models.IntegerField(default=0)
    recvRec = models.IntegerField(default=0)
    recvYds = models.IntegerField(default=0)
    recvTD =  models.IntegerField(default=0)
    retnYds = models.IntegerField(default=0)
    retnTD =  models.IntegerField(default=0)
    twoPT = models.IntegerField(default=0)
    fumTot = models.IntegerField(default=0)
    fumLost = models.IntegerField(default=0)
    playerId = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.playerId} {self.fanPts} {self.projPts} {self.ranking} {self.passYds} {self.passTD} {self.passInt} {self.rushAtts} {self.rushYds} {self.rushTD} {self.recvTgt} {self.recvRec} {self.recvYds} {self.recvTD} {self.retnYds} {self.retnTD} {self.twoPT} {self.fumTot} {self.fumLost}"

class kickerStats(models.Model):
    fanPts = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    projPts = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ranking = models.IntegerField(default=0)
    under20 = models.IntegerField(default=0)
    under30 = models.IntegerField(default=0)
    under40 = models.IntegerField(default=0)
    under50 = models.IntegerField(default=0)
    over50 = models.IntegerField(default=0)
    made = models.IntegerField(default=0)
    playerId = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.fanPts} {self.projPts} {self.ranking} FGs: {self.under20}(0-19) {self.under30}(20-29) {self.under40}(30-39) {self.under50}(40-49) {self.over50}(50+) PAT Made:{self.made}"

class defStats(models.Model):
    fanPts = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    projPts = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ranking = models.IntegerField(default=0)
    ptsAll = models.IntegerField(default=0)
    sack = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    safe = models.IntegerField(default=0)
    ints = models.IntegerField(default=0)
    fumRec = models.IntegerField(default=0)
    TD = models.IntegerField(default=0)
    blkKick = models.IntegerField(default=0)
    retnYds = models.IntegerField(default=0)
    retnTD = models.IntegerField(default=0)
    playerId = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.fanPts} {self.projPts} {self.ranking} {self.ptsAll} {self.sack} {self.safe} {self.ints} {self.fumRec} {self.TD} {self.blkKick} {self.retnYds} {self.retnTD}"

class gameTeam(models.Model):
    POSITIONS = (
        (0, 'QB'),
        (1, 'RB1'),
        (2, 'RB2'),
        (3, 'WR1'),
        (4, 'WR2'),
        (5, 'TE'),
        (6, 'DEF'),
        (7, 'FLEX'),
        (8, 'K'),
    )

    STATE = (
        (0, 'Cancelled'),
        (1, 'Cart'),
        (2, 'Submitted'),
        (3, 'Game In Progress'),
        (4, 'Completed'),
    )
    
    WEEKS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
        (16, '16'),
        (17, '17'),
        (18, 'Wild Card'),
        (19, 'Divisional'),
        (20, 'Conference'),
        (21, 'Super Bowl'),
    )
    
    username = models.CharField(max_length=50)
    userTeamId = models.IntegerField(default=0)
    positionId = models.IntegerField(default=0)
    positionChoice = models.IntegerField(default=0, choices=POSITIONS)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.IntegerField(choices=STATE, default=1)
    positionDesc = models.CharField(default=None, max_length=100)
    pts = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    week = models.IntegerField(default=1, choices=WEEKS)

    def __str__(self):
        return f"Fantasy Player {self.id} on Fantasy Team {self.userTeamId} for customer {self.username}: pos {dict(gameTeam.POSITIONS)[self.positionChoice]} - {self.positionDesc} for ${self.price}"

class weeklyRankings(models.Model):
    username = models.CharField(max_length=50)
    teamId = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    ranking = models.IntegerField(default=0)

    def __str__(self):
        return f"ID {self.id}: Fantasy Team {self.teamId} for customer {self.username}: total pts{self.total} ranked {self.ranking}"

class seasonSchedule(models.Model):
    TEAMS = (
        (0, 'Buffalo Bills'),
        (1, 'Miami Dolphins'),
        (2, 'New England Patriots'),
        (3, 'New York Jets'),
        (4, 'Baltimore Ravens'),
        (5, 'Cincinnati Bengals'),
        (6, 'Cleveland Browns'),
        (7, 'Pittsburgh Steelers'),
        (8, 'Houston Texans'),
        (9, 'Indianapolis Colts'),
        (10, 'Jacksonville Jaguars'),
        (11, 'Tennessee Titans'),
        (12, 'Denver Broncos'),
        (13, 'Kansas City Chiefs'),
        (14, 'Los Angeles Chargers'),
        (15, 'Oakland Raiders'),
        (16, 'Dallas Cowboys'),
        (17, 'New York Giants'),
        (18, 'Philadelphia Eagles'),
        (19, 'Washington Redskins'),
        (20, 'Chicago Bears'),
        (21, 'Detroit Lions'),
        (22, 'Green Bay Packers'),
        (23, 'Minnesota Vikings'),
        (24, 'Atlanta Falcons'),
        (25, 'Carolina Panthers'),
        (26, 'New Orleans Saints'),
        (27, 'Tampa Bay Buccaneers'),
        (28, 'Arizona Cardinals'),
        (29, 'Los Angeles Rams'),
        (30, 'San Francisco 49ers'),
        (31, 'Seattle Seahawks'),
    )

    WEEKS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
        (13, '13'),
        (14, '14'),
        (15, '15'),
        (16, '16'),
        (17, '17'),
        (18, 'Wild Card'),
        (19, 'Divisional'),
        (20, 'Conference'),
        (21, 'Super Bowl'),
    )

    DAY = (
        (0, 'Thursday'),
        (1, 'Saturday'),
        (2, 'Sunday'),
        (3, 'Monday'),
    )

    MONTH = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )
    
    week = models.IntegerField(default=1, choices=WEEKS)
    day =  models.IntegerField(default=2, choices=DAY)
    date = models.IntegerField(default=1)
    month = models.IntegerField(default=9, choices=MONTH)
    year = models.IntegerField(default=2019)
    homeTeam = models.IntegerField(default=0, choices=TEAMS)
    awayTeam = models.IntegerField(default=0, choices=TEAMS)
    currentWeek = models.IntegerField(default=0, choices=WEEKS)
    currentDay =  models.IntegerField(default=0, choices=DAY)

    def __str__(self):
        return f"GameId {self.id} for week {self.week}: {dict(seasonSchedule.TEAMS)[self.awayTeam]} at {dict(seasonSchedule.TEAMS)[self.homeTeam]} on {dict(seasonSchedule.DAY)[self.day]}, {dict(seasonSchedule.MONTH)[self.month]} {self.date}"