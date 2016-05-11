'use strict'

function get_cookie(key) {
  var cs = document.cookie;
  var cookies = cs.split(";");
  for (var cookie of cookies) {
    var cl = cookie.split("=");
    if (key.trim() == cl[0].trim()) {
      return cl[1]
    }
  }
  return ""
}

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
      $.post("/api/v1/memo/word/"+word.learning_id, {
          status: word.status,
          csrfmiddlewaretoken: get_cookie("csrftoken")
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
      $.post("/api/v1/memo/finish", {
        csrfmiddlewaretoken: get_cookie("csrftoken")
      }, function (data, status) {
        if (status == "success") {
          app.finish = false;
          $.getJSON("/api/v1/memo/status", function(data, status) {
            app.words = data.words;
          })
        }
      });
    }
  },
  compiled: function () {
    var app = this;
    $.getJSON("/api/v1/memo/status", function(data, status) {
      app.words = data.words;
    });
  }
});
