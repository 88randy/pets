jQuery(document).ready(function () {
    ImgUpload();

    $('.alert .close').on('click', function(e) {
        $(this).parent().hide();
    });

});

function ImgUpload() {
    var imgWrap = "";
    var imgArray = [];

    $(".upload__inputfile").each(function () {
        $(this).on("change", function (e) {
            imgWrap = $(this).closest(".upload__box").find(".upload__img-wrap");
            var maxLength = $(this).attr("data-max_length");
            var files = e.target.files;
            var filesArr = Array.prototype.slice.call(files);
            var iterator = 0;

            filesArr.forEach(function (f, index) {

                // Valida que sea una imagen que no se encuentra en el array
                for (var i = 0; i < imgArray.length; i++) {
                    if (f.name == imgArray[i].name){
                        var imgFormatError = '<div class="alert alert-warning alert-dismissible fade show" role="alert">'
                                +`<strong>Atención!</strong> La imagen seleccionada ya se encuentra en el listado`
                                +'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
                                +'</div>';
                        imgWrap.append(imgFormatError);
                        $('#image-format-error').show();
                        return;
                    }
                }
                
                // Valida que la imagen tenga un formato ".jpg, .jpng y .png"
                var ext = f.name.split('.').pop().toLowerCase();
                if($.inArray(ext, ['jpg','jpeg','png']) == -1) {
                    var imgFormatError = '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
                                        +'<strong>Error!</strong> El formato de la imagen: ' 
                                        + '<b>' + f.name + '</b>'
                                        +' no es válido. Solo se permiten formatos jpg, jpeg y png.'
                                        +'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
                                        +'</div>';
                    imgWrap.append(imgFormatError);
                    $('#image-format-error').show();
                    return;
                }

                // Valida que la imagen sea menor a 2 Mb
                if (f.size > 2 * 1024 * 1024) {
                    var imgSizeError = '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
                        +'<strong>Error!</strong> El tamaño de la imagen: ' 
                        + '<b>' + f.name + '</b>'
                        +' supera el límite permitido de 2MB.'
                        +'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
                        +'</div>';
                    imgWrap.append(imgSizeError);
                    $('#image-size-error').show();
                    return;
                }

                // Valida que la cantidad de imagenes sea menor o igual a 5
                if (imgArray.length > maxLength - 1) {
                    var imgLimitExceeded = '<div class="alert alert-warning alert-dismissible fade show" role="alert">'
                        +`<strong>Atención!</strong> Haz alcanzado el límite de <b>${maxLength}</b> imágenes que puedes subir.`
                        +'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
                        +'</div>';
                    imgWrap.append(imgLimitExceeded);
                    $('#image-size-error').show();
                    return false;
                } else {
                    var len = 0;
                    for (var i = 0; i < imgArray.length; i++) {
                        if (imgArray[i] !== undefined) {
                            len++;
                        }
                    }
                    if (len > maxLength) {
                        return false;
                    } else {
                        //imgArray = imgArray.concat(Array.prototype.slice.call(files));
                        imgArray.push(f);
                        var reader = new FileReader();
                        reader.onload = function (e) {
                            var html =
                                "<div class='upload__img-box'><div style='background-image: url(" 
                                + e.target.result 
                                + ")' data-number='" 
                                + $(".upload__img-close").length +
                                "' data-file='" +
                                f.name +
                                "' class='img-bg'><div class='upload__img-close'></div></div></div>";
                            imgWrap.append(html);
                            iterator++;
                        };
                        reader.readAsDataURL(f);
                        const dataTransfer = new DataTransfer();
                        imgArray.forEach(file => dataTransfer.items.add(file));
                        document.querySelector('input[name="images"]').files = dataTransfer.files;
                    }
                }
            });
        });
    });

    $("body").on("click", ".upload__img-close", function (e) {
        var file = $(this).parent().data("file");
        for (var i = 0; i < imgArray.length; i++) {
            if (imgArray[i].name === file) {
                imgArray.splice(i, 1);
                break;
            }
        }
        $(this).parent().parent().remove();
        const dataTransfer = new DataTransfer();
        imgArray.forEach(file => dataTransfer.items.add(file));
        document.querySelector('input[name="images"]').files = dataTransfer.files;
    });
}