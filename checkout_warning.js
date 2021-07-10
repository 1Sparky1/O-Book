var link_was_clicked = false;

document.addEventListener("click", function(e) {
    if ((e.target.nodeName.toLowerCase() == 'a' && (!e.target.classList.contains('navbar-brand'))) || e.target.nodeName.toLowerCase() == 'button') {
        link_was_clicked = true;
        }
    else {
        link_was_clicked = false;
        };
    }, true);

window.onbeforeunload = function(){
    if (!link_was_clicked) {
        return 'Warning'; //Any text creates the same message.
        };
    };