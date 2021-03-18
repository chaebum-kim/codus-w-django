
document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelector('#comment-set').addEventListener('click', (e) => {

        e.preventDefault();
        const target = e.target;

        if (target.innerHTML === 'Edit') {
            showEditBox(target);
        } else if (target.innerHTML === 'Delete') {
            deleteComment(target);
        } else if (target.innerHTML === 'Save') {
            editComment(target);
        }

    })
})


function showEditBox(target) {
    target.style.pointerEvents = 'none';
    const pk = target.dataset.commentPk;
    const commentBox = document.querySelector(`div[data-comment-pk='${pk}']`);
    const container = commentBox.querySelector('div:nth-child(2)');
    content = container.innerHTML.trim()
    container.innerHTML = `\
        <div class="row">\
            <div class="col-sm-9">\
                <input type="text" name="content" placeholder="Comment" class="form-control" maxlength="300" value="${content}"required></input>\
            </div>\
            <div class="col-sm-3">\
                <button data-comment-pk="${pk}" class="btn btn-dark">Save</button>\
            </div>\
        </div>\
    `;
}


function editComment(target) {
    const pk = target.dataset.commentPk;
    const commentBox = document.querySelector(`div[data-comment-pk='${pk}']`);
    let content = commentBox.querySelector('input').value;

    const contentBox = commentBox.querySelector('div:nth-child(2)');
    const info = commentBox.querySelector('div:nth-child(1)')
    const editedAt = info.querySelector('span:nth-child(4)');
    const editLink = info.querySelector('span:nth-child(5)').querySelector('a:first-child');
    editLink.style.pointerEvents = 'auto';

    fetch(`http://127.0.0.1:8000/board/comment/${pk}/edit/`, {
        method: 'post',
        body: JSON.stringify({
            'content': content,
        })
    })
    .then(response => response.json()
    )
    .then(data => {
        if (data['status'] === true) {
            const comment = data['comment'];
            contentBox.innerHTML = comment['content'];
            editedAt.innerHTML = `edited ${comment['updated_at']}`
        } 
    });
}


function deleteComment(target) {
    const pk = target.dataset.commentPk;
    const commentBox = document.querySelector(`div[data-comment-pk='${pk}']`);
    if (confirm('Are you sure you want to delete this comment?')) {
        fetch(`http://127.0.0.1:8000/board/comment/${pk}/delete/`, {
            method: 'put',
        })
        .then(response => response.json())
        .then(data => {
            if (data['status'] === true) {
                commentBox.remove();
            }
        });
    }
}