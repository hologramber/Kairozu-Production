function cleanInput(dirtytext) {
    return dirtytext.replace(/[　｡。、､？?！!「」｢｣'"`,.\s]/g, "");
}

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

$(function() {
    $("#byealert").click(function() { $(this).parent().remove(); });
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    $('#nav-toggle').click(function(e) {
        $('#myTopnav').toggleClass("responsive");
        $('.dropdown-content').hide();
        $('.dropdown').removeClass('active');
        e.stopPropagation();
    });

    $('.dropdown').click(function(e) {
        $(this).children('.dropdown-content').slideToggle();
        this.classList.toggle('active');
        $('.dropdown-content').not($(this).children()).hide();
        $('.dropdown').not($(this)).removeClass('active');
        e.stopPropagation();
    });

    $('html').click(function(e) {
        if (e.target.id == 'form-modal') {
            e.target.style.display = "none";
        } else {
            $('.dropdown-content').hide();
            $('.dropdown').removeClass('active');
            $('#myTopnav').removeClass('responsive');
        }
        e.stopPropagation();
    });

    $('#bug-button').click(function() {
        $('#form-modal-body').load('/news/newissue/', function () {
            modal.style.display = "block";
            formAjaxSubmit('#form-modal-body form', '#form-modal');
        });
    });
});