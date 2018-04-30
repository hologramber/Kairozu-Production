var vlevel = 3;
var vocabcode = 'A';
var input = document.getElementById('id_vocabattempt');
wanakana.bind(input);

function vocabNext(data) {
    if (data['id'] != null) {
        $('#literal_one').html('&nbsp;' + data['vocab']['note'] + '&nbsp;');
        $('#vocab_english').html(data['vocab']['english']);
        $('#vocabquizform #vactual').val(data['vocab']['kana_clean']);
        $('#vocabquizform #vid').val(data['id']);
        switch(vlevel) {
            case 3:
                $('#hint_block').html('&nbsp;'); break;
            case 2:
                $('#hint_block').html(data['vocab']['kana_all_blank']); break;
            case 1:
                $('#hint_block').html(data['vocab']['kana_alt_blank']); break;
            default:
                $('#hint_block').html(data['vocab']['kana']); break;
        }
        $('#vocabquizform').removeClass('abox_g abox_r');
        if (data['vocab']['katakana'] == true) {
            $('#katakana-tips').show();
        } else {
            $('#katakana-tips').hide();
        }
    } else {
        $.get("{% url 'main:vocabsuccess' chapter.id %}").done(function (data) {
            $('#wrapper').html(data);
        });
    }
}
$('#vocabquizform').submit(function(event) {
    event.preventDefault();
    var clean_attempt = $('#id_vocabattempt').val().replace(/[　｡。、？！「」'",.?!\s]/g, "");
    if (clean_attempt == $('#vactual').val()) {
        $('#bug-button').hide();
        $('#vocabquizform').attr('class', 'abox abox_g');
        if (vlevel == 3) {
            vocabcode = 'C';
        } else {
            vlevel = 3;
            vocabcode = 'N';
        }
    } else {
        $('#bug-button').show();
        $('#vocabquizform').attr('class', 'abox_red abox_r');
        if (vlevel == 3) {
            vocabcode = 'I';
        } else {
            vocabcode = 'A';
        }
        if (vlevel > 0) { vlevel--; }
    }
    $('#vocabquizform #vcode').val(vocabcode);
    var form_data = $('#vocabquizform').serialize();
    $.post("{% url 'main:vocabcheck' chapter.id %}", form_data).done(function(data) {
        $('#vocabquizform')[0].reset();
        vocabNext(data);
    });
});

$(document).ready(function() {
    $.get("{% url 'main:vocabgrab' chapter.id %}").done(function (data) {
        vocabNext(data);
    });
});

$('#bug-button').click(function() {
    $('#form-modal-body').load('/news/newissue/', function () {
        modal.style.display = "block";
        formAjaxSubmit('#form-modal-body form', '#form-modal');
    });
});