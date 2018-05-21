var vlevel = 3,
    vindex = 0,
    $hint_block = $('#hint_block'),
    $vocabquizform = $('#vocabquizform');

function vocabNext(data) {
    if (data['id'] != null) {
        $('#vocab_english').html(data['english']);
        $('#vactual').val(data['kana_clean']);
        switch(vlevel) {
            case 3:
                $hint_block.html('&#8203;'); break;
            case 2:
                $hint_block.html(data['kana_all_blank']); break;
            case 1:
                $hint_block.html(data['kana_alt_blank']); break;
            default:
                $hint_block.html(data['f_kana']); break;
        }
        $vocabquizform.removeClass('abox_g abox_r');
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
        if (vlevel == 3) { vindex++; } else { vlevel = 3; }
    } else {
        $vocabquizform.attr('class', 'abox_red abox_r');
        if (vlevel > 0) { vlevel--; }
    }
    $('#vindex').val(vindex);
    var form_data = $vocabquizform.serialize();
    $.post(checkurl, form_data).done(function(data) {
        $vocabquizform[0].reset();
        vocabNext(data);
    });
});