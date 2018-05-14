function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);       // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));    // Only send token to relative/local URLs
        }
    }
});

function cleanInput(dirtytext) {
    return dirtytext.replace(/[　｡。、､？?！!「」｢｣'"`,.\s]/g, "");
}

$(function() {
    $('#bug-button').click(function() {
        $('#form-modal-body').load('/news/newissue/', function () {
            modal.style.display = "block";
            formAjaxSubmit('#form-modal-body form', '#form-modal');
        });
    });
});