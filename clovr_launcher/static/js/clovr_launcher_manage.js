$('.alert .close').on('click', function(e) {
    $(this).parent().hide();
});

var infoDialog = new BootstrapDialog({
    type: BootstrapDialog.TYPE_WARNING,
    title: 'WARNING: Terminate CloVR VM',
    message: '',
    closable: false,
    buttons: [{
        id: 'btn-cancel',
        icon: 'glyphicon glypicon-ban-cicle',
        label: 'Cancel',
        cssClass: 'btn-danger',
        action: function(dialog) {
            dialog.close();
        }
    },
    {
        id: 'btn-ok',
        icon: 'glyphicon glyphicon-check',
        label: 'Terminate VM',
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
                type: 'DELETE',
                url: '/api/instances/' + infoDialog.getData('instance_id'),
                success: function(data) {
                    vmTable = infoDialog.getData('vmTable');
                    vmTable.ajax.reload();

                    $('#status-msg .message').remove()
                    $('#status-msg').append('<span class="message"><strong>CloVR VM <strong>' + 
                                            infoDialog.getData('instance_id') + 
                                            '</strong> was successfully terminated</span>');
                    $('#status-msg').show();
                    dialog.close();
                },
                error: function(data) {
                    $('#terminate-error .message').remove()
                    $('#terminate-error').append('<span class="message"><strong>An error occurred terminating the CloVR VM. Please try again later.</span>');
                    $('#terminate-error').show();
                    dialog.close();
                }
            });
        }
    }]
});


$(document).ready( function() {
    infoDialog.realize();

    // Initialize our table of VM's.
    var vmTable = $('#vm_monitor').DataTable({
        ajax: {
            'url': '/api/instances/',
            'dataSrc': 'instances'
        },
        searching: false,
        order: [[4, 'desc']],
        language: {
            emptyTable: 'No CloVR VM\'s are currently running.',
            zeroRecords: 'No CloVR VM\'s are currently running.',
            loadingRecords: 'Please wait - loading...'
        },
        columns: [
            {data: 'id', className: 'ami-id'},
            {data: 'name'},
            {data: 'instance_type'},
            {data: 'state'},
            {data: 'start_time'},
            {defaultContent: '', orderable: false, targets: 'no-sort'}
        ],
        createdRow: function(row, data, index) {
            $('td', row).eq(4).addClass('vm-time');
            $('td', row).eq(5).addClass('fa fa-times fa-icon-red');

            switch (data.state) {
                case "pending":
                case "shutting-down":
                    $('td', row).eq(3).addClass('state-pending');
                    $('td', row).eq(5).addClass('terminate-disable')
                    break;
                case "running":
                    $('td', row).eq(3).addClass('state-running');
                    $('td', row).eq(5).addClass('terminate-enable');
                    $('td', row).addClass('clicky');

                    for (var i = 0; i <= 4; i += 1) {
                        $('td', row).eq(i).on('click', function() {
                            window.open('http://' + data.address);
                        });
                    }

                    $('td', row).eq(5).on('click', function() {
                        // Terminate the selected VM, make sure to prompt a 
                        // warning when doing so.
                        infoDialog.setData('instance_id', data.id);
                        infoDialog.getModalBody().html('<div class="bootstrap-dialog-message">' +
                                                       'Are you sure you want to Terminate the follwing ' +
                                                       'VM: <strong>' + data.id + '</strong>');
                        infoDialog.open();
                    });

                    break;
                case "terminated": 
                    $('td', row).eq(3).addClass('state-terminated');
                    $('td', row).eq(5).addClass('terminate-disable');
                    break;
            }

        }
    });
    
    infoDialog.setData('vmTable', vmTable);

    setInterval(function() {
        vmTable.ajax.reload();
    }, 120000);


});

