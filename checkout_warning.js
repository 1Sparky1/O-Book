var link_was_clicked = false;
document.addEventListener("click", function(e) {
  if (e.target.nodeName.toLowerCase() === 'a') {
    link_was_clicked = true;
  }
}, true);

window.onbeforeunload = function() {
  if(link_was_clicked) {
    link_was_clicked = false;
    return;
  }
  if (confirm("You are leaving without checking out - your entries may be cancelled")) {
    txt = "You pressed OK!";
    } else {
    txt = "You pressed Cancel!";
}

}