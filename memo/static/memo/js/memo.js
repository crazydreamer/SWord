'use strict'

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
var client = new $.RestClient("/api/v1/");
client.add("memo_status");
client.add("memo_finish");

var app = new Vue({
  el: "#app",
  data: {
    status: 3,
    know: false,
    current_index: 0,
    words: [],
    start: false,
    finish: false
  },
  computed: {
    word_stat: function () {
      var nums = [0,0,0,0];
      var total = this.words.length;

      this.words.map(function (w) {
        nums[w.status] += 1;
      });
      var percent = nums.map(function (x) {
        return (x/total*100).toString()+"%";
      });
      return {
        total: total,
        progress: nums,
        percent: percent
      };
    },
    current_word: function () {
      return this.words[this.current_index];
    },
    finish: function () {
      return (this.word_stat.total == this.word_stat.progress[0])
    }
  },
  methods: {
    begin: function () {
      this.start = true;
      do {
        this.current_index = parseInt(Math.random()*this.words.length);
      } while(this.words[this.current_index].status == 0);
    },
    choose: function (ch) {
      if (ch) {
        if (this.status == 3) {
          this.know = true;
        }
        this.status = 0;
      }
      else {
        this.status -= 1;
      }
    },
    next: function () {
      var word = this.words[this.current_index]

      if (!this.know){
        word.status = 2;
      }
      else if (word.status == 2) {
        word.status = 1;
      }
      else {
        word.status = 0;
      }

      client.memo_status.update(word.learning_id, {
        status: word.status
      });

      this.status = 3;

      if (this.word_stat.progress[0] == this.word_stat.total)
      {
        this.current_index = 0;
        this.start = false;
        this.finish = true;
        return;
      }
      else {
        // 随机一个未掌握的词
        do {
          this.current_index = parseInt(Math.random()*this.words.length);
        } while(this.words[this.current_index].status == 0);
      }
      this.know = false;
    },
    do_finish: function () {
      var app = this;

      $.post("/api/v1/memo_finish", {}, function (data, status) {
        if (data.success) {
          app.finish = false;
          $.getJSON("/api/v1/memo_status", function(data, status) {
            app.words = data.words;
          })
        }
      });
    }
  },
  compiled: function () {
    var app = this;
    client.memo_status.read().done(function (data) {
      app.words = data.words;
    });
  }
});
