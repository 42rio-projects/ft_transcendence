function fetchHTML(elementId, url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
        });
}

function fetchHTMLForm(elementId, event) {
    event.preventDefault();

    const form = event.target;
    const data = new FormData(form);

    fetch(form.action, {
        method: form.method,
        body: data
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
        });
}

window.onload = function() {
    fetchHTML("main", "home/");
};
