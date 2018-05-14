function vocabNext(data, vtype) {
    var $hint_block = $('#hint_block');
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
        $('#vocabquizform').removeClass('abox_g abox_r');
        if (data['vocab']['katakana']) {
            $('#katakana-tips').show();
        } else {
            $('#katakana-tips').hide();
        }
    } else {
        if (vtype == 'vreview') {
            $.get("{% url 'main:reviewvocabcurrent' %}").done(function (data) {
                $('#allwrap').html(data);
            });
        } else if (vtype == 'vquiz') {
            $.get("{% url 'main:vocabsuccess' chapter.id %}").done(function (data) {
                $('#wrapper').html(data);
            });
        }
    }
}


function sentenceNext(data, stype) {
    var $sentencehint = $('#sentence_hint');
    if (data['id'] != null) {
        $('#sentence_eng').html(data['sentence']['english']);
        $('#sactual').val(data['sentence']['kana_clean']);
        $('#sstrict').val(data['sentence']['force_strict']);
        $('#sid').val(data['id']);
        if (data['sentence']['literal'].trim()) {
            $('#literal_one').html('<div class="white-words litcontextbox upper">literal</div>' + data['sentence']['literal'] + '&#8203;');
        } else {
            $('#literal_one').html('&#8203;');
        }
        $('#context_one').html(data['sentence']['context'] + '&#8203;');
        $("#reflink").attr("href", '/main/lesson/' + data['sentence']['lesson'] + '/');
        switch (slevel) {
            case 3:
                if (data['sentence']['disamb_location'] != 0) {
                    $sentencehint.html(data['sentence']['kana_all_blank']);
                    $sentencehint.addClass('ls5y');
                } else {
                    $sentencehint.html('&#8203;');
                } break;
            case 2:
                $sentencehint.html(data['sentence']['kana_all_blank']);
                $sentencehint.removeClass('ls5y');
                break;
            case 1:
                $sentencehint.html(data['sentence']['kana_alt_blank']); break;
            default:
                $sentencehint.html(data['sentence']['f_kana']); break;
        }
        $('#sentencequizform').removeClass('abox_g abox_r');
    } else {
        if (stype == 'sreview') {
            $.get("{% url 'main:reviewsentencecurrent' %}").done(function (data) {
                $('#allwrap').html(data);
            });
        } else if (stype == 'squiz') {
            $.get("{% url 'main:sentencesuccess' lesson.id %}").done(function (data) {
                $('#wrapper').html(data);
            });
        }
    }
}


function practiceNext(data) {
    var $hint_one = $('#hint_one'),
        $hint_two = $('#hint_two');
    if (data['pone_english'] != null) {
        $('#practice_eng_one').html(data['pone_english']);
        $('#practice_eng_two').html(data['ptwo_english']);
        $('#pstrict').val(data['force_strict']);
        $('#poneact').val(data['pone_kana_clean']);
        $('#ptwoact').val(data['ptwo_kana_clean']);
        switch(pcode) {
            case 'BC':
                $hint_one.html(data['pone_kana_all'] + '&#8203;');
                $hint_two.html(data['ptwo_kana_all'] + '&#8203;');
                break;
            case 'OC':
                if (plevel == 1) {
                    $hint_one.html(data['pone_kana_f'] + '&#8203;');
                    $hint_two.html(data['ptwo_kana_alt'] + '&#8203;');
                } else {
                    $hint_one.html(data['pone_kana_f'] + '&#8203;');
                    $hint_two.html(data['ptwo_kana_f'] + '&#8203;');
                }
                break;
            case 'TC':
                if (plevel == 1) {
                    $hint_one.html(data['pone_kana_alt'] + '&#8203;');
                    $hint_two.html(data['ptwo_kana_f'] + '&#8203;');
                } else {
                    $hint_one.html(data['pone_kana_f'] + '&#8203;');
                    $hint_two.html(data['ptwo_kana_f'] + '&#8203;');
                }
                break;
            default:
                if (plevel == 1) {
                    $hint_one.html(data['pone_kana_alt'] + '&#8203;');
                    $hint_two.html(data['ptwo_kana_alt'] + '&#8203;');
                } else {
                    $hint_one.html(data['pone_kana_f'] + '&#8203;');
                    $hint_two.html(data['ptwo_kana_f'] + '&#8203;');
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
        $('#context_one').html(data['pone_context'] + '&#8203;');
        $('#context_two').html(data['ptwo_context'] + '&#8203;');
        $('#id_pone_attempt').removeClass('kbox1_g kbox1_r');
        $('#id_ptwo_attempt').removeClass('kbox2_g kbox2_r');
        $('#ksubmit').removeClass('ksub_r ksub_g');
    } else {
        $.get("{% url 'main:practicesuccess' lesson.id %}").done(function (data) {
            $('#wrapper').html(data);
        });
    }
}


function expressionNext(data, etype) {
    if (data['id'] != null) {
        $('#literal_note').html('&#8203;' + data['express']['note'] + '&#8203;');
        $('#expression_english').html(data['express']['english']);
        $('#eactual').val(data['express']['kana_clean']);
        $('#eid').val(data['id']);
        if (data['express']['literal'].trim()) {
            $('#literal_one').html('<div class="white-words litcontextbox upper">literal</div>' + data['express']['literal'] + '&#8203;');
        } else {
            $('#literal_one').html('&#8203;');
        }
        $("#reflink").attr("href", '/main/chapter/' + data['express']['chapter'] + '/expressionlist/');
        switch(elevel) {
            case 2:
                $hint_block.html(data['express']['kana_all_blank']); break;
            case 1:
                $hint_block.html(data['express']['kana_alt_blank']); break;
            default:
                $hint_block.html(data['express']['f_kana']); break;
        }
        $('#expressionquizform').removeClass('abox_g abox_r');
        if (data['express']['katakana']) {
            $('#katakana-tips').show();
        } else {
            $('#katakana-tips').hide();
        }
        if (data['express']['prompt']) {
            $('#expression-example').show();
            $('#prompt-text').html('Example: ' + data['express']['prompt']);
        } else {
            $('#expression-example').hide();
        }
    } else {
        if (etype == 'ereview') {
            $.get("{% url 'main:reviewexpressioncurrent' %}").done(function (data) {
                $('#allwrap').html(data);
            });
        } else if (etype == 'equiz') {
            $.get("{% url 'main:expressionsuccess' chapter.id %}").done(function (data) {
                $('#wrapper').html(data);
            });
        }
    }
}