document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("tbody").addEventListener("click", (e) => {
    const target = e.target.parentElement;
    window.location.href = target.dataset.href;
  });
});
