const BASE_URL = window.location.origin;

(function () {
  /* ========= sidebar toggle ======== */
  const sidebarNavWrapper = document.querySelector(".sidebar-nav-wrapper");
  const mainWrapper = document.querySelector(".main-wrapper");
  const menuToggleButton = document.querySelector("#menu-toggle");
  const menuToggleButtonIcon = document.querySelector("#menu-toggle i");
  const overlay = document.querySelector(".overlay");

  menuToggleButton.addEventListener("click", () => {
    sidebarNavWrapper.classList.toggle("active");
    overlay.classList.add("active");
    mainWrapper.classList.toggle("active");

    if (document.body.clientWidth > 1200) {
      if (menuToggleButtonIcon.classList.contains("lni-chevron-left")) {
        menuToggleButtonIcon.classList.remove("lni-chevron-left");
        menuToggleButtonIcon.classList.add("lni-menu");
      } else {
        menuToggleButtonIcon.classList.remove("lni-menu");
        menuToggleButtonIcon.classList.add("lni-chevron-left");
      }
    } else {
      if (menuToggleButtonIcon.classList.contains("lni-chevron-left")) {
        menuToggleButtonIcon.classList.remove("lni-chevron-left");
        menuToggleButtonIcon.classList.add("lni-menu");
      }
    }
  });
  overlay.addEventListener("click", () => {
    sidebarNavWrapper.classList.remove("active");
    overlay.classList.remove("active");
    mainWrapper.classList.remove("active");
  });
})();


// Handle user manage
const swalWithBootstrapButtons = Swal.mixin({
  customClass: {
    confirmButton: 'btn btn-success',
    cancelButton: 'btn btn-danger'
  },
  buttonsStyling: false
})


function deleteUser(data) {
  const url = BASE_URL + '/admin/user-manage/delete'
  const userId = data?.dataset?.userid;
  if(userId) {
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, cancel!',
      reverseButtons: true
    }).then((result) => {
         if (result.isConfirmed) {
        const ajxReq = $.ajax( url, {
            type : 'DELETE',
            data: {userId},
            success: function(resultData){
              Swal.fire(
                'Deleted!',
                'Account has been deleted.',
                'success'
              ).then(() => {
                location.reload();
              })
            },
            error: function(data) {
              alert('error');
            }
            
        });

      } else if (
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire(
          'Cancelled',
          'Your imaginary file is safe :)',
          'error'
        )
      }
    })
  }
}


function updateUser(data) {
  const userId = data?.dataset?.userid;
  if(userId) {

    $.ajax( BASE_URL + '/admin/user-manage/find-by-id', {
      type : 'GET',
      data: {userId},
      success: function(resultData){
        const userInfo = JSON.parse(resultData);
         Swal.fire({
          title: 'Update User',
          html:
          `<div class="row">
              <div class="col-12">
                <div class="input-style-1" style="text-align: initial;">
                  <label for="fullname">Fullname</label>
                  <input type="text" placeholder="Fullname" id="fullname" name="fullname" value="${userInfo.fullname}" required/>
                </div>
              </div> 
              <div class="col-12">
                <div class="input-style-1" style="text-align: initial;">
                  <label for="address">Address</label>
                  <input type="text" placeholder="Address" id="address" name="address" value="${userInfo.address}"required/>
                </div>
              </div> 
              <div class="col-12">
                <div class="input-style-1" style="text-align: initial;">
                  <label for="age">Age</label>
                  <input type="number" placeholder="Age" id="age" name="age" value="${userInfo.age}"required/>
                </div>
              </div> 
              <div class="col-12">
                <div class="input-style-1" style="text-align: initial;">
                  <label for="avatar">Avatar link</label>
                  <input type="text" placeholder="Avatar link" id="avatar" name="avatar" value="${userInfo.avatar}" required/>
                </div>
              </div> 
            </div>`,
          showCancelButton: true,
          focusConfirm: false,
        }).then((result) => {
          /* Read more about isConfirmed, isDenied below */
          if (result.isConfirmed) {
            const data = {
                userId,
                fullname: $('#fullname').val(),
                address: $('#address').val(),
                age: $('#age').val(),
                avatar: $('#avatar').val()
            };
             $.ajax( BASE_URL + '/admin/user-manage/update', {
                type : 'POST',
                data: {...data},
                success: function(resultData) {
                  Swal.fire('Changes are saved', resultData.message, 'success').then(() => {
                    location.reload();
                  })
                },
                error: function(error) {
                  Swal.fire('Changes are not saved', '', 'info')
                }
             })
          } 
        })
      },
      error: function(data) {
        Swal.fire('An error occurred', '', 'info')
      }
    })
  }
}


function recoveryUserDeleted() {
  Swal.fire({
  title: 'Are you sure?',
  text: "You won't be able to revert this!",
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes, recovery it!'
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax(BASE_URL + '/admin/user-manage/recovery', {
        type: 'GET',
        success: function(resultData) {
          Swal.fire(
            'Deleted!',
            'Your file has been deleted.',
            'success'
          ).then(() => {
            location.reload()
          })
        }
      })
      
    }
  }) 
}



function deleteAllUserDeleted() {
  Swal.fire({
  title: 'Are you sure?',
  text: "You won't be able to revert this!",
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes, recovery it!'
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax(BASE_URL + '/admin/user-manage/delete-all', {
        type: 'GET',
        success: function(resultData) {
          Swal.fire(
            'Deleted!',
            'Your file has been deleted.',
            'success'
          ).then(() => {
            location.reload()
          })
        }
      })
      
    }
  }) 
}