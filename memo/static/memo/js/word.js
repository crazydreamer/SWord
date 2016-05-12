'use strict';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});
$("#submit").click(function () {
	var content = $("textarea[name=content]").val();
  var word_id = $("div[word-id]").attr("word-id");
  $.post("/api/v1/word/"+word_id+"/note", {
    content: content
  }, function (data, status) {
      if (data.success) {
        var note = data.note;
        $("#notes").prepend('<div class="ui segment">'+note.content+" by "+note.user+"</div>");
      }
  });
});
