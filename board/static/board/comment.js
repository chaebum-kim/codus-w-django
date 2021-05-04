document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#comment-set").addEventListener("click", (e) => {
    const target = e.target;

    if (target.innerHTML === "Edit") {
      showEditBox(target);
    } else if (target.innerHTML === "Delete") {
      confirmDelete(target);
    }
  });
});

function showEditBox(target) {
  target.style.pointerEvents = "none";
  const pk = target.dataset.commentPk;
  const commentBox = document.querySelector(`div[data-comment-pk='${pk}']`);
  const content = commentBox.querySelector(".comment-content");
  const edit = commentBox.querySelector(".comment-edit");

  content.style.display = "none";
  edit.style.display = "block";
}

function confirmDelete(target) {
  const pk = target.dataset.commentPk;

  if (confirm("Do you want to delete the comment?") === true) {
    fetch(`http://127.0.0.1:8000/board/comment/${pk}/delete/`).then(
      (response) => {
        if (response.status !== 200) {
          console.log("Failed");
        } else {
          location.reload();
        }
      }
    );
  }
}
