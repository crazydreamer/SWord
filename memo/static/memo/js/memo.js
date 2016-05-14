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

// 进行 POST 等操作时头部加上 CSRFToken
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

// 设置 jQuery.rest client
var client = new $.RestClient("/api/v1/");
client.add("memo_status");
client.add("memo_finish");

var app = new Vue({
  el: "#app",
  data: {
    status: 3,          // 当前背单词状态
    know: false,        // 是否认识当前单词
    current_index: 0,   // 当前单词下标
    words: [],
    start: false,       // 开始状态
  },
  computed: {
    word_stat: function () {
      // 单词背诵情况统计
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
      // 当前单词
      return this.words[this.current_index];
    },
    finish: function () {
      // 完成状态
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
      }
      else {
        // 随机一个未掌握的词
        do {
          this.current_index = parseInt(Math.random()*this.words.length);
        } while(this.words[this.current_index].status == 0);
      }
      this.know = false;
    },
    do_finish: function (event) {
      var app = this;
      $(event.target).addClass("loading");

      $.post("/api/v1/memo_finish", {}, function (data, status) {
        if (data.success) {
          $.getJSON("/api/v1/memo_status", function(data, status) {
            app.words = data.words;
            app.finish = false;
            $(event.target).removeClass("loading");
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
