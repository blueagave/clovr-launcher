$('.clovr-start').on('click', function() {
	$('#start-error').hide();
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
            action: function(dialog) {
                dialog.close();
            }
        },
        {
            id: 'btn-ok',
            icon: 'glyphicon glyphicon-check',
            label: 'Continue VM Launch',
            cssClass: 'btn-success',
            action: function(dialog) {
                dialog.enableButtons(false);

                // Get a couple of the parameters we need
				var csrftoken = $('meta[name=csrf-token]').attr('content')

				$.ajaxSetup({
					beforeSend: function(xhr, settings) {
						if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
							xhr.setRequestHeader("X-CSRFToken", csrftoken)
						}
					}
				});

                $.ajax({
                    type: 'POST',
                    url: '/api/instances/',
                    data: $('#vm_start_form').serialize(),
                    success: function(data) {

                        // Can we re-jigger our existing dialog menu to show success?
                        dialog.getModalHeader().html('<div class="bootstrap-dialog-title">VM Started Successfully.</div>');
                        dialog.getModalBody().html('<div class="bootstrap-dialog-message">' +
                                                   'Your VM was started successfully and can be ' +
                                                   'identified with the instance ID ' + 
                                                   '<strong>' + data.instances[0] + '</strong>.' +
                                                   '<br /><br />Redirecting to VM monitor page in 3 seconds.</div>');

                        setTimeout(function() {
                            $(location).attr('href', "/vm/manage/");
                        }, 3000);
                    },
                    error: function(data) {
						$('#start-error .message').remove()
                        $('#start-error').append('<span class="message"><strong>An error occurred starting CloVR. Please try again later.</span>');
                        $('#start-error').show();
                        dialog.close();
                        $('#overlay').hide();
                    }
                });
            }
        }]
    });
});

$('.alert .close').on('click', function(e) {
    $(this).parent().hide();
});

$('.toggle').click(function(event) {
        event.preventDefault();
            var target = $(this).attr('href');
                $(target).toggleClass('hidden show');
});

$(document).ready( function() {
    // Fire of an AJAX request to grab our list of CloVR VM's from EC2. 
    // In the future I'll likely want to actually cache these results...
    $.ajax({
        type: 'GET',
        url: '/api/ami/',
        success: function(data) {
            $('#ami_select').find('option').remove().end();
            
            $.each(data.amis, function() {
                $('#ami_select').append($('<option />').val(this.id).text(this.name));
            });
        },
        error: function() {
            alert("LOL");
        }
    });
});

