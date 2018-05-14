$(function() {
    var dialogue_level = 3,
        dialogue_index = 0,
        response_index = 0,
        response_length = 0,
        total_inputs = 0,
        incorrect_inputs = 0,
        next_step = 1,
        newly_wrong = 0,
        current_dialogue = '',
        current_prompt = '',
        current_response = '',
        current_name = '';
    var $dialoguehint = $('#dialogue_hint');

    var newpromptline = '',
        newpromptline_a = "<tr><td class='dialogue-green'><i class='fa fa-user fa-lg green-words' aria-hidden='true'></i> <span id='dialoguename",
        newpromptline_b = "' class='green-words bigbold'></span></td></tr><tr><td><div class='message'><div><p><span id='dialogueprompt",
        newpromptline_c = "'></div></p></span></div></td></tr>";

    var newresponseline = '',
        newresponseline_a ="<tr style='text-align:right;'><td class='dialogue-orange'><i class='fa fa-user fa-lg orange-words' aria-hidden='true'></i> <span class='orange-words bigbold'>You</span></td></tr><tr><td><div class='message me'><div><p><span id='responsekana",
        newresponseline_b = "' class='bold'></div></p></span></div></td></tr>";

    var newsecondaryline = '',
        newsecondaryline_a = "<tr><td><div class='message me'><div><p><span id='responsekana",
        newsecondaryline_b = "' class='bold'></div></p></span></div></td></tr>";

    function dialogueNext(data) {
        if (data['id'] != null) {
            if (response_index == 0 && next_step == 1) {
                newpromptline = newpromptline_a + dialogue_index + newpromptline_b + dialogue_index + newpromptline_c;
                newresponseline = newresponseline_a + dialogue_index + '-' + response_index + newresponseline_b;
                $('#dialogue-table').append(newpromptline, newresponseline);
            } else if (next_step == 1) {
                newsecondaryline = newsecondaryline_a + dialogue_index + '-' + response_index + newsecondaryline_b;
                $('#dialogue-table').append(newsecondaryline);
            }
            response_length = data['responses'].length-1;
            current_prompt = '#dialogueprompt' + dialogue_index;
            current_response = '#responsekana' + dialogue_index + '-' + response_index;
            current_name = '#dialoguename' + dialogue_index;
            $(current_name).html(data['prompt_name']);
            $(current_prompt).html(data['prompt_kana_f']);
            var topelement = document.getElementById("grammarholder");
            topelement.scrollIntoView();
            $('#dialogue_actual').val(data['responses'][response_index]['response_kana_clean']);
            $('#dialogue_kana').val(data['responses'][response_index]['response_kana_f']);
            $('#dialogue_english').html(data['responses'][response_index]['response_english']);
            if (data['responses'][response_index]['response_literal'].trim()) {
                $('#literal_one').html('<div class="white-words litcontextbox upper">literal</div>' + data['responses'][response_index]['response_literal'] + '&#8203;');
            } else {
                $('#literal_one').html('&#8203;');
            }
            $('#context_one').html(data['responses'][response_index]['response_context'] + '&#8203;');
            switch (dialogue_level) {
                case 3:
                    if (data['responses'][response_index]['response_disamb_location'] != 0) {
                        $dialoguehint.html(data['responses'][response_index]['response_kana_all_blank']);
                        $dialoguehint.addClass('ls5y');
                    } else {
                        $dialoguehint.html('&#8203;');
                    } break;
                case 2:
                    $dialoguehint.html(data['responses'][response_index]['response_kana_all_blank']);
                    $dialoguehint.removeClass('ls5y');
                    break;
                case 1:
                    $dialoguehint.html(data['responses'][response_index]['response_kana_alt_blank']); break;
                case 0:
                    $dialoguehint.html(data['responses'][response_index]['response_kana_f']); break;
                default:
                    $dialoguehint.html('&#8203;'); break;
            }
            $('#dialogue_form').removeClass('abox_g abox_r');
        } else {
            var dialogue_grade = (total_inputs-incorrect_inputs)/total_inputs;
            var total_dialogue = $('#dialogue-table').html();
            $.ajax({
                url: "{% url 'main:exercisedialoguegrade' chapter.id exercise.id %}",
                data: { 'dialogue_grade' : dialogue_grade }, type: "POST",
                success: function (data) {
                    $('#wrapper').html(data);
                    $('#dialogue-table').html(total_dialogue);
                }
            })
        }
    }

    $('#dialogue_form').submit(function(event) {
        event.preventDefault();
        var clean_attempt = cleanInput($('#id_dialogue_attempt').val());
        if (clean_attempt == $('#dialogue_actual').val()) {
            $('#dialogue_form').attr('class', 'abox abox_g');
            $('#bug-button').hide();
            $('#dialogue_english').attr('class', 'challenge-grammar');
            if (dialogue_level == 3) {
                total_inputs++;
                next_step = 1;
                newly_wrong = 0;
                current_dialogue = $('#dialogue_kana').val();
                $(current_response).html(current_dialogue);
                if (response_index == response_length) {
                    dialogue_index++;
                    response_index = 0;
                    current_dialogue = '';
                } else {
                    response_index++;
                }
            } else {
                if (newly_wrong == 0) { incorrect_inputs++; }
                newly_wrong = 1;
                next_step = 0;
                dialogue_level = 3;
            }
        } else {
            $('#bug-button').show();
            $('#dialogue_form').attr('class', 'abox_red abox_r');
            $('#dialogue_english').attr('class', 'challenge-grammar red-words');
            if (dialogue_level > 0) {
                next_step = 0;
                dialogue_level--;
            }
        }

        $('#dialogue_index').val(dialogue_index);
        var form_data = $('#dialogue_form').serialize();
        $.post("{% url 'main:exercisedialoguecheck' chapter.id exercise.id %}", form_data).done(function(data) {
            $('#dialogue_form')[0].reset();
            dialogueNext(data);
        })
    });
});