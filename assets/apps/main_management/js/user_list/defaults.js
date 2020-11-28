var today = new Date();
var week_ago = new Date();
week_ago.setDate(today.getDate() - 7);
document.download_overview_form.date_to.valueAsDate = today;
document.download_overview_form.date_from.valueAsDate = week_ago;
