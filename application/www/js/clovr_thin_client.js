$('.clovr-start').on('click', function() {
    BootstrapDialog.show({
        type: BootstrapDialog.TYPE_WARNING,
        title: 'WARNING: Regarding CloVR VM Termination',
        message: 'A CloVR VM launched using this application will continue to run until terminated by the user. Closing this application, shutting down or restarting the PC or closing the browser window WILL NOT terminate a CloVR VM. In order to do so please use the Manage VM\'s utility.',
        closable: false,
        buttons: [{
            id: 'btn-cancel',
            icon: 'glyphicon glyphicon-ban-circle',
            label: 'Cancel VM Launch',
            cssClass: 'btn-danger',
            action: function(dialogRef) {
                dialogRef.close();
            }

        },
        {
            id: 'btn-ok',
            icon: 'glyphicon glyphicon-check',
            label: 'Continue VM Launch',
            cssClass: 'btn-success',
        }]
    });
})

$(document).on('change', '.btn-file :file', function() {
  var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
  input.trigger('fileselect', [numFiles, label]);
});

$('.toggle').click(function(event) {
    event.preventDefault();
    var target = $(this).attr('href');
    $(target).toggleClass('hidden show');
});

$(document).ready( function() {
    $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
        
        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;
        
        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }
        
    });

    $('#vm_monitor').DataTable({
        ordering: false,
        lengthChange: false,
    });
});

