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

function downloadImage() {
  // var imgElement = document.getElementById("xray-img--output");

  var imageUrl = document.getElementById("xray-img--output").src;

  // Sử dụng Fetch API để tải hình ảnh từ URL
  fetch(imageUrl)
    .then((response) => response.blob()) // Chuyển đổi dữ liệu hình ảnh thành Blob
    .then((blob) => {
      // Tạo một URL từ Blob
      var url = window.URL.createObjectURL(blob);

      // Tạo một phần tử <a> để tạo ra một liên kết tải xuống
      var a = document.createElement("a");
      a.href = url;
      a.download = "image.jpg"; // Tên tệp khi tải xuống

      // Thêm phần tử <a> vào body
      document.body.appendChild(a);

      // Kích hoạt sự kiện click trên phần tử <a>
      a.click();

      // Xóa URL của Blob sau khi tải xuống hoàn tất
      window.URL.revokeObjectURL(url);
    });
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
          phone: phone_add,
        }),
        success: function (response) {
          $("#error_adding_user").html(response);
          $("#error_adding_user_outer").removeClass("d-none");
          //console.log(response);
          //alert(response.message);
        },
        error: function (error) {
          console.log(error);
        },
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
          img: img,
        }),
        success: function (response) {
          $("#error_editing_user").html(response);
          $("#error_editing_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        },
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
          id: id,
        }),
        success: function (response) {
          $("#error_delete_user").html(response);
          $("#error_delete_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        },
      });
    });
  });
}

function removeQueryString(url) {
  var parts = url.split("?");
  var cleanedUrl = parts[0];
  return cleanedUrl;
}

function onClickItem(event) {
  console.log('hi world')
  var itemId = event.target.id;


}

