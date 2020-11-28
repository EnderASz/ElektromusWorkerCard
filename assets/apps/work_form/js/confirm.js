function confirmButton(){
    var action = document.confirmForm.action.value;
    var confirmed = confirm(
        `Czy napewno chcesz ${action == 'start_work' ? "rozpocząć pracę?" : (action == 'finish_work' ? "zakończyć pracę?" : "dodać czas pracy?")}`
    )
    if (confirmed) {
        document.confirmForm.submit();
    }
}
document.confirmForm.confirmBt.addEventListener('click', confirmButton);
