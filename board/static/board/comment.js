
document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelector('#comment-set').addEventListener('click', (e) => {
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
    const parent = target.parentElement;
    let content = parent.querySelector('span').innerHTML;
    parent.innerHTML = `\
        <div class="row">\
            <div class="col-sm-9">\
                <input type="text" name="content" placeholder="Comment" class="form-control" maxlength="300" value="${content}"required></input>\
            </div>\
            <div class="col-sm-3">\
                <button class="btn btn-dark">Save</button>\
            </div>\
        </div>\
    `;
}


function editComment(target) {
    const commentBox = target.parentElement.parentElement.parentElement;
    const pk = commentBox.dataset.commentPk;
    let content = commentBox.querySelector('input').value;

    fetch(`http://127.0.0.1:8000/board/comment/${pk}/edit/`, {
        method: 'post',
        body: JSON.stringify({
            'content': content,
        })
    })
    .then(response => response.json())
    .then(data => {
        commentBox.innerHTML = "";
        commentBox.innerHTML = `\
            ${data['author']}\
            <span>${data['content']}</span>
            ${data['created_at']}
            <a href="#">Edit</a>
            <a href="#">Delete</a>
        `;
    });
}


function deleteComment(target) {
    const commentBox = target.parentElement;
    if (confirm('Are you sure you want to delete this comment?')) {
        const pk = commentBox.dataset.commentPk;
        fetch(`http://127.0.0.1:8000/board/comment/${pk}/delete/`)
        .then(response => response.json())
        .then(data => {
            if (data['status'] === true) {
                commentBox.remove();
            }
        });
    }
}