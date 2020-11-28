function documentResized(){
    if(document.user_data_form){
        var title_tag = document.querySelector('main > header > h3')
        if(window.innerWidth<850) {
            title_tag.innerHTML = title_tag.innerHTML.replace(" - ", "<br>");
        } else {
            title_tag.innerHTML = title_tag.innerHTML.replace("<br>"," - ");
        }
    }
}

function documentLoaded(){
    documentResized();
}