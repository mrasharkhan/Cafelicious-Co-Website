// for filtering tables
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName("tr");
  
    for (let i = 1; i < tr.length; i++) {
      let match = false;
      const td = tr[i].getElementsByTagName("td");
      for (let j = 0; j < td.length - 1; j++) {  // exclude action column
        if (td[j]) {
          const textValue = td[j].textContent || td[j].innerText;
          if (textValue.toLowerCase().includes(filter)) {
            match = true;
            break;
          }
        }
      }
      tr[i].style.display = match ? "" : "none";
    }
  }
  
  function showAllRows(tableId) {
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName("tr");
    for (let i = 1; i < tr.length; i++) {
      tr[i].style.display = "";
    }
  }