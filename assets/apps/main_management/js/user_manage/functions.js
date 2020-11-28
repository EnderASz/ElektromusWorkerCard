function isWorkerChanged(){
    var checkbox = document.user_data_form.is_worker;
    if(checkbox.checked){
        document.user_data_form.rate.readOnly = false;
        document.querySelector('#worker-data').classList.toggle("read-only", false)
    } else {
        document.user_data_form.rate.readOnly = true;
        document.querySelector('#worker-data').classList.toggle("read-only", true)
    }
}

function checkboxReadOnlyChecked(checkbox){
    if(checkbox.readOnly) {
        checkbox.checked = (checkbox.checked ? false : true);
    }
}