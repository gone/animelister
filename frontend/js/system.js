import 'htmx.org';
import {createApp, reactive} from 'petite-vue';

const store = reactive({
  count: 0,
  global_inc() {
    this.count++
  }
})


function GlobalCounter(props) {
  return {
    count: props.initialCount,
    inc() {
      store.inc();
    },
    mounted() {
      console.log(`I'm mounted!`);
    }
  };
}


function Counter(props) {
  return {
    count: props.initialCount,
    inc() {
      this.count++
    },
    mounted() {
      console.log(`I'm mounted!`);
    }
  };
}


// manipulate it here
store.global_inc();


const app = createApp({
  store,
  GlobalCounter,
  Counter,
  $delimiters: ['${', '}']
});
//catch template jitter
app.mount(document.body);
htmx.on("htmx:afterSwap", function(evt) {
  app.mount(evt.target);
});
// htmx.on("htmx:load", function(evt) {
//     app.mount(evt.detail.elt);
//  });
