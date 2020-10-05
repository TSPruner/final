document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    var alink = document.querySelector('#login');
    alink.href = "";

    document.getElementById('currentWeek').style.display = 'none';
    var current_week = document.getElementById('currentWeek');
    var week_selection = document.getElementById('week');
    week_selection.selectedIndex = current_week.innerHTML;

});
