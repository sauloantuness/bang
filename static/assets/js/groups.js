$('#group-confirmation-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var groupName = button.data('groupName') ;
    var groupId = button.data('groupId') ;
    var modal = $(this);

    modal.find('.modal-title').text(groupName);
    modal.find('.modal-body [name=group_id]').val(groupId);
    modal.find('[name=secret_key]').focus();
})

$('#group-confirmation-modal [name=secret_key]').on('keyup', function (event) {
    $('#group-confirmation-modal form .form-group:first').removeClass('has-error');

    if(event.target.value.length > 0)
        $('#group-confirmation-modal button').prop('disabled', false);
    else
        $('#group-confirmation-modal button').prop('disabled', true);
})

$('#group-confirmation-modal form').on('submit', function (event) {
    var csrf_token = $('[name=csrfmiddlewaretoken]').val()
    var secret_key = $('[name=secret_key]').val()
    var group_id = $('[name=group_id]').val()

    $.ajax({
        url: '/api/confirm_secret_key/',
        method: 'post',
        data: {
            group_id: group_id,
            secret_key: secret_key,
            csrfmiddlewaretoken: csrf_token
        },

        success: function(response) {
            if (response.success) {
                window.location.replace("/");
            }
            else {
                $('#group-confirmation-modal form .form-group:first').addClass('has-error');
            }
        }
    })

    return false;
})