function sumUpManualBoundingBoxAndDownloadInXray() {
  // edit and download file
  $(document).ready(function () {
    // document.addEventListener("DOMContentLoaded", function () {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");
    var realImg = document.getElementById("xray-img--output");
    var image = document.getElementById("img_link_download");
    // console.log(image);
    // var imgSrc = image.src;
    // image.src = removeQueryString(imgSrc);
    var editBtn = document.getElementById("editing");
    var downloadBtn = document.getElementById("downloading");
    var undoBtn = document.getElementById("btn-undo-xray");
    var redoBtn = document.getElementById("btn-redo-xray");
    var isClickOnBoundingBox = false;
    var redoStackBB = [];
    var redoStackHM = [];
    var redoStackNote = [];
    var currentBox = null;
    var boundingBoxes = [];
    var hashMapData = [];
    var hashMapNote = [];

    var isDrawing = false;
    var startX, startY, endX, endY;
    canvas.width = 330;
    canvas.height = 330;

    // Sự kiện khi nhấn nút "Edit"
    editBtn.addEventListener("click", function (e) {
      // var imgSplit = image.src.split('?')
      // image.src = imgSplit[0];
      // console.log("split:"+image.src);

      // console.log("Width:"+image.width);
      // console.log("Height:"+image.height);

      // canvas.width = ( image.width) ;
      // canvas.height = ( image.height) ;
      // canvas.width = canvas.clientWidth;
      // canvas.height = canvas.clientHeight;

      // image.src = imgSplit[0]+"?"+imgSplit[1];
      canvas.style.objectFit = "contain";

      image.style.display = "none";
      canvas.style.display = "block";
      realImg.style.display = "none";
      document.getElementById("xray-btn--undo").style.display = "block";
      document.getElementById("xray-btn--redo").style.display = "block";
      isDrawing = true;
    });


    function redrawCanvas() {
      isDrawing = true;
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
          ctx.textBaseline = "top"; // Đặt baseline văn bản

          // Tính toán kích thước văn bản
          var textWidth = ctx.measureText(box.option).width;
          var textHeight = 12; // 12px Arial

          // Vẽ nền đỏ cho văn bản
          ctx.fillStyle = "red";
          ctx.fillRect(box.startX, box.startY - 13, textWidth, textHeight);

          // Vẽ văn bản trắng lên trên
          ctx.fillStyle = "white";
          ctx.fillText(box.option, box.startX, box.startY - 13);
        }
      });
    }


    canvas.addEventListener("mousedown", function (e) {
      if (!isClickOnBoundingBox) {
        isDrawing = true;
        startX = e.offsetX;
        startY = e.offsetY;
      } else {
        isDrawing = false;
      }
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
            ctx.textBaseline = "top"; // Đặt baseline văn bản

            // Tính toán kích thước văn bản
            var textWidth = ctx.measureText(box.option).width;
            var textHeight = 12; // 12px Arial

            // Vẽ nền đỏ cho văn bản
            ctx.fillStyle = "red";
            ctx.fillRect(box.startX, box.startY - 13, textWidth, textHeight);

            // Vẽ văn bản trắng lên trên
            ctx.fillStyle = "white";
            ctx.fillText(box.option, box.startX, box.startY - 13);
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
      // isDownloadOk = true;
      endX = event.offsetX;
      endY = event.offsetY;
      currentBox = { startX: startX, startY: startY, endX: endX, endY: endY }; // Lưu bounding box đang được vẽ vào biến tạm thời
      //$("#selectOptionModal").modal("show"); // Hiển thị modal

      isClickOnBoundingBox = false;
      var modal = document.getElementById("selectOptionModal");
      modal.classList.add("show");
      modal.style.display = "block";
      modal.setAttribute("aria-modal", "true");
      modal.setAttribute("aria-hidden", "false");
    });

    undoBtn.addEventListener("click", function () {
      if (boundingBoxes.length != 0 && hashMapData.length != 0) {
        var itemBB = boundingBoxes.pop();
        redoStackBB.push(itemBB);
        redrawCanvas();
        var itemHM = hashMapData.pop();
        redoStackHM.push(itemHM);

        var itemNote = hashMapNote.pop();
        redoStackNote.push(itemNote);

        writeDataToFront(hashMapData, hashMapNote);
        isDrawing = false;
      }
    });

    redoBtn.addEventListener("click", function () {
      if (redoStackBB.length != 0 && redoStackHM.length != 0) {
        isDrawing = false;
        boundingBoxes.push(redoStackBB.pop());
        redrawCanvas();
        hashMapData.push(redoStackHM.pop());
        hashMapNote.push(redoStackNote.pop());
        writeDataToFront(hashMapData, hashMapNote);
        isDrawing = false;
      }
    });

    function writeDataToFront(hashMapData, hashMapNote) {
      var htmlContent = "";
      var indexNote = 0;
      hashMapData.forEach(function (item) {

        htmlContent +=
          "<div style='cursor: pointer' class='text-light xray-predict__item w-100 mb-2'>" +
          "<div class='xray-predict__title d-flex flex-wrap mb-2'>" +
          "<p class='mb-0 w-75 text-left text-secondary'>" +
          item + ' (' + hashMapNote[indexNote] + ')' +
          "</p>" +
          "<div class='w-25 text-right'>" +
          "<input type='hidden' class='delete-doctor-predict' value='" +
          item +
          "' />" +
          "<i onclick='onClickItem(event)' id='" +
          item +
          "' style='font-size: 18px' class='doctor-predict-icon fa-solid fa-pen-to-square text-right text-danger'></i>" +
          "</div>" +
          "</div>" +
          "<div style='height: 5px;background-color: #ccc;border-radius: 10px;overflow: hidden;' class='xray-percent--outer w-100'>" +
          "<div style='width: 100%; background-color: red' class='xray-percent h-100'></div>" +
          "</div>" +
          "</div>";

        indexNote++;
      });
      // <i class="fa-solid fa-pen-to-square"></i>
      $("#profile").html(htmlContent);
    }

    // Sự kiện khi nhấn nút "Save" trong modal
    document.getElementById("saveOption").addEventListener("click", function () {
      var selectedOption = document.getElementById("options").value;
      var noteOption = document.getElementById("note-id").value;
      // console.log("Selected option:", selectedOption);

      // Lưu thông tin đã chọn vào bounding box đang được vẽ
      currentBox.option = selectedOption;

      // Đóng modal
      var modal = document.getElementById("selectOptionModal");
      modal.classList.remove("show");
      modal.style.display = "none";
      modal.setAttribute("aria-modal", "false");
      modal.setAttribute("aria-hidden", "true");

      // Vẽ lựa chọn lên bounding box
      ctx.font = "12px Arial";
      ctx.textBaseline = "top"; // Đặt baseline văn bản

      // Tính toán kích thước văn bản
      var textWidth = ctx.measureText(selectedOption).width;
      var textHeight = 12; // 12px Arial

      // Vẽ nền đỏ cho văn bản
      ctx.fillStyle = "red";
      ctx.fillRect(currentBox.startX, currentBox.startY - 13, textWidth, textHeight);

      // Vẽ văn bản trắng lên trên
      ctx.fillStyle = "white";
      ctx.fillText(selectedOption, currentBox.startX, currentBox.startY - 13);

      // Lưu bounding box vào mảng boundingBoxes
      boundingBoxes.push(currentBox);

      // Thêm phần tử vào Map
      hashMapData.push(selectedOption);
      hashMapNote.push(noteOption);

      $("#note-id").html('');

      writeDataToFront(hashMapData, hashMapNote);
    });

    document.getElementById("closeModal").addEventListener("click", function () {
      // Xóa bounding box tạm thời
      currentBox = null;

      // Đóng modal
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
          ctx.textBaseline = "top"; // Đặt baseline văn bản

          // Tính toán kích thước văn bản
          var textWidth = ctx.measureText(box.option).width;
          var textHeight = 12; // 12px Arial

          // Vẽ nền đỏ cho văn bản
          ctx.fillStyle = "red";
          ctx.fillRect(box.startX, box.startY - 13, textWidth, textHeight);

          // Vẽ văn bản trắng lên trên
          ctx.fillStyle = "white";
          ctx.fillText(box.option, box.startX, box.startY - 13);
        }
      });
    });


    var isDownloading = false;
    // Sự kiện khi nhấn nút "Download"
    downloadBtn.addEventListener("click", async function () {
      var count = 0;
      if (isDownloading) {
        // alert("You must wait 5s")
        return;
      }
      isDownloading = await true;
      // Lấy reference đến canvas và context
      if (boundingBoxes.length != 0 && hashMapData.length != 0) {
        var imageUrl = document.getElementById("img_link_download").src;
        var proxyUrl = "xray/proxy-image?url=" + encodeURIComponent(imageUrl);

        var imageClass = new Image();
        // Đảm bảo sử dụng cross-origin
        // Using like this, system will know that imgs from another place are safety
        imageClass.crossOrigin = "Anonymous";

        imageClass.onload = function () {
          // Vẽ hình ảnh lên canvas
          ctx.drawImage(imageClass, 0, 0);
        };

        imageClass.src = proxyUrl;

        canvas.toBlob(function (blob) {
          if (count == 0) {
            var link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "image_with_bounding_box.jpg";
            link.click();
            count = count + 1;
          }
        }, "image/jpeg");
        isDrawing = false;
        redrawCanvas();
      } else {
        if (count == 0) {
          downloadImage();
          isDrawing = false;
          redrawCanvas();
          count = count + 1;
        }
      }
      redrawCanvas();

      setTimeout(async function () {
        isDownloading = await false;
        isDrawing = false;
      }, 15000);
    });
  });
}

