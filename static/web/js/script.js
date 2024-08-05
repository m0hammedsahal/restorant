let add = document.getElementById('add');
let addmore = document.getElementById('addmore');


function additem() {
    console.log(add)
    add.style.cssText = "hidden"
}


add.addEventListener("click", additem);
