import 'htmx.org';
import {createApp} from 'petite-vue';

htmx.on("htmx:load", function(evt) {
  createApp().mount(evt.detail.elt);
});
