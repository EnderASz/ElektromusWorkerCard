function checkAll(){
    var new_state = document.user_list_form.all_users_selection.checked;
    var checkboxes = document.getElementsByClassName("user-selection")
    for(var i=0; i<checkboxes.length; i++){
        checkboxes[i].checked = new_state;
    }
}

function updateCheckAllCheckbox(clicked){
    var all_checkbox = document.user_list_form.all_users_selection;
    if (!clicked.checked) all_checkbox.checked = false;

    var checkboxes = document.getElementsByClassName("user-selection")
    var all_checked = true;
    for(var i=0; i<checkboxes.length; i++){
        if(!checkboxes[i].checked){
            all_checked = false;
            break;
        }
    }
    if(all_checked) all_checkbox.checked = true;
}

function runAction(action, url, username, user_permission){
    document.user_list_form.action = url;
    const delete_question = `Czy napewno chcesz usunąć ${user_permission}: ${username}?`
    if((action=="delete" && confirm(delete_question)) || action=="change_password"){
        document.user_list_form.submit();
    }
    if(action=="manage"){
        document.user_list_form.method = "post";
        document.user_list_form.submit();
    }
}

function generateOverview(){
    var checked_users = document.querySelectorAll('[name="user_selection"]:checked')
    var users = [];
    for(var i = 0; i<checked_users.length; i++){
        users[i] = checked_users[i].value;
    }
    document.download_overview_form.users.value = users.toString();
    document.download_overview_form.submit();
}