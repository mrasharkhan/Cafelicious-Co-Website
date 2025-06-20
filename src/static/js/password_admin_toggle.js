// password field toggle
function togglePassword(fieldId, btn) {
    const field = document.getElementById(fieldId);
    if (field.type === "password") {
      field.type = "text";
      btn.textContent = "👁️"; // Eye open
    } else {
      field.type = "password";
      btn.textContent = "👁️‍🗨"; // Eye with slash
    }
  }