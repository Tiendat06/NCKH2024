
function collapsedSideBar(){
    document.getElementById('toggleButton').addEventListener('click', function() {
        const specificSidebar = document.getElementById('header-sidebar');
        const sidebar = document.getElementById('sidebar');
        const content = document.querySelector('.content');
        const header_content = document.getElementById('header-content');
        const sidebar_para = document.querySelectorAll('.main-sidebar__para');
        const sidebar_item = document.querySelectorAll('.main-sidebar__item');
        const header_title = document.querySelector('#header-navbar__title');
      
        for(let i = 0; i < sidebar_para.length; i++){
            if(sidebar_para[i].classList.contains('d-none') && sidebar_item[i].classList.contains('justify-content-center')){
                sidebar_para[i].classList.remove('d-none');
                sidebar_item[i].classList.remove('justify-content-center');

            }else{
                sidebar_para[i].classList.add('d-none');
                sidebar_item[i].classList.add('justify-content-center');
            }
        }

        console.log(header_title);

        sidebar.classList.toggle('collapsed');
        header_content.classList.toggle('collapsed');
        specificSidebar.classList.toggle('collapsed');
        content.classList.toggle('collapsed');
    });
      
}

function fullScreen(){
    const fullscreenButton = document.getElementById('navbar-bottom__icon--fullscreen');
    const content = document.querySelector('#body');

    fullscreenButton.addEventListener('click', () => {
    if (document.fullscreenElement) {
        exitFullscreen();
    } else {
        requestFullscreen();
    }
    });

    function requestFullscreen() {
        if (content.requestFullscreen) {
            content.requestFullscreen();
        } else if (content.mozRequestFullScreen) { /* Firefox */
            content.mozRequestFullScreen();
        } else if (content.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
            content.webkitRequestFullscreen();
        } else if (content.msRequestFullscreen) { /* IE/Edge */
            content.msRequestFullscreen();
        }
    }

    function exitFullscreen() {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { /* Firefox */
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { /* IE/Edge */
            document.msExitFullscreen();
        }
    }

}

function handleUploadImg() {
    const fileInput = document.getElementById('fileInput');
    const img = document.getElementById('xray-img');

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
    var imgElement = document.getElementById('xray-img--output');
    
    var a = document.createElement('a');
    a.href = imgElement.src;
    a.download = 'downloaded_image.jpg';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function ajaxInUserManagement(){
    // add
    $(document).ready(function() {
        $('#btn_add').click(function() {
            let name_add = $('#full_name_add').val();
            let gender_add = $('#gender_add').val();
            let email_add = $('#email_add').val();
            let dob_add = $('#dob_add').val();
            let phone_add = $('#phone_add').val();

            $.ajax({
                url: '/user/add',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(
                    {
                        name : name_add,
                        gender: gender_add,
                        email: email_add,
                        dob: dob_add,
                        phone: phone_add,
                    }
                ),
                success: function(response) {
                    $('#error_adding_user').html(response)
                    $('#error_adding_user_outer').removeClass('d-none')
                    //console.log(response);
                    //alert(response.message);
                },
                error: function(error) {
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
    
    $(document).ready(function() {
        $('#btn_edit').click(function() {
            let name_edit = $('#full_name_edit').val();
            let gender_edit = $('#gender_edit').val();
            let email_edit = $('#email_edit').val();
            let dob_edit = $('#dob_edit').val();
            let phone_edit = $('#phone_edit').val();
            
            // Truy cập trực tiếp đối tượng tệp từ đối tượng jQuery prop('files')
            // let avatar_edit = $('#avatar_edit').prop('files')[0];
    
            let tmp_email = $('#tmp_email').val();
            let user_id = $('#user_id').val();
            let acc_id = $('#acc_id').val();
            let img = $('#img_edit').val();
            
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
                url: '/user/edit',
                type: 'POST',
                // contentType: false,
                // processData: false,
                contentType: 'application/json',
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
                success: function(response) {
                    $('#error_editing_user').html(response)
                    $('#error_editing_user_outer').removeClass('d-none')
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });
    });
    

    $(document).ready(function() {
        $('.btn-show-details').on('click', function() {
            var name = $(this).data('name');
            var gender = $(this).data('gender')
            var email = $(this).data('email')
            var dob = $(this).data('dob')
            var phone = $(this).data('phone')
            var user_id = $(this).data('user_id')
            var acc_id = $(this).data('acc_id')
            var img_profile = $(this).data('img')

            // alert(userId)
            $('#full_name_edit').attr('value', name);
            $('#gender_edit').val(gender);
            $('#email_edit').attr('value', email);
            $('#dob_edit').val(dob);
            $('#phone_edit').val(phone);
            $('#tmp_email').attr('value', email);
            $('#user_id').attr('value', user_id);
            $('#acc_id').attr('value', acc_id);
            $('#img_edit').attr('value', img_profile);

        });
    });

    $(document).ready(function() {
        $('.btn-show-details-delete').on('click', function() {
            var id = $(this).data('id');
            var name = $(this).data('name');

            $('#userIdDelete').attr('value', id);
            $('#userNameDelete').attr('value', name);

            $('#userIdDelete-para').html('Are you sure to delete '+ name + ' ?');

        });
    });
}

function jsInXray(){

    $('#checking').click(function () {
        $('#form').submit();
    });

    $(document).ready(function() {
        $('#myRange').on('input', function() {
            var formData = new FormData();

            // var fileInput = document.getElementById('upload');
            // if (fileInput.files.length > 0) {
            //     var file = fileInput.files[0];
            //     console.log(file.name)
            //     formData.append('file', file);
            // }
            let img_link = $('#img_link_predict').val();
            let range = $('#myRange').val();
            $('#rangeValue').text(range);
            formData.append('img_link', img_link);
            formData.append('range', range);
            console.log(img_link)
            console.log(range)

            $.ajax({
                url: '/xray/ajax/changeRange',
                type: 'POST',

                processData: false,
                contentType: false,
                data: formData

            }).done((response)=>{
                $('#xray-general__predict').html(response)
                // success: function(response) {
                // },
                // error: function(error) {
                //     console.log(error);
                // }
            }).fail((error)=>{
                console.log(error)
            })


        });
    });

    // overlay
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('form');
        const overlay = document.getElementById('overlay');
        
      
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Ngăn chặn form submit mặc định
            //overlay.style.display = 'block'; // Hiển thị overlay
            $('#overlay').removeClass('d-none')

            setTimeout(function() {
                //overlay.style.display = 'none'; // Ẩn overlay
            $('#overlay').addClass('d-none')

                // Xử lý dữ liệu trả về từ form
            }, 100000);
        });
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
    // console.log(this)
    const fileInput = document.getElementById('upload');
    const img = document.getElementById('xray-img--output');
    console.log(img)
    console.log(fileInput)

    const file = fileInput.files[0];

    const file_path = fileInput.files[0].name;
    console.log(file_path)

    // for(let i = 0; i < img.length; i++){
        if (file) {
            const reader = new FileReader();
    
            reader.onload = function (e) {
                img.src = e.target.result;
                console.log(e.target.result);
                // console.log('hello')
            };
            reader.readAsDataURL(file);
        }
    // }

}


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