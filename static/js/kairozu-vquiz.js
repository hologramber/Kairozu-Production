var vlevel = 3,
    vocabcode = 'A',
    $hint_block = $('#hint_block'),
    $vocabquizform = $('#vocabquizform');

function vocabNext(data) {
    if (data['id'] != null) {
        $('#literal_one').html('&#8203;' + data['vocab']['note'] + '&#8203;');
        $('#vocab_english').html(data['vocab']['english']);
        $('#vactual').val(data['vocab']['kana_clean']);
        $('#vid').val(data['id']);
        $("#reflink").attr("href", '/main/chapter/' + data['vocab']['chapter'] + '/vocablist/');
        switch(vlevel) {
            case 3:
                $hint_block.html('&#8203;'); break;
            case 2:
                $hint_block.html(data['vocab']['kana_all_blank']); break;
            case 1:
                $hint_block.html(data['vocab']['kana_alt_blank']); break;
            default:
                $hint_block.html(data['vocab']['f_kana']); break;
        }
        $vocabquizform.removeClass('abox_g abox_r');
        if (data['vocab']['katakana']) {
            $('#katakana-tips').show();
        } else {
            $('#katakana-tips').hide();
        }
    } else {
        $.get(successurl).done(function (data) {
            $(successwrap).html(data);
        });
    }
}
$vocabquizform.submit(function(event) {
    event.preventDefault();
    var clean_attempt = cleanInput($('#id_vocabattempt').val());
    if (clean_attempt == $('#vactual').val()) {
        $vocabquizform.attr('class', 'abox abox_g');
        $('#bug-button').hide();
        if (vlevel == 3) {
            vocabcode = 'C';
        } else {
            vlevel = 3;
            vocabcode = 'N';
        }
    } else {
        $vocabquizform.attr('class', 'abox_red abox_r');
        $('#bug-button').show();
        if (vlevel == 3) { vocabcode = 'I'; } else { vocabcode = 'A'; }
        if (vlevel > 0) { vlevel--; }
    }
    $('#vcode').val(vocabcode);
    var form_data = $vocabquizform.serialize();
    $.post(checkurl, form_data).done(function(data) {
        $vocabquizform[0].reset();
        vocabNext(data);
    });
});