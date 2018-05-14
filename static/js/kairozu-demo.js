function vocabNextDemo(data) {
    if (data['id'] != null) {
        $('#vocab_english').html(data['english']);
        $('#vactual').val(data['kana_clean']);
        switch(vlevel) {
            case 3:
                $('#hint_block').html('&#8203;'); break;
            case 2:
                $('#hint_block').html(data['kana_all_blank']); break;
            case 1:
                $('#hint_block').html(data['kana_alt_blank']); break;
            default:
                $('#hint_block').html(data['f_kana']); break;
        }
        $('#vocabquizform').removeClass('abox_g abox_r');
    } else {
        $.get("{% url 'demo:demovocabsuccess' %}").done(function (data) {
            $('#wrapper').html(data);
        });
    }
}

function sentenceNextDemo(data) {
    if (data['id'] != null) {
        $('#sentence_eng').html(data['english']);
        $('#sactual').val(data['kana_clean']);
        if (data['literal'].trim()) {
            $('#literal_one').html('<div class="white-words litcontextbox upper">literal</div>' + data['literal'] + '&#8203;');
        } else {
            $('#literal_one').html('&#8203;');
        }
        switch (slevel) {
            case 3:
                $('#sentence_hint').html('&#8203;'); break;
            case 2:
                $('#sentence_hint').html(data['kana_all_blank']); break;
            case 1:
                $('#sentence_hint').html(data['kana_alt_blank']); break;
            default:
                $('#sentence_hint').html(data['f_kana']); break;
        }
        $('#sentencequizform').removeClass('abox_g abox_r');
    } else {
        $.get("{% url 'demo:demosentencesuccess' %}").done(function (data) {
            $('#wrapper').html(data);
        });
    }
}

function practiceNextDemo(data) {
    if (data['pone_english'] != null) {
        $('#practice_eng_one').html(data['pone_english']);
        $('#practice_eng_two').html(data['ptwo_english']);
        $('#poneact').val(data['pone_kana_clean']);
        $('#ptwoact').val(data['ptwo_kana_clean']);
        switch(pcode) {
            case 'BC':
                $('#hint_one').html(data['pone_kana_all'] + '&#8203;');
                $('#hint_two').html(data['ptwo_kana_all'] + '&#8203;');
                break;
            case 'OC':
                if (plevel == 1) {
                    $('#hint_one').html(data['pone_kana_f'] + '&#8203;');
                    $('#hint_two').html(data['ptwo_kana_alt'] + '&#8203;');
                } else {
                    $('#hint_one').html(data['pone_kana_f'] + '&#8203;');
                    $('#hint_two').html(data['ptwo_kana_f'] + '&#8203;');
                }
                break;
            case 'TC':
                if (plevel == 1) {
                    $('#hint_one').html(data['pone_kana_alt'] + '&#8203;');
                    $('#hint_two').html(data['ptwo_kana_f'] + '&#8203;');
                } else {
                    $('#hint_one').html(data['pone_kana_f'] + '&#8203;');
                    $('#hint_two').html(data['ptwo_kana_f'] + '&#8203;');
                }
                break;
            default:
                if (plevel == 1) {
                    $('#hint_one').html(data['pone_kana_alt'] + '&#8203;');
                    $('#hint_two').html(data['ptwo_kana_alt'] + '&#8203;');
                } else {
                    $('#hint_one').html(data['pone_kana_f'] + '&#8203;');
                    $('#hint_two').html(data['ptwo_kana_f'] + '&#8203;');
                }
                break;
        }
        if (data['pone_literal'].trim()) {
            $('#literal_one').html('<div class="white-words litcontextbox upper">literal</div>' + data['pone_literal'] + '&#8203;');
        } else {
            $('#literal_one').html('&#8203;');
        }
        if (data['ptwo_literal'].trim()) {
            $('#literal_two').html('<div class="white-words litcontextbox upper">literal</div>' + data['ptwo_literal'] + '&#8203;');
        } else {
            $('#literal_two').html('&#8203;');
        }
        $('#id_pone_attempt').removeClass('kbox1_g kbox1_r');
        $('#id_ptwo_attempt').removeClass('kbox2_g kbox2_r');
        $('#ksubmit').removeClass('ksub_r ksub_g');
    } else {
        $.get("{% url 'demo:demopracticesuccess' %}").done(function (data) {
            $('#wrapper').html(data);
        });
    }
}

function expressionNextDemo(data) {
    if (data['id'] != null) {
        $('#vocab_english').html(data['english']);
        $('#vactual').val(data['kana_clean']);
        switch(vlevel) {
            case 2:
                $('#hint_block').html(data['kana_all_blank']); break;
            case 1:
                $('#hint_block').html(data['kana_alt_blank']); break;
            default:
                $('#hint_block').html(data['f_kana']); break;
        }
        $('#vocabquizform').removeClass('abox_g abox_r');
    } else {
        $.get("{% url 'demo:demoexpressionsuccess' %}").done(function (data) {
            $('#wrapper').html(data);
        });
    }
}