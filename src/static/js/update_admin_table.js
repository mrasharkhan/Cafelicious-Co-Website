// for modals
function openUpdateModal(model, id) {
    fetch(`/srcadmin/update/${model}/${id}/`)
      .then(res => res.json())
      .then(data => {
        // Update form fields based on the model
        if (model === 'store') {
          // Set the form action URL
          document.getElementById('updateForm-store').action = `/srcadmin/update/${model}/${id}/`;
          
          // Pre-fill the form with current store data
          document.getElementById('updateStoreId').value = data.store_id;
          document.getElementById('updateStoreName').value = data.store_name;
          document.getElementById('updateStoreLocation').value = data.location;
          document.getElementById('updateStoreContact').value = data.contact_info;
          document.getElementById('updateDateOpened').value = data.opening_date;
          document.getElementById('updateStatus').value = data.status;
          
          // Show the store modal
          document.getElementById('updateModal-store').style.display = 'block';
        }
        else if (model === 'category') {
          // Set the form action URL for category
          document.getElementById('updateForm-category').action = `/srcadmin/update/${model}/${id}/`;
  
          // Pre-fill the form with current category data
          document.getElementById('updateCategoryId').value = data.category_id;
          document.getElementById('updateCategoryName').value = data.category_name;
          document.getElementById('updateCategoryDescription').value = data.description;
  
          // Show the category modal
          document.getElementById('updateModal-category').style.display = 'block';
        }
        else if (model === 'admin') {
          // Set the form action URL
          document.getElementById('updateForm-admin').action = `/srcadmin/update/${model}/${id}/`;
      
          // Pre-fill the form with current admin data
          document.getElementById('updateAdminId').value = data.admin_id;
          document.getElementById('updateAdminName').value = data.name;
          document.getElementById('updateAdminEmail').value = data.email;
          document.getElementById('updatePassword').value = data.password;
          document.getElementById('updatePhone').value = data.phone;
          document.getElementById('updateDateJoined').value = data.date_joined;
      
          // Fetch the list of stores
          fetch('/srcadmin/stores/')
            .then(res => res.json())
            .then(storeList => {
              const dropdown = document.getElementById('updateStoreDropdown');
              dropdown.innerHTML = ''; // Clear previous options
      
              // Loop through the store list and create dropdown options
              storeList.forEach(store => {
                const option = document.createElement('option');
                option.value = store.id;  // store ID
                option.textContent = store.name;  // store name
      
                // If the store ID matches the admin's current store, mark it as selected
                if (store.id === data.store_id) {
                  option.selected = true;
                  document.getElementById('updateStoreId').value = store.id;  // Update the hidden input
                }
      
                dropdown.appendChild(option);
              });
              $(storeDropdown).select2();
            });
      
          // Show the modal
          document.getElementById('updateModal-admin').style.display = 'block';
      }
      else if (model === 'menu') {
        // Set the form action URL
        document.getElementById('updateForm-menu').action = `/srcadmin/update/${model}/${id}/`;
    
        // Pre-fill the form with current menu data
        document.getElementById('updateMenuId').value = data.menu_id;
        document.getElementById('updateMenuName').value = data.menu_name;
        document.getElementById('updateDescription').value = data.description;
        document.getElementById('updatePrice').value = data.price;
            // Set the current image
      const currentImage = document.getElementById('currentImage');
      if (data.image) {
          currentImage.src = data.image;
      } else {
          currentImage.src = '';  // No image available
      }


        // Fetch the list of stores
        fetch('/srcadmin/stores/')
        .then(res => res.json())
        .then(storeList => {
          const dropdown = document.getElementById('updateStoreDropdown2');
          dropdown.innerHTML = ''; // Clear previous options
  
          // Loop through the store list and create dropdown options
          storeList.forEach(store => {
            const option = document.createElement('option');
            option.value = store.id;  // store ID
            option.textContent = store.name;  // store name
  
            // If the store ID matches the menu's current store, mark it as selected
            if (store.id === data.store_id) {
              option.selected = true;
              document.getElementById('updateStoreId').value = store.id;  // Update the hidden input
            }
  
            dropdown.appendChild(option);
          });
          $(storeDropdown).select2();
        });
          fetch('/srcadmin/admins/')
          .then(res => res.json())
          .then(adminList => {
            const dropdown = document.getElementById('updateAdminDropdown');
            dropdown.innerHTML = ''; // Clear previous options
    
            // Loop through the admin list and create dropdown options
            adminList.forEach(admin => {
              const option = document.createElement('option');
              option.value = admin.id;  // admin ID
              option.textContent = admin.email;  // admin email
    
              // If the admin ID matches the menu's current admin, mark it as selected
              if (admin.id === data.admin_id) {
                option.selected = true;
                document.getElementById('updateAdminId').value = admin.id;  // Update the hidden input
              }
    
              dropdown.appendChild(option);
            });
            $(adminDropdown).select2();
          });
    
        // Show the modal
        document.getElementById('updateModal-menu').style.display = 'block';
    }
    else if (model === 'offer') {
      // Set the form action URL
      document.getElementById('updateForm-offer').action = `/srcadmin/update/${model}/${id}/`;
  
      // Pre-fill the form with current offer data
      document.getElementById('updateOfferId').value = data.offer_id;
      document.getElementById('updateOfferName').value = data.offer_name;
      document.getElementById('updateDescription2').value = data.offer_description;
      document.getElementById('updatePrice2').value = data.offer_price;
          // Set the current image

    const currentImage = document.getElementById('currentImage2');
    if (data.offer_image) {
      document.getElementById('currentImage2').src = data.offer_image;
  } else {
      document.getElementById('currentImage2').src = '';  // No image available
  }


      // Fetch the list of stores
      fetch('/srcadmin/stores/')
      .then(res => res.json())
      .then(storeList => {
        const dropdown = document.getElementById('updateStoreDropdown3');
        dropdown.innerHTML = ''; // Clear previous options

        // Loop through the store list and create dropdown options
        storeList.forEach(store => {
          const option = document.createElement('option');
          option.value = store.id;  // store ID
          option.textContent = store.name;  // store name
          // If the store ID matches the offer's current store, mark it as selected
          if (store.id === data.store_id) {
            option.selected = true;
            document.getElementById('updateStoreId').value = store.id;  // Update the hidden input
          }

          dropdown.appendChild(option);
        });
        $('#updateStoreDropdown3').select2();
      });
        
  
      // Show the modal
      document.getElementById('updateModal-offer').style.display = 'block';
  }

   else if (model === 'menucategory') {
      // Set form fields for menucategory modal
      document.getElementById('updateMenuCategoryId').value = data.menucategory_id;
  // Fetch the list of categories
  fetch('/srcadmin/categories/')
  .then(res => res.json())
  .then(categoryList => {
    const dropdown = document.getElementById('updateCategoryDropdown');
    dropdown.innerHTML = ''; // Clear previous options

    // Loop through the category list and create dropdown options
    categoryList.forEach(category => {
      const option = document.createElement('option');
      option.value = category.id;  // store ID
      option.textContent = category.name;  // store name

      // If the store ID matches the menucategory's current category, mark it as selected
      if (category.id === category.store_id) {
        option.selected = true;
        document.getElementById('updateCategoryId').value = category.id;  // Update the hidden input
      }
      dropdown.appendChild(option);
    });
    $(categoryDropdown).select2();
  });
    fetch('/srcadmin/menus/')
    .then(res => res.json())
    .then(menuList => {
      const dropdown = document.getElementById('updateMenuDropdown');
      dropdown.innerHTML = ''; // Clear previous options

      // Loop through the menu list and create dropdown options
      menuList.forEach(menu => {
        const option = document.createElement('option');
        option.value = menu.id;  // menu ID
        option.textContent = menu.name;  // menu name
        
        if (menu.id === data.menu_id) {
          option.selected = true;
          document.getElementById('updateMenuId').value = menu.id;  // Update the hidden input
        }
        dropdown.appendChild(option);
      });
      // Initialize Select2 on the category dropdown after populating it
      $(menuDropdown).select2();
    });
              
      // Show the menucategory modal
      document.getElementById('updateModal-menucategory').style.display = 'block';
  }

  else if (model === 'size') {
    // Set form fields for size modal
    document.getElementById('updateSizeId').value = data.id;
    document.getElementById('updatePriceMedium').value = data.price_m;
    document.getElementById('updatePriceLarge').value = data.price_l;

  fetch('/srcadmin/menus/')
  .then(res => res.json())
  .then(menuList => {
    const dropdown = document.getElementById('updateMenuDropdown2');
    dropdown.innerHTML = ''; // Clear previous options

    // Loop through the menu list and create dropdown options
    menuList.forEach(menu => {
      const option = document.createElement('option');
      option.value = menu.id;  // menu ID
      option.textContent = menu.name;  // menu name
      
      if (menu.id === data.menu_id) {
        option.selected = true;
        document.getElementById('updateMenuId2').value = menu.id;  // Update the hidden input
      }
      dropdown.appendChild(option);
    });
    // Initialize Select2 on the category dropdown after populating it
    $(menuDropdown2).select2();
  });
            
    // Show the menucategory modal
    document.getElementById('updateModal-size').style.display = 'block';
}

    })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
  function closeUpdateModal(model) {
    document.getElementById(`updateModal-${model}`).style.display = 'none';
  }