function jsAjaxChangRangeInXray() {
  $(document).ready(function () {
    // abort previous request
    // let currentRequest;
    // Locking
    let isLocked = false;
    $("#myRange").on("input", function () {
      // if(currentRequest){
      //   currentRequest.abort();
      // }
      if (isLocked) return
      var formData = new FormData();

      isLocked = true;
      // $('#overlay').removeClass('d-none');
      let img_link = $("#img_link_predict").val();
      let range = $("#myRange").val();
      $("#rangeValue").text(range);
      formData.append("img_link", img_link);
      formData.append("range", range);
      //   console.log(img_link);
      //   console.log(range);

      currentRequest = $.ajax({
        url: "/xray/ajax/changeRange",
        type: "POST",

        processData: false,
        contentType: false,
        data: formData,
        complete: function () {
          isLocked = false;
          // $('#overlay').addClass('d-none');

        }
      })
        .done((response) => {
          $("#xray-general__predict").html(response);
          // success: function(response) {
          // },
          // error: function(error) {
          //     console.log(error);
          // }
          // sumUpManualBoundingBoxAndDownloadInXray()
        })
        .fail((error) => {
          console.log(error);
        });
    });
  });
}

function jsInXray() {
  //   check
  $(document).ready(function () {
    $("#checking").click(function () {
      $("#form").submit();
    });
  });

  // overlay
  // document.addEventListener("DOMContentLoaded", function () {
  $(document).ready(function () {
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
  // })

  // add record
  $(document).ready(function () {
    $("#btn_add-record").click(function () {
      var name = $("#full_name_add").val();
      var PID = $("#number_add").val();
      var age = $("#age_add").val();
      var phone = $("#phone_add").val();
      var gender = $("#gender_add").val();
      var address = $("#address_add").val();
      var dob = $("#date_add").val();
      var email = $("#email_add").val();
      var predict = $("#doctor_predict_add").val();

      $.ajax({
        type: "POST",
        url: "/xray/saveRecord",
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
          predict: predict,
        }),
        success: function (response) {
          $("#error_adding_record_outer").removeClass("d-none");
          $("#error_adding_record").html(response);
        },
        error: function (err) {
          console.log(err);
        },
      });
    });
  });

  // open-img
  $(document).ready(function () {
    $("#xray-img__small").click(function () {
      // var imgUrl = $(this).attr('src');
      var imgUrl = document.getElementById("xray-img__small").src;
      $("#xray-img--show").attr("src", imgUrl);
    });
  });
// app

  // open-img-show-body
  // $(document).ready(function () {
  //   $("#pills-body-target-tab").click(function () {
  //     // var imgUrl = $(this).attr('src');
  //     var imgUrl = document.getElementById("xray-img--small-body").src;
  //     // console.log('hi world');
  //     $("#xray-img--show-body").attr("src", imgUrl);
  //   });
  // });

  // check body target
  $(document).ready(function () {
    var selectedOptions = [];
    let isLocked = false;
    $('#btn__body-target--submit').click(function () {
      $('#overlay__show-body').removeClass('d-none');
      if (isLocked) return

      isLocked = true;

      $('input[name="checkbox__body-target"]:checked').each(function () {
        selectedOptions.push($(this).val());
      });
      console.log(selectedOptions);
      var img = document.getElementById("upload-body");

      var formData = new FormData();
      console.log(img.files[0]);
      formData.append("file", img.files[0]);
      formData.append('checkbox', selectedOptions);
      selectedOptions.splice(0, selectedOptions.length);
      
      $.ajax({
        type: 'POST',
        url: '/xray/show_body_target',
        contentType: false,
        processData: false,
        data: formData,
        success: function (response) {
          $('#body-target--showed').html(response);
        },
        fail: function (error) {
          console.log(error);
        },
        complete: function () {
          $('#overlay__show-body').addClass('d-none');
          isLocked = false;
        }
      })
    })
  })

  // upload ratio
  $(document).ready(function () {
    let isLocked = false;
    $('#btn__upload-ratio').click(function () {
      // console.log('hi world');
      $('#overlay__show-body').removeClass('d-none');
      if (isLocked) return

      isLocked = true;

      var img = document.getElementById("upload-ratio");

      var formData = new FormData();
      // console.log(img.files[0]);
      formData.append("file", img.files[0]);
      // formData.append('checkbox', selectedOptions);
      // selectedOptions.splice(0, selectedOptions.length);
      
      $.ajax({
        type: 'POST',
        url: '/xray/upload_ratio',
        contentType: false,
        processData: false,
        data: formData,
        success: function (response) {
          // console.log(response);

          $('#xray-img-ratio').attr('src', response.processed_image_url+"?random_code="+generateCode(8));
        },
        fail: function (error) {
          console.log(error);
        },
        complete: function () {
          $('#overlay__show-body').addClass('d-none');
          isLocked = false;
        }
      })
    })
  })

  $(document).ready(function (){
    $('#btn__upload-angle').click(function (){

    })
  })

//   upload contours
  $(document).ready(function () {
      let isLocked = false;
      $('#btn__upload-contours').click(function (){
          $('#overlay__show-body').removeClass('d-none');

          var formData = new FormData();
          var img = document.getElementById("upload-contours");
          formData.append("file", img.files[0]);
          if (isLocked) return

          isLocked = true;

          $.ajax({
            type: 'POST',
            url: '/xray/upload_contours',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response){
                document.getElementById('xray-img-contours').style = 'margin-right: 500px !important;';

                $('#xray-img-contours').attr('src', response.processed_image_url+"?random_code="+generateCode(8));
            },
            error: function (error){
                console.log(error);
            },
            complete: function (xhr, status){
                console.log(status);
                $('#overlay__show-body').addClass('d-none');
                isLocked = false;
            }
          })
      })

  })


  $(document).ready(function (){
    $('#btn-submit__body-target').click(function (){
      let selectedBodyOptions = [];
      let selectedFunctionOptions = [];
      let img_url = document.getElementById('body-target__img').src;
      const fileInput = document.getElementById('upload-ratio');
      const file = fileInput.files[0];

      $('input[name="checkbox__body-target"]:checked').each(function () {
        selectedBodyOptions.push($(this).val());
      });

      $('input[name="checkbox__body-target--function"]:checked').each(function () {
        selectedFunctionOptions.push($(this).val());
      });

      // console.log(selectedBodyOptions);
      // console.log(selectedFunctionOptions);
      // console.log(img_url);
      var formData = new FormData();
      formData.append('body-options', JSON.stringify(selectedBodyOptions));
      formData.append('function-options', JSON.stringify(selectedFunctionOptions));
      formData.append('file', file);

      $('#overlay__show-body').removeClass('d-none');
      fetch('/xray/combine_body_target', {
        method: 'POST',
        body: formData
      })
          .then(response => response.json())
          .then(data => {
            // console.log(data)
            img_url = data['img_url']
            console.log(data)
            if (data['isAngle'] === true){
              document.getElementById('body-target__img').style = 'margin-right: 450px; width: 100%; height: 100%';
            } else{
              document.getElementById('body-target__img').style = 'margin-right: 0';
            }
            document.getElementById('body-target__img').src = img_url;
          })
          .catch(error => {
            console.log(error)
          })
          .finally(() => {
            $('#overlay__show-body').addClass('d-none');
          })
    })

  })

}

