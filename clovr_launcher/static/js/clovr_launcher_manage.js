$(document).ready( function() {
    // Initialize our table of VM's.
    var vmTable = $('#vm_monitor').DataTable({
        ajax: {
            'url': '/api/instances/',
            'dataSrc': 'instances'
        },
        columns: [
            {'data': 'id'},
            {'data': 'name'},
            {'data': 'instance_type'},
            {'data': 'state'},
            {'data': 'start_time'},
            {'defaultContent': ''}
        ]
    });

    setInterval(function() {
        vmTable.ajax.reload();
    }, 120000);
});

