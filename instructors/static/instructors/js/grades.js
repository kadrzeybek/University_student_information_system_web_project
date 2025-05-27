
    // Pagination script
document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 10;
    const table = document.getElementById("gradesTable");
    const tbody = table.querySelector("tbody");
    const allRows = Array.from(tbody.querySelectorAll("tr"));
    const pagination = document.getElementById("pagination");
    const searchInput = document.getElementById("searchInput");

    let filteredRows = [...allRows]; // Başlangıçta tüm satırlar

    function showPage(page, rows) {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        allRows.forEach(row => row.style.display = "none"); // tümünü gizle
        rows.slice(start, end).forEach(row => row.style.display = ""); // sayfaya düşenleri göster

        renderPagination(page, rows);
    }

    function renderPagination(currentPage, rows) {
        const totalPages = Math.ceil(rows.length / rowsPerPage);
        pagination.innerHTML = "";

        for (let i = 1; i <= totalPages; i++) {
            const li = document.createElement("li");
            li.className = `page-item ${i === currentPage ? "active" : ""}`;
            const a = document.createElement("a");
            a.className = "page-link";
            a.href = "#";
            a.innerText = i;
            a.addEventListener("click", function (e) {
                e.preventDefault();
                showPage(i, rows);
            });

            li.appendChild(a);
            pagination.appendChild(li);
        }
        }

        // Arama kutusu olayını dinle
        searchInput.addEventListener("keyup", function () {
            const searchTerm = this.value.toLowerCase();

            filteredRows = allRows.filter(row => {
                return Array.from(row.cells).some(cell =>
                    cell.textContent.toLowerCase().includes(searchTerm)
                );
            });

            showPage(1, filteredRows); 
        });

        showPage(1, filteredRows);
    });


    