Vue.component('form-input', {
  template: '#form-input'
});

Vue.component('form-select', {
  template: '#form-select'
});

Vue.component('form-textarea', {
  template: '#form-textarea'
});

new Vue({
  el: '#posts',
  data: {
    fields: [],
    count: 0
  },

  methods: {
    addFormElement: function(type) {
      this.fields.push({
        'type': type,
        id: this.count++
      });
    }
  }
})