function generateCode(length = 8) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

function jsInPatient() {
  // delete
  $(document).ready(function () {
    $(".btn-show-details-delete").on("click", function () {
      var id = $(this).data("id");
      var name = $(this).data("name");

      $("#patientIdDelete").attr("value", id);
      $("#patientNameDelete").attr("value", name);

      $("#patientIdDelete-para").html("Are you sure to delete " + name + " ?");
    });
  });

  // $(document).ready(function(){
  //   $("#btn-delete").click(function(){
  //     var id = $("#patientIdDelete").val();

  //     $.ajax({
  //       url: "/patient/delete",
  //       type: "POST",
  //       contentType: "application/json",
  //       data: JSON.stringify({
  //         id: id
  //       }),
  //       success: function(response) {
  //         $("#error_delete_user").html(response);
  //         $("#error_delete_user_outer").removeClass("d-none");
  //       },
  //       error: function(error) {
  //         console.log(error);
  //       }
  //     });
  //   });
  // });

  // show details record
  $(document).ready(function () {
    $(".btn-show-details-medical-record").click(function () {
      var patient_id = $(this).data("patient_id");
      // console.log(patient_id);
      var name = $(this).data("name");

      $.ajax({
        url: "/patient/medical_record",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          patient_id: patient_id,
          name: name,
        }),
        success: function (response) {
          $("#more-patient-medical-record").html(response);
          // $("#error_editing_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        },
      });
    });
  });

  // show img of record
  $(document).ready(function () {
    $(".btn-show-details-xray-img").click(function () {
      var m_rec_id = $(this).data("m_rec_id");
      var img_before = $(this).data("img_before");
      var img_last = $(this).data("img_last");
      var medical_predict = $(this).data("medical_predict");

      console.log(img_before);
      console.log(img_last);
      console.log(medical_predict);
      console.log($(".img-left"));

      $("#img-left").attr("src", img_before);
      $("#img-right").attr("src", img_last);
      $("#medical_predict").val(medical_predict);
    });
  });

  // edit
  $(document).ready(function () {
    $(".btn-show-details").on("click", function () {
      var patient_id = $(this).data("patient_id");
      var name = $(this).data("name");
      var age = $(this).data("age");
      var img = $(this).data("img");
      var phone = $(this).data("phone");
      var PID = $(this).data("pid");
      var gender = $(this).data("gender");
      var address = $(this).data("address");
      var date_created = $(this).data("date_created");
      var dob = $(this).data("dob");
      var email = $(this).data("email");

      $("#patient_id").attr("value", patient_id);
      $("#full_name_edit").attr("value", name);
      $("#age_edit").attr("value", age);
      $("#phone_edit").val(phone);
      $("#PID_edit").attr("value", PID);
      $("#gender_edit").val(gender);
      $("#address_edit").attr("value", address);
      $("#dob_edit").val(dob);
      $("#email_edit").attr("value", email);
      $("#date_created_edit").attr("value", date_created);
      // $("#img_edit").attr("value", img_profile);
    });
  });

  $(document).ready(function () {
    $("#btn_edit").click(function () {
      let patient_id = $("#patient_id").val();
      let name_edit = $("#full_name_edit").val();
      let age_edit = $("#age_edit").val();
      let phone_edit = $("#phone_edit").val();
      let PID_edit = $("#PID_edit").val();
      let gender_edit = $("#gender_edit").val();
      let address_edit = $("#address_edit").val();
      let dob_edit = $("#dob_edit").val();
      let email_edit = $("#email_edit").val();
      let date_created = $("#date_created_edit").val();

      $.ajax({
        url: "/patient/edit",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          patient_id: patient_id,
          name_edit: name_edit,
          age_edit: age_edit,
          phone_edit: phone_edit,
          PID_edit: PID_edit,
          gender_edit: gender_edit,
          address_edit: address_edit,
          dob_edit: dob_edit,
          email_edit: email_edit,
          date_created: date_created,
        }),
        success: function (response) {
          $("#error_editing_user").html(response);
          $("#error_editing_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        },
      });
    });
  });
}

