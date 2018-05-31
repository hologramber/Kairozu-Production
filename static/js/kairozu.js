function cleanInput(text) {
    text = text.replace(/[　｡。、､？?！!「」｢｣'"`,.\s]/g, "");
    return text;
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
        e.stopPropagation();
    });

    $('.dropdown').click(function (e) {
        $(this).children('.dropdown-content').slideToggle();
        this.classList.toggle('active');
        $('.dropdown-content').not($(this).children()).hide();
        $('.dropdown').not($(this)).removeClass('active');
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
            $('#myTopnav').removeClass('responsive');
        }
        e.stopPropagation();
    });
});
