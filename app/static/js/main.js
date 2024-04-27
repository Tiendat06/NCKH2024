function collapsedSideBar() {
  document
    .getElementById("toggleButton")
    .addEventListener("click", function () {
      const specificSidebar = document.getElementById("header-sidebar");
      const sidebar = document.getElementById("sidebar");
      const content = document.querySelector(".content");
      const header_content = document.getElementById("header-content");
      const sidebar_para = document.querySelectorAll(".main-sidebar__para");
      const sidebar_item = document.querySelectorAll(".main-sidebar__item");
      const header_title = document.querySelector("#header-navbar__title");

      for (let i = 0; i < sidebar_para.length; i++) {
        if (
          sidebar_para[i].classList.contains("d-none") &&
          sidebar_item[i].classList.contains("justify-content-center")
        ) {
          sidebar_para[i].classList.remove("d-none");
          sidebar_item[i].classList.remove("justify-content-center");
        } else {
          sidebar_para[i].classList.add("d-none");
          sidebar_item[i].classList.add("justify-content-center");
        }
      }

      console.log(header_title);

      sidebar.classList.toggle("collapsed");
      header_content.classList.toggle("collapsed");
      specificSidebar.classList.toggle("collapsed");
      content.classList.toggle("collapsed");
    });
}

function fullScreen() {
  const fullscreenButton = document.getElementById(
    "navbar-bottom__icon--fullscreen"
  );
  const content = document.querySelector("#body");

  fullscreenButton.addEventListener("click", () => {
    if (document.fullscreenElement) {
      exitFullscreen();
    } else {
      requestFullscreen();
    }
  });

  function requestFullscreen() {
    if (content.requestFullscreen) {
      content.requestFullscreen();
    } else if (content.mozRequestFullScreen) {
      /* Firefox */
      content.mozRequestFullScreen();
    } else if (content.webkitRequestFullscreen) {
      /* Chrome, Safari and Opera */
      content.webkitRequestFullscreen();
    } else if (content.msRequestFullscreen) {
      /* IE/Edge */
      content.msRequestFullscreen();
    }
  }

  function exitFullscreen() {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
      /* Firefox */
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      /* Chrome, Safari and Opera */
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
      /* IE/Edge */
      document.msExitFullscreen();
    }
  }
}

function handleUploadImg() {
  const fileInput = document.getElementById("fileInput");
  const img = document.getElementById("xray-img");

  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      img.src = e.target.result;
    };

    reader.readAsDataURL(file);
  }
}

function downloadImage() {
  var imgElement = document.getElementById("xray-img--output");

  var a = document.createElement("a");
  a.href = imgElement.src;
  a.download = "downloaded_image.jpg";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

function ajaxInUserManagement() {
  // add
  $(document).ready(function () {
    $("#btn_add").click(function () {
      let name_add = $("#full_name_add").val();
      let gender_add = $("#gender_add").val();
      let email_add = $("#email_add").val();
      let dob_add = $("#dob_add").val();
      let phone_add = $("#phone_add").val();

      $.ajax({
        url: "/user/add",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          name: name_add,
          gender: gender_add,
          email: email_add,
          dob: dob_add,
          phone: phone_add
        }),
        success: function (response) {
          $("#error_adding_user").html(response);
          $("#error_adding_user_outer").removeClass("d-none");
          //console.log(response);
          //alert(response.message);
        },
        error: function (error) {
          console.log(error);
        }
      });
    });
  });

  // edit
  // $(document).ready(function() {
  //     $('#btn_edit').click(function() {
  //         let name_edit = $('#full_name_edit').val();
  //         let gender_edit = $('#gender_edit').val();
  //         let email_edit = $('#email_edit').val();
  //         let dob_edit = $('#dob_edit').val();
  //         let phone_edit = $('#phone_edit').val();
  //         let avatar_edit = $('#avatar_edit');
  //         var file = avatar_edit.prop('files')[0];

  //         let tmp_email = $('#tmp_email').val();
  //         let user_id = $('#user_id').val();
  //         let acc_id = $('#acc_id').val();

  //         $.ajax({
  //             url: '/user/edit',
  //             type: 'POST',
  //             contentType: false,
  //             data: JSON.stringify(
  //                 {
  //                     name : name_edit,
  //                     gender: gender_edit,
  //                     email: email_edit,
  //                     dob: dob_edit,
  //                     phone: phone_edit,
  //                     avatar: formData,
  //                     tmp_email: tmp_email,
  //                     user_id: user_id,
  //                     acc_id: acc_id,
  //                 }
  //             ),
  //             success: function(response) {
  //                 $('#error_editing_user').html(response)
  //                 $('#error_editing_user_outer').removeClass('d-none')
  //             },
  //             error: function(error) {
  //                 console.log(error);
  //             }
  //         });
  //     });
  // });

  // edit
  $(document).ready(function () {
    $("#btn_edit").click(function () {
      let name_edit = $("#full_name_edit").val();
      let gender_edit = $("#gender_edit").val();
      let email_edit = $("#email_edit").val();
      let dob_edit = $("#dob_edit").val();
      let phone_edit = $("#phone_edit").val();

      // Truy cập trực tiếp đối tượng tệp từ đối tượng jQuery prop('files')
      // let avatar_edit = $('#avatar_edit').prop('files')[0];

      let tmp_email = $("#tmp_email").val();
      let user_id = $("#user_id").val();
      let acc_id = $("#acc_id").val();
      let img = $("#img_edit").val();

      // console.log(avatar_edit.length)

      // var formData = new FormData();
      // formData.append('name', name_edit);
      // formData.append('gender', gender_edit);
      // formData.append('email', email_edit);
      // formData.append('dob', dob_edit);
      // formData.append('phone', phone_edit);
      // formData.append('tmp_email', tmp_email);
      // formData.append('user_id', user_id);
      // formData.append('acc_id', acc_id);

      $.ajax({
        url: "/user/edit",
        type: "POST",
        // contentType: false,
        // processData: false,
        contentType: "application/json",
        data: JSON.stringify({
          name: name_edit,
          gender: gender_edit,
          email: email_edit,
          dob: dob_edit,
          phone: phone_edit,
          tmp_email: tmp_email,
          user_id: user_id,
          acc_id: acc_id,
          img: img
        }),
        success: function (response) {
          $("#error_editing_user").html(response);
          $("#error_editing_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        }
      });
    });
  });

  $(document).ready(function () {
    $(".btn-show-details").on("click", function () {
      var name = $(this).data("name");
      var gender = $(this).data("gender");
      var email = $(this).data("email");
      var dob = $(this).data("dob");
      var phone = $(this).data("phone");
      var user_id = $(this).data("user_id");
      var acc_id = $(this).data("acc_id");
      var img_profile = $(this).data("img");

      // alert(userId)
      $("#full_name_edit").attr("value", name);
      $("#gender_edit").val(gender);
      $("#email_edit").attr("value", email);
      $("#dob_edit").val(dob);
      $("#phone_edit").val(phone);
      $("#tmp_email").attr("value", email);
      $("#user_id").attr("value", user_id);
      $("#acc_id").attr("value", acc_id);
      $("#img_edit").attr("value", img_profile);
    });
  });

  $(document).ready(function () {
    $(".btn-show-details-delete").on("click", function () {
      var id = $(this).data("id");
      var name = $(this).data("name");

      $("#userIdDelete").attr("value", id);
      $("#userNameDelete").attr("value", name);

      $("#userIdDelete-para").html("Are you sure to delete " + name + " ?");
    });
  });

  // delete
  $(document).ready(function () {
    $("#btn-delete").click(function () {
      var id = $("#userIdDelete").val();

      $.ajax({
        url: "/user/delete",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          id: id
        }),
        success: function (response) {
          $("#error_delete_user").html(response);
          $("#error_delete_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        }
      });
    });
  });
}

function jsInXray() {

    // edit and download file
  document.addEventListener("DOMContentLoaded", function () {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    var realImg = document.getElementById('xray-img--output');
    var image = document.getElementById("img_link_download");
    var editBtn = document.getElementById("editing");
    var downloadBtn = document.getElementById("downloading");
    var boundingBoxes = []; 
    var currentBox = null; 

    // canvas.width = image.width;
    // canvas.height = image.height;
    canvas.width = image.width;
    canvas.height = image.height;
    canvas.style.objectFit = 'contain'

    var isDrawing = false;
    var startX, startY, endX, endY;

    // Sự kiện khi nhấn nút "Edit"
    editBtn.addEventListener("click", function (e) {
      image.style.display = "none";
      canvas.style.display = "block";
      realImg.style.display = "none";
      isDrawing = true;
    });

    canvas.addEventListener("mousedown", function (e) {
      isDrawing = true;
      startX = e.offsetX;
      startY = e.offsetY;
    });

    canvas.addEventListener("mousemove", function (e) {
      if (isDrawing) {
        var currentX = e.offsetX;
        var currentY = e.offsetY;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(image, 0, 0); // Vẽ lại hình ảnh

        // Vẽ lại tất cả các bounding box đã lưu
        boundingBoxes.forEach(function (box) {
          ctx.beginPath();
          ctx.rect(
            box.startX,
            box.startY,
            box.endX - box.startX,
            box.endY - box.startY
          );
          ctx.strokeStyle = "red";
          ctx.lineWidth = 2;
          ctx.stroke();

          // Vẽ lựa chọn lên bounding box
          if (box.option) {
            ctx.font = "12px Arial";
            ctx.fillStyle = "black";
            ctx.fillText(box.option, box.startX + 10, box.startY + 20);
          }
        });

        ctx.beginPath();
        ctx.rect(startX, startY, currentX - startX, currentY - startY);
        ctx.strokeStyle = "red";
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    });

    canvas.addEventListener("mouseup", function () {
      isDrawing = false;
      endX = event.offsetX;
      endY = event.offsetY;
      currentBox = { startX: startX, startY: startY, endX: endX, endY: endY }; // Lưu bounding box đang được vẽ vào biến tạm thời
        //$("#selectOptionModal").modal("show"); // Hiển thị modal

        var modal = document.getElementById("selectOptionModal");
        modal.classList.add("show");
        modal.style.display = "block";
        modal.setAttribute("aria-modal", "true");
        modal.setAttribute("aria-hidden", "false");                
    
    });

    // Sự kiện khi nhấn nút "Save" trong modal
    document
      .getElementById("saveOption")
      .addEventListener("click", function () {
        var selectedOption = document.getElementById("options").value;
        console.log("Selected option:", selectedOption);

        // Lưu thông tin đã chọn vào bounding box đang được vẽ
        currentBox.option = selectedOption;

        // Đóng modal
        //$("#selectOptionModal").modal("hide");

        var modal = document.getElementById("selectOptionModal");
        modal.classList.remove("show");
        modal.style.display = "none";
        modal.setAttribute("aria-modal", "false");
        modal.setAttribute("aria-hidden", "true");
        

        // var modal = document.getElementById("selectOptionModal");
        // modal.style.display = "none";


        // Vẽ lựa chọn lên bounding box
        ctx.font = "12px Arial";
        ctx.fillStyle = "black";
        ctx.fillText(
          selectedOption,
          currentBox.startX + 10,
          currentBox.startY + 20
        );

        // Lưu bounding box vào mảng boundingBoxes
        boundingBoxes.push(currentBox);
      });

    // Sự kiện khi nhấn nút "Close" trong modal
    document
      .getElementById("closeModal")
      .addEventListener("click", function () {
        // Xóa bounding box tạm thời
        currentBox = null;

        // Đóng modal
        //$("#selectOptionModal").modal("hide");
        var modal = document.getElementById("selectOptionModal");
        modal.classList.remove("show");
        modal.style.display = "none";
        modal.setAttribute("aria-modal", "false");
        modal.setAttribute("aria-hidden", "true");

        // Vẽ lại canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(image, 0, 0); // Vẽ lại hình ảnh
        boundingBoxes.forEach(function (box) {
          ctx.beginPath();
          ctx.rect(
            box.startX,
            box.startY,
            box.endX - box.startX,
            box.endY - box.startY
          );
          ctx.strokeStyle = "red";
          ctx.lineWidth = 2;
          ctx.stroke();

          // Vẽ lựa chọn lên bounding box
          if (box.option) {
            ctx.font = "12px Arial";
            ctx.fillStyle = "black";
            ctx.fillText(box.option, box.startX + 10, box.startY + 20);
          }
        });
      });

    // Sự kiện khi nhấn nút "Download"
    downloadBtn.addEventListener("click", function () {
        // Lấy reference đến canvas và context
        var imageUrl = document.getElementById('img_link_download').src;
        var proxyUrl = 'xray/proxy-image?url=' + encodeURIComponent(imageUrl);

        var image = new Image();
        // Đảm bảo sử dụng cross-origin
        // Using like this, system will know that imgs from another place are safety
        image.crossOrigin = "Anonymous"; 

        image.onload = function() {
            // Vẽ hình ảnh lên canvas
            ctx.drawImage(image, 0, 0);
        };

        image.src = proxyUrl;

        canvas.toBlob(function(blob) {
            var link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "image_with_bounding_box.jpg";
            link.click();
        }, "image/jpeg");


        /*var imageUrl = document.getElementById('xray-img--output').src;
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext("2d");
    
        // Tạo một hình ảnh mới từ URL của proxy server
        var image = new Image();
        image.src = '/xray/proxy-image?url=' + encodeURIComponent(imageUrl);
    
        // Khi hình ảnh đã được load
        image.onload = function() {
            // Vẽ hình ảnh lên canvas
            ctx.drawImage(image, 0, 0);
    
            // Vẽ lại bounding boxes lên canvas
            boundingBoxes.forEach(function (box) {
                ctx.beginPath();
                ctx.rect(
                    box.startX,
                    box.startY,
                    box.endX - box.startX,
                    box.endY - box.startY
                );
                ctx.strokeStyle = "red";
                ctx.lineWidth = 2;
                ctx.stroke();

                // Vẽ option lên bounding box nếu có
                if (box.option) {
                    ctx.font = "16px Arial";
                    ctx.fillStyle = "black";
                    ctx.fillText(box.option, box.startX + 10, box.startY + 20);
                }
            });
    
            // Tạo một liên kết để tải hình ảnh mới
            var link = document.createElement("a");
            link.href = canvas.toDataURL("image/jpeg");
            link.download = "image_with_bounding_box.jpg";
            link.click();
        };*/
    });

    
    

  });


  //   check
  $("#checking").click(function () {
    $("#form").submit();
  });

  $(document).ready(function () {
    $("#myRange").on("input", function () {
      var formData = new FormData();

      // var fileInput = document.getElementById('upload');
      // if (fileInput.files.length > 0) {
      //     var file = fileInput.files[0];
      //     console.log(file.name)
      //     formData.append('file', file);
      // }
      let img_link = $("#img_link_predict").val();
      let range = $("#myRange").val();
      $("#rangeValue").text(range);
      formData.append("img_link", img_link);
      formData.append("range", range);
      console.log(img_link);
      console.log(range);

      $.ajax({
        url: "/xray/ajax/changeRange",
        type: "POST",

        processData: false,
        contentType: false,
        data: formData
      })
        .done((response) => {
          $("#xray-general__predict").html(response);
          // success: function(response) {
          // },
          // error: function(error) {
          //     console.log(error);
          // }
        })
        .fail((error) => {
          console.log(error);
        });
    });
  });

  // overlay
  document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form");
    const overlay = document.getElementById("overlay");

    form.addEventListener("submit", function (event) {
      event.preventDefault(); // Ngăn chặn form submit mặc định
      //overlay.style.display = 'block'; // Hiển thị overlay
      $("#overlay").removeClass("d-none");

      setTimeout(function () {
        //overlay.style.display = 'none'; // Ẩn overlay
        $("#overlay").addClass("d-none");

        // Xử lý dữ liệu trả về từ form
      }, 100000);
    });
  });

  // add record
  $(document).ready(function(){
    $('#btn_add-record').click(function(){
      var name = $('#full_name_add').val()
      var PID = $('#number_add').val()
      var age = $('#age_add').val()
      var phone = $('#phone_add').val()
      var gender = $('#gender_add').val()
      var address = $('#address_add').val()
      var dob = $('#date_add').val()
      var email = $('#email_add').val()
      var predict = $('#doctor_predict_add').val();

      $.ajax({
        type: 'POST',
        url: '/xray/saveRecord',
        contentType: "application/json",
        data: JSON.stringify({
            name: name,
            PID: PID,
            age: age,
            phone: phone,
            gender: gender,
            address: address,
            dob: dob,
            email: email,
            predict: predict
          }),
          success: function(response){
            $('#error_adding_record_outer').removeClass('d-none');
            $('#error_adding_record').html(response);
          },
          error: function (err){
            console.log(err);
          } 
      })
    })

  });

}

// function changeRange(){
// var rangeInput = document.getElementById("myRange");

// rangeInput.addEventListener("input", function() {
//     var value = rangeInput.value;

//     document.getElementById("rangeValue").textContent = value;
// });
// }

function handleUploadImg() {
  const fileInput = document.getElementById("upload");
  const img = document.getElementById("xray-img--output");
  const editImg = document.getElementById('img_link_download');
  img.style.display = 'block';
  editImg.style.display = 'none';

  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      const imgDataUrl = e.target.result;
      
      // Tạo một hình ảnh mới
      const image = new Image();
      
      // Khi hình ảnh đã được tải lên
      image.onload = function() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Thiết lập kích thước mới cho canvas
        const maxWidth = 330; // Đặt kích thước tối đa cho chiều rộng
        const maxHeight = 330; // Đặt kích thước tối đa cho chiều cao
        
        let newWidth = image.width;
        let newHeight = image.height;

        // Kiểm tra xem có cần thay đổi kích thước không
        if (image.width > maxWidth || image.height > maxHeight) {
          const aspectRatio = image.width / image.height;
          if (aspectRatio > 1) {
            newWidth = maxWidth;
            newHeight = maxWidth / aspectRatio;
          } else {
            newHeight = maxHeight;
            newWidth = maxHeight * aspectRatio;
          }
        }

        // Thiết lập kích thước mới cho canvas
        canvas.width = newWidth;
        canvas.height = newHeight;

        // Vẽ hình ảnh mới với kích thước mới lên canvas
        ctx.drawImage(image, 0, 0, newWidth, newHeight);

        // Lấy dữ liệu của hình ảnh từ canvas dưới dạng URL
        const resizedImgDataUrl = canvas.toDataURL('image/jpeg');

        // Hiển thị hình ảnh đã thay đổi kích thước
        img.src = resizedImgDataUrl;
      };

      // Đặt nguồn hình ảnh cho hình ảnh mới
      image.src = imgDataUrl;
    };

    reader.readAsDataURL(file);
  }
}

// function handleUploadImg() {
//   // console.log(this)
//   const fileInput = document.getElementById("upload");
//   const img = document.getElementById("xray-img--output");
//   var editImg = document.getElementById('img_link_download');
//   img.style.display = 'block';
//   editImg.style.display = 'none';
//   console.log(img);
//   console.log(fileInput);

//   const file = fileInput.files[0];

//   const file_path = fileInput.files[0].name;
//   console.log(file_path);


//   if (file) {
//     const reader = new FileReader();

//     reader.onload = function (e) {
//       img.src = e.target.result;
//       console.log(e.target.result);
//       // console.log('hello')
//     };
//     reader.readAsDataURL(file);
//   }
// }

// $.ajax({
//     url: '/xray/ajax/changeRange',
//     type: 'POST',
//     contentType: 'application/json',
//     data: JSON.stringify({
//         img_link: img_link,
//         range: range,

//     }),
//     success: function(response) {
//         $('#myTabContent').html(response)
//         //$('#error_editing_user_outer').removeClass('d-none')

//     },
//     error: function(error) {
//         console.log(error);
//     }
// });
