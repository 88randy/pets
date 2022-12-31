$(document).ready(function () {
    
    // Inicializar Filepond en el elemento con clase "filepond"
    FilePond.registerPlugin(
        FilePondPluginFileValidateType,
        FilePondPluginImageExifOrientation,
        FilePondPluginImagePreview,
        FilePondPluginImageCrop,
        FilePondPluginImageResize,
        FilePondPluginImageTransform,
        FilePondPluginImageEdit
    );

    // Select the file input and use 
    // create() to turn it into a pond
    const filePondElement = FilePond.create(
        document.querySelector('.filepond'),
        {
            labelIdle: `Arrastra y suelta tu imagen o <span class="filepond--label-action">Examinar</span>`,
            imagePreviewHeight: 170,
            imageCropAspectRatio: '1:1',
            imageResizeTargetWidth: 200,
            imageResizeTargetHeight: 200,
            stylePanelLayout: 'compact',
            styleLoadIndicatorPosition: 'center bottom',
            styleButtonRemoveItemPosition: 'center bottom',
        }
    );
    
    filePondElement.on('addfile', (event, file) => {
        FilePond.getFiles(filePondElement).then((files) => {
            // Asigna la lista de archivos al input de Django
            $('#id_profile_picture').prop('files', files);
        });
    });

    
    $("#show_hide_password1 a").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password1 input').attr("type") == "text"){
            $('#show_hide_password1 input').attr('type', 'password');
            $('#show_hide_password1 i').addClass( "bi bi-eye-slash" );
            $('#show_hide_password1 i').removeClass( "bi bi-eye" );
        }else if($('#show_hide_password1 input').attr("type") == "password"){
            $('#show_hide_password1 input').attr('type', 'text');
            $('#show_hide_password1 i').removeClass( "bi bi-eye-slash" );
            $('#show_hide_password1 i').addClass( "bi bi-eye" );
        }
    });
    $("#show_hide_password2 a").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password2 input').attr("type") == "text"){
            $('#show_hide_password2 input').attr('type', 'password');
            $('#show_hide_password2 i').addClass( "bi bi-eye-slash" );
            $('#show_hide_password2 i').removeClass( "bi bi-eye" );
        }else if($('#show_hide_password2 input').attr("type") == "password"){
            $('#show_hide_password2 input').attr('type', 'text');
            $('#show_hide_password2 i').removeClass( "bi bi-eye-slash" );
            $('#show_hide_password2 i').addClass( "bi bi-eye" );
        }
    });
});