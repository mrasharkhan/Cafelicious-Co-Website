function deleteItem(model, id) {
    if (confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
        fetch(`/srcadmin/delete/${model}/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Item deleted successfully!");
                const row = document.getElementById(`${model}-row-${id}`);
                if (row) row.remove();
                else location.reload();
            } else {
                alert("Delete failed: " + data.error);
            }
        });
    }
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
