document.addEventListener('DOMContentLoaded', () => {

    const user_name = document.getElementById('user-name');

    if (user_name) {
        document.getElementById('loginTab').style.backgroundColor = "lightgrey";
        var alink = document.querySelector('#login');
        alink.href = "";
    }
    else {
        document.getElementById('logoutTab').style.backgroundColor = "lightgrey";
        var alink = document.querySelector('#logout');
        alink.href = "";
    }
});

// Set main tab highlight to indicated page.
function format_selected_tab(e_th, e_link) {
    e_th.style.textDecoration = "none";
    e_link.style.color = "white";
    e_th.style.backgroundColor = "darkblue";
    e_th.style.borderBottomColor = "darkblue";
}

// Set previously selected main tab back to defaults.
function format_old_tab(e_th, e_link) {
    e_th.style.textDecoration = "none";
    e_link.style.color = "darkblue";
    e_th.style.backgroundColor = "white";
    e_th.style.borderBottomColor = "darkblue";
}