function handleUploadImg() {
  const fileInput = document.getElementById("upload");
  const img = document.getElementById("xray-img--output");
  const editImg = document.getElementById("img_link_download");
  const canvas = document.getElementById("canvas");
  img.style.display = "block";
  editImg.style.display = "none";
  canvas.style.display = "none";

  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      const imgDataUrl = e.target.result;

      // Tạo một hình ảnh mới
      const image = new Image();

      // Khi hình ảnh đã được tải lên
      image.onload = function () {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");

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
        const resizedImgDataUrl = canvas.toDataURL("image/jpeg");

        // Hiển thị hình ảnh đã thay đổi kích thước
        img.src = resizedImgDataUrl;
      };

      // Đặt nguồn hình ảnh cho hình ảnh mới
      image.src = imgDataUrl;
    };

    reader.readAsDataURL(file);
  }
}

function handleUploadImgInAjaxBody() {
  // console.log('hi world');
  const fileInput = document.getElementById("upload-body");
  const img = document.getElementById("xray-img--show-body");

  // console.log(fileInput);
  // console.log(img)
  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      img.src = e.target.result;
    };

    reader.readAsDataURL(file);
  }
}

function handleUploadImgInProfile() {
  const fileInput = document.getElementById("fileInput");
  const img = document.getElementById("profile-img");

  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      img.src = e.target.result;
    };

    reader.readAsDataURL(file);
  }
}

