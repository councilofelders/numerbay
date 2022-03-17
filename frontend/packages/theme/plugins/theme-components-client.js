// // bootstrap
// import 'bootstrap';
// import { Modal } from 'bootstrap';
//
// // eslint-disable-next-line no-unused-vars,@typescript-eslint/no-unused-vars
// export default async ({env}, inject) => {
//   inject('bsModal', Modal);
// };

import { Dropdown, Modal } from 'bootstrap';
import Vue from 'vue';

Vue.mixin({
  methods: {
    getBootstrapModal(id) {
      return new Modal(id);
    },
    getBootstrapDropdown(id) {
      return new Dropdown(id);
    }
  }
});
