import Vue from 'vue';

// vue select
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';

Vue.component('v-select', vSelect);

// template custom css
import '../assets/scss/bundles.scss';
import '../assets/scss/style.scss';

// Global page components imported
import HeaderMain from '../components/common/HeaderMain.vue';
import SectionHeading from '../components/common/SectionHeading.vue';
import Footer from '../pages/Footer.vue';
import FooterSection from '../components/section/FooterSection.vue';
import ButtonLink from '../components/common/ButtonLink.vue';
import ButtonGroup from '../components/common/ButtonGroup.vue';
import LogoLink from '../components/common/LogoLink.vue';
import Tab from '../components/common/Tab.vue';
import Modal from '../components/common/Modal.vue';
import AuthorHero from '../components/section/AuthorHero.vue';
import Pagination from '../components/common/Pagination.vue';
import UserSidebar from '../components/common/UserSidebar.vue';
import Notification from '../components/common/Notification.vue';
import ThemeSwitcher from '../components/common/ThemeSwitcher.vue';

// Global page components register
Vue.component('HeaderMain', HeaderMain);
Vue.component('SectionHeading', SectionHeading);
Vue.component('Footer', Footer);
Vue.component('FooterSection', FooterSection);
Vue.component('ButtonLink', ButtonLink);
Vue.component('ButtonGroup', ButtonGroup);
Vue.component('LogoLink', LogoLink);
Vue.component('Tab', Tab);
Vue.component('Modal', Modal);
Vue.component('AuthorHero', AuthorHero);
Vue.component('Pagination', Pagination);
Vue.component('UserSidebar', UserSidebar);
Vue.component('Notification', Notification);
Vue.component('ThemeSwitcher', ThemeSwitcher);

// vee-validate
import { ValidationObserver, ValidationProvider, extend } from 'vee-validate';
// eslint-disable-next-line camelcase
import { alpha_dash, email, integer, max_value, min, min_value, required} from 'vee-validate/dist/rules';

Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);

extend('required', {
  ...required,
  message: 'This field is required'
});

extend('min', {
  ...min,
  message: 'The field should have at least {length} characters'
});

extend('email', {
  ...email,
  message: 'Invalid email'
});

extend('min_value', {
  // eslint-disable-next-line camelcase
  ...min_value,
  message: 'This must be positive'
});

extend('max_value', {
  // eslint-disable-next-line camelcase
  ...max_value,
  message: 'This must be lower than {max}'
});

extend('integer', {
  ...integer,
  message: 'This field must be an integer'
});

extend('decimal', {
  validate: (value, {decimals = '*', separator = '.'} = {}) => {
    if (value === null || value === undefined || value === '') {
      return {
        valid: false
      };
    }
    if (Number(decimals) === 0) {
      return {
        valid: /^-?\d*$/.test(value)
      };
    }
    const regexPart = decimals === '*' ? '+' : `{1,${decimals}}`;
    const regex = new RegExp(`^[-+]?\\d*(\\${separator}\\d${regexPart})?([eE]{1}[-]?\\d+)?$`);

    return {
      valid: regex.test(value)
    };
  },
  message: 'The {_field_} field must contain only decimal values'
});

extend('alpha_dash', {
  // eslint-disable-next-line camelcase
  ...alpha_dash,
  message: 'The field should only contain alphabetic characters, numbers, dashes or underscores'
});
