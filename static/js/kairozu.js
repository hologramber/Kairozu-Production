function cleanInput(text) {
    text = text.replace(/[　｡。、､？?！!「」｢｣'"`,.\s]/g, "");
    return text;
}

function addTime(score) {
    // use addTime(0) to return current time
    var datenow = new Date(),
        // # score     0, 1, 2,  3,  4,  5,   6,   7,   8,   9,  10,   11,   12,   13,   14
        hours_scale = [0, 1, 7, 24, 48, 72, 120, 240, 336, 480, 984, 1680, 2328, 3000, 6000],
        addhours;
        if (score < 0) {
            addhours = 0;
        } else if (score > 14) {
            addhours = 12000;
        } else {
            addhours = hours_scale[score];
        }
    datenow.setHours(datenow.getHours()+addhours);
    return datenow.toJSON();
}

$(function() {
    $("#byealert").click(function () {
        $(this).parent().remove();
    });

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    $('#nav-toggle').click(function (e) {
        $('#myTopnav').toggleClass("responsive");
        $('.dropdown-content').hide();
        $('.dropdown').removeClass('active');
        $('.dropdown-sub-content').hide();
        $('.dropdown-sub').removeClass('active');
        e.stopPropagation();
    });

    $('.dropdown').click(function(e) {
        $(this).children('.dropdown-content').slideToggle();
        this.classList.toggle('active');
        $('.dropdown-content').not($(this).children()).hide();
        $('.dropdown').not($(this)).removeClass('active');
        $('.dropdown-sub-content').not($(this).children()).hide();
        $('.dropdown-sub').not($(this)).removeClass('active');
        e.stopPropagation();
    });

    $('.dropdown-sub').click(function(e) {
        $(this).children('.dropdown-sub-content').slideToggle();
        this.classList.toggle('active');
        $('.dropdown-sub-content').not($(this).children()).hide();
        $('.dropdown-sub').not($(this)).removeClass('active');
        e.stopPropagation();
    });

    $('#bug-button').click(function() {
        $('#form-modal-body').load('/news/newissue/', function () {
            modal.style.display = "block";
            formAjaxSubmit('#form-modal-body form', '#form-modal');
        });
    });

    $('html').click(function (e) {
        if (e.target.id == 'form-modal') {
            e.target.style.display = "none";
        } else {
            $('.dropdown-content').hide();
            $('.dropdown').removeClass('active');
            $('.dropdown-sub-content').hide();
            $('.dropdown-sub').removeClass('active');
            $('#myTopnav').removeClass('responsive');
        }
        e.stopPropagation();
    });
});
