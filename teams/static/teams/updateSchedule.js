document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    var alink = document.querySelector('#login');
    alink.href = "";

    document.getElementById('awayTeam').style.display = 'none';
    var teamInfo = document.getElementById('awayTeam');
    var team_selection = document.getElementById('away');
    team_selection.selectedIndex = teamInfo.innerHTML;
    
    document.getElementById('homeTeam').style.display = 'none';
    var teamInfo = document.getElementById('homeTeam');
    var team_selection = document.getElementById('home');
    team_selection.selectedIndex = teamInfo.innerHTML;

});
