$(function(){
    $('#buy-form').submit(function(e){
        e.preventDefault();
        $.ajax({
            method:'GET',
            url: $(this).attr('action'),
            dataType: 'json',
            data: {
                'count': $('#id_count').val(),
                'product_slug': $('#submit_button').attr('data-product'),
            },
            success: function(data){
                console.log('OK')
            }
        })
    })

});