function handleUploadImgRatio(fileInputId, imgId){
  const fileInput = document.getElementById(fileInputId);
  const img = document.getElementById(imgId);

  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      img.src = e.target.result;
    };

    reader.readAsDataURL(file);
    if(fileInputId === 'upload-contours'){
        document.getElementById('xray-img-contours').style = 'margin-right: 0 !important;';
    }

  }
}

function jsInUserProfile() {
  // change personal information
  $(document).ready(function () {
    $("#btn_submit_personal").click(function () {
      // console.log('hi world');
      $("#overlay").removeClass("d-none");
      var fullname = $("#fullname").val();
      var email = $("#email").val();
      var phone = $("#phone").val();
      var gender = $("#gender").val();
      var dob = $("#dob").val();

      var tmp_email = $("#tmp_email").val();
      var user_id = $("#user_id").val();
      var acc_id = $("#acc_id").val();
      var img = document.getElementById("fileInput");

      var formData = new FormData();
      formData.append("fullname", fullname);
      formData.append("email", email);
      formData.append("phone", phone);
      formData.append("gender", gender);
      formData.append("dob", dob);
      formData.append("tmp_email", tmp_email);
      formData.append("user_id", user_id);
      formData.append("acc_id", acc_id);
      formData.append("img", img.files[0]);

      $.ajax({
        url: "/user/profile/edit_personal_information",
        type: "POST",
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
          $("#error_editing_user").html(response);
          $("#error_editing_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        },
        complete: function () {
          $("#overlay").addClass("d-none");
        },
      });
    });
  });

  // change pwd
  $(document).ready(function () {
    $("#btn_submit_change_pwd").click(function () {
      var currentPwd = $('#current_pwd').val();
      var newPwd = $('#new_pwd').val();
      var verifyPwd = $('#verify_pwd').val();

      var formData = new FormData();
      formData.append('currentPwd', currentPwd);
      formData.append('newPwd', newPwd);
      formData.append('verifyPwd', verifyPwd);

      $.ajax({
        url: "/user/profile/change_pwd",
        type: "POST",
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
          $("#error_change_pwd_user").html(response);
          $("#error_change_pwd_user_outer").removeClass("d-none");
        },
        error: function (error) {
          console.log(error);
        },
        complete: function () {
          $("#overlay").addClass("d-none");
        },
      })
    })
  });
}

function getCookie(cookieName) {
  var name = cookieName + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookieArray = decodedCookie.split(";");
  for (var i = 0; i < cookieArray.length; i++) {
    var cookie = cookieArray[i];
    while (cookie.charAt(0) == " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) == 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
}

function getUserInformationForHeader() {
  fetch("/user/get_user_info")
    .then((response) => response.json())
    .then((data) => {
      var userName = data.user_name;
      var userImg = data.user_img;
      var roleId = data.role_id;
      $("#navbar_username").text(userName);
      $("#dashboard-username").text(userName);
      $("#navbar_user_img").attr("src", userImg);
      $("#dashboard_userimg").attr("src", userImg);
      console.log(roleId);
      if (roleId == 'ROL0000002') {
        $("#side-bar__account").addClass("d-none");
        $("#side-bar__user").addClass("d-none");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function jsInHome() {
  // show medical record in details by PID
  $(document).ready(function () {
    $(".btn-show-details-medical-record").click(function () {
      var Pid = $("#pid").val();
      console.log(Pid);
      if (Pid != undefined || Pid != '') {
        $.ajax({
          url: "/home/medical_record",
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify({
            Pid: Pid,
          }),
          success: function (response) {
            $("#more-patient-medical-record").html(response);
            // $("#error_editing_user_outer").removeClass("d-none");
          },
          error: function (error) {
            console.log(error);
          },
        });
      }
    });

  });

  // show img of record
  $(document).ready(function () {
    $(".btn-show-details-xray-img").click(function () {
      var m_rec_id = $(this).data("m_rec_id");
      var img_before = $(this).data("img_before");
      var img_last = $(this).data("img_last");
      var medical_predict = $(this).data("medical_predict");

      console.log(img_before);
      console.log(img_last);
      console.log(medical_predict);
      console.log($(".img-left"));

      $("#img-left").attr("src", img_before);
      $("#img-right").attr("src", img_last);
      $("#medical_predict").val(medical_predict);
    });
  });
}
