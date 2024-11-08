$(document).ready(function() {
    $('#search-input').on('input', function() {
        var query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: '/search',
                type: 'GET',
                data: {'query': query},
                success: function(response) {
                    $('#search-results').html('');
                    $.each(response.results, function(index, result) {
                        $('#search-results').append('<div><p>' + result.title + '</p><img src="' + result.poster_path + '"></div>');
                    });
                }
            });
        } else {
            $('#search-results').html('');
        }
    })
})