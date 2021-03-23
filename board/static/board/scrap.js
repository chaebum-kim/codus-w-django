
document.addEventListener('DOMContentLoaded', () => {

    document.addEventListener('click', e => {
        const target = e.target;
        if (target.innerHTML === 'scrap'){
            scrapArticle(target);
        } else if (target.innerHTML === 'unscrap') {
            unscrapArticle(target);
        }
    });
})


function scrapArticle(target) {
    const pk = target.parentElement.dataset.articlePk;
    fetch(`http://127.0.0.1:8000/board/article/${pk}/scrap/`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] === true) {
            target.innerHTML = 'unscrap';
        }
    });
}


function unscrapArticle(target) {
    const pk = target.parentElement.dataset.articlePk;
    fetch(`http://127.0.0.1:8000/board/article/${pk}/unscrap/`, {
        method: 'PUT',
    })
    .then(response => response.json())
    .then(data => {
        if (data['status'] === true) {
            target.innerHTML = 'scrap';
        }
    });
}