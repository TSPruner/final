document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    var alink = document.querySelector('#login');
    alink.href = "";

    document.getElementById('posInfo').style.display = 'none';
    var position = document.getElementById('posInfo');
    var pos_selection = document.getElementById('pos');
    pos_selection.selectedIndex = position.innerHTML;

    document.getElementById('teamTypeInfo').style.display = 'none';
    var teamType = document.getElementById('teamTypeInfo');
    var type_selection = document.getElementById('teamType');
    type_selection.selectedIndex = teamType.innerHTML;

    document.getElementById('teamInfo').style.display = 'none';
    var teamInfo = document.getElementById('teamInfo');
    var team_selection = document.getElementById('teamId');
    team_selection.selectedIndex = teamInfo.innerHTML;
    
    document.getElementById('teamDiv').style.display = 'none';
    var teamDiv = document.getElementById('teamDiv');
    var div_selection = document.getElementById('div');
    if (teamDiv.innerText == "True")
        div_selection.selectedIndex = 0;
    else
        div_selection.selectedIndex = 1;
        
    document.getElementById('statusInfo').style.display = 'none';
    var statusInfo = document.getElementById('statusInfo');
    var status_selection = document.getElementById('status');
    status_selection.selectedIndex = statusInfo.innerHTML;

});
