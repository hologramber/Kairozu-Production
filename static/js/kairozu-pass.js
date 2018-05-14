$(function() {
    var passage_level = 3,
        passage_index = 0,
        current_passage = '',
        currentline = '',
        totalinputs = 0,
        incorrectinputs = 0,
        nextstep = 1,
        newlywrong = 0;
    var $passagehint = $('#passage_hint');

    function passageNext(data) {
        if (data['id'] != null) {
            $('#passage_eng').html(data['english']);
            $('#passageactual').val(data['kana_clean']);
            $('#passagekana').val(data['f_kana']);
            if (data['literal'].trim()) {
                $('#literal_one').html('<div class="white-words litcontextbox upper">literal</div>' + data['literal'] + '&#8203;');
            } else {
                $('#literal_one').html('&#8203;');
            }
            $('#context_one').html(data['context'] + '&#8203;');
            $('#passage_jp').html(current_passage);
            switch (passage_level) {
                case 3:
                    if (data['disamb_location'] != 0) {
                        $passagehint.html(data['kana_all_blank']);
                        $passagehint.addClass('ls5y');
                    } else {
                        $passagehint.html('&#8203;');
                    } break;
                case 2:
                    $passagehint.html(data['kana_all_blank']);
                    $passagehint.removeClass('ls5y');
                    break;
                case 1:
                    $passagehint.html(data['kana_alt_blank']); break;
                default:
                    $passagehint.html(data['f_kana']); break;
            }
            currentline = '#sentence' + data['id'];
            $(currentline).attr('class', 'green-words-bold');
            $('#passageform').removeClass('abox_g abox_r');
        } else {
            var passage_grade = (totalinputs-incorrectinputs)/totalinputs;
            var total_passage = $('#retain-passage').html();
            $.ajax({
                url: "{% url 'main:exercisepassagegrade' chapter.id exercise.id %}",
                data: { 'passage_grade' : passage_grade }, type: "POST",
                success: function (data) {
                    $('#wrapper').html(data);
                    $('#retain-passage').html(total_passage);
                }
            })
        }
    }

    $('#passageform').submit(function(event) {
        event.preventDefault();
        var clean_attempt = cleanInput($('#id_passageattempt').val());
        if (clean_attempt == $('#passageactual').val()) {
            $('#bug-button').hide();
            $('#passageform').attr('class', 'abox abox_g');
            $('#passage_eng').attr('class', 'challenge-grammar');
            if (passage_level == 3) {
                totalinputs++;
                nextstep = 1;
                newlywrong = 0;
                passage_index++;
                $(currentline).removeClass('green-words-bold');
                current_passage = current_passage + ' ' + $('#passagekana').val();
            } else {
                if (newlywrong == 0) { incorrectinputs++; }
                newlywrong = 1;
                nextstep = 0;
                passage_level = 3;
            }
        } else {
            $('#bug-button').show();
            $('#passageform').attr('class', 'abox_red abox_r');
            $('#passage_eng').attr('class', 'challenge-grammar red-words');
            if (passage_level > 0) { passage_level--; }
        }
        $('#passage_index').val(passage_index);
        var form_data = $('#passageform').serialize();
        $.post("{% url 'main:exercisepassagecheck' chapter.id exercise.id %}", form_data).done(function(data) {
            $('#passageform')[0].reset();
            passageNext(data);
        })
    });
});