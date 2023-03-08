$(document).ready(function () {

    $("#show_hide_password1 button").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password1 input').attr("type") == "text"){
            $('#show_hide_password1 input').attr('type', 'password');
            $('#show_hide_password1 i').removeClass( "fa fa-sharp fa-solid fa-eye" );
            $('#show_hide_password1 i').addClass( "fa fa-solid fa-eye-slash" );
        }else if($('#show_hide_password1 input').attr("type") == "password"){
            $('#show_hide_password1 input').attr('type', 'text');
            $('#show_hide_password1 i').removeClass( "fa fa-solid fa-eye-slash" );
            $('#show_hide_password1 i').addClass( "fa fa-sharp fa-solid fa-eye" );
        }
    });
    $("#show_hide_password2 button").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password2 input').attr("type") == "text"){
            $('#show_hide_password2 input').attr('type', 'password');
            $('#show_hide_password2 i').removeClass( "fa fa-sharp fa-solid fa-eye" );
            $('#show_hide_password2 i').addClass( "fa fa-solid fa-eye-slash" );
        }else if($('#show_hide_password2 input').attr("type") == "password"){
            $('#show_hide_password2 input').attr('type', 'text');
            $('#show_hide_password2 i').removeClass( "fa fa-solid fa-eye-slash" );
            $('#show_hide_password2 i').addClass( "fa fa-sharp fa-solid fa-eye" );
        }
    });
});

const previewImage = (event) => {
    // Obtiene la imagen
    const imageFiles = event.target.files;
    // Cuenta el número de imagenes seleccionadas
    const imageFilesLength = imageFiles.length;
    // Si se selecciona al menos una imagen, proceda a mostrar la vista previa
    if (imageFilesLength > 0) {
        // Obtiene la ruta de la imagen
        const imageSrc = URL.createObjectURL(imageFiles[0]);
        // Seleccione el elemento de vista previa de la imagen
        const imagePreviewElement = document.querySelector("#preview-selected-image");
        // Asigna la ruta al elemento de vista previa de la imagen
        imagePreviewElement.src = imageSrc;
        // Muestra la imagen cambiando el valor de visualización a "block".
        imagePreviewElement.style.display = "block";
    }
};