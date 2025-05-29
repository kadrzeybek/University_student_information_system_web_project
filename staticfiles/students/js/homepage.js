document.addEventListener("DOMContentLoaded", function () {
    const announcements = Array.from(document.querySelectorAll("#announcementsContainer .list-group-item"));
    const itemsPerPage = 5;
    const pagination = document.getElementById("pagination");

    function showPage(pageNumber) {
        const start = (pageNumber - 1) * itemsPerPage;
        const end = start + itemsPerPage;

        announcements.forEach((item, index) => {
            item.style.display = (index >= start && index < end) ? "block" : "none";
        });

        const pageButtons = pagination.querySelectorAll("li.page-item");
        pageButtons.forEach((li, index) => {
            li.classList.toggle("active", index === pageNumber - 1);
        });
    }

    function setupPagination() {
        const pageCount = Math.ceil(announcements.length / itemsPerPage);
        pagination.innerHTML = "";

        for (let i = 1; i <= pageCount; i++) {
            const li = document.createElement("li");
            li.className = "page-item";
            const btn = document.createElement("button");
            btn.className = "page-link";
            btn.innerText = i;
            btn.addEventListener("click", () => showPage(i));
            li.appendChild(btn);
            pagination.appendChild(li);
        }

        showPage(1);
    }

    setupPagination();
});