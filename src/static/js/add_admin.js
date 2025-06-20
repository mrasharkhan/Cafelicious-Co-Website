document.querySelectorAll('.open-modal').forEach(button => {
    button.addEventListener('click', () => {
      const model = button.dataset.model;
  
      fetch(`/form/${model}/`)
        .then(res => res.text())
        .then(html => {
          document.getElementById('modal-content').innerHTML = html;
          document.getElementById('form-modal').style.display = 'block';
  
          document.getElementById('dynamic-form').addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(`/submit/${model}/`, {
              method: 'POST',
              body: formData,
            })
            .then(res => res.text())
            .then(response => {
              if (response.includes('form')) {
                document.getElementById('modal-content').innerHTML = response;
              } else {
                document.getElementById('form-modal').style.display = 'none';
                window.location.reload(); // or show success message
              }
            });
          });
        });
    });
  });