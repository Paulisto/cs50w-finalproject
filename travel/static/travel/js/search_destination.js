function searchDestination() {
    var input, filter, container, card, i, a, txtValue;
    input = document.getElementById("search-bar");
    filter = input.value.toUpperCase();
    container = document.getElementById("all-destinations");
    card = container.getElementsByClassName("card");

    for (i = 0; i < card.length; i++) {
        a = card[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            card[i].style.display = "";
        } else {
            card[i].style.display = "none";
        }
    }
}