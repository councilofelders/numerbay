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
import HeaderDashboard from '../components/common/HeaderDashboard.vue';
import SectionHeading from '../components/common/SectionHeading.vue';
import SectionHeadingTwo from '../components/common/SectionHeadingTwo.vue';
import ProductsContainer from '../components/section/ProductsContainer.vue';
import FeaturedCreators from '../components/section/FeaturedCreators.vue';
import Footer from '../pages/Footer.vue';
import FooterSection from '../components/section/FooterSection.vue';
import ButtonLink from '../components/common/ButtonLink.vue';
import ButtonGroup from '../components/common/ButtonGroup.vue';
import LogoLink from '../components/common/LogoLink.vue';
import Tab from '../components/common/Tab.vue';
import Featured from '../components/section/Featured.vue';
import HowItWork from '../components/section/HowItWork.vue';
import HowItWorkItem from '../components/common/HowItWorkItem.vue';
import HowItWorkSlider from '../components/common/HowItWorkSlider.vue';
import Category from '../components/section/Category.vue';
import Newsletter from '../components/section/Newsletter.vue';
import FeaturedCreatorSlider from '../components/common/FeaturedCreatorSlider.vue';
import ExploreSection from '../components/section/ExploreSection.vue';
import Filters from '../components/common/Filters.vue';
import TopCreators from '../components/section/TopCreators.vue';
import Creators from '../components/common/Creators.vue';
import Collections from '../components/section/Collections.vue';
import CollectionsTwo from '../components/section/CollectionsTwo.vue';
import CollectionSlider from '../components/common/CollectionSlider.vue';
import ModelMetricsCard from '../components/section/ModelMetricsCard.vue';
import Modal from '../components/common/Modal.vue';
import ArtifactModal from '../components/section/ArtifactModal.vue';
import OrderInfoModal from '../components/section/OrderInfoModal.vue';
import PricingOptionModal from '../components/section/PricingOptionModal.vue';
import RelatedProducts from '../components/section/RelatedProducts.vue';
import AuthorHero from '../components/section/AuthorHero.vue';
import Pagination from '../components/common/Pagination.vue';
import Comments from '../components/common/Comments.vue';
import Form from '../components/common/Form.vue';
import Range from '../components/common/Range.vue';
import LoginSection from '../components/section/LoginSection.vue';
import LoginSectionTwo from '../components/section/LoginSectionTwo.vue';
import UserSidebar from '../components/common/UserSidebar.vue';
import ListingsSection from '../components/section/ListingsSection.vue';
import PurchasesSection from '../components/section/PurchasesSection.vue';
import SalesSection from '../components/section/SalesSection.vue';
import AccountSection from '../components/section/AccountSection.vue';
import NumeraiSettingSection from '../components/section/NumeraiSettingSection.vue';
import Notification from '../components/common/Notification.vue';
import ThemeSwitcher from '../components/common/ThemeSwitcher.vue';
// import LazyHydrate from 'vue-lazy-hydration';

// Global page components register
Vue.component('HeaderMain', HeaderMain);
Vue.component('HeaderDashboard', HeaderDashboard);
Vue.component('SectionHeading', SectionHeading);
Vue.component('SectionHeadingTwo', SectionHeadingTwo);
Vue.component('ProductsContainer', ProductsContainer);
Vue.component('FeaturedCreators', FeaturedCreators);
Vue.component('Footer', Footer);
Vue.component('FooterSection', FooterSection);
Vue.component('ButtonLink', ButtonLink);
Vue.component('ButtonGroup', ButtonGroup);
Vue.component('LogoLink', LogoLink);
Vue.component('Tab', Tab);
Vue.component('Featured', Featured);
Vue.component('HowItWork', HowItWork);
Vue.component('HowItWorkItem', HowItWorkItem);
Vue.component('HowItWorkSlider', HowItWorkSlider);
Vue.component('Category', Category);
Vue.component('Newsletter', Newsletter);
Vue.component('FeaturedCreatorSlider', FeaturedCreatorSlider);
Vue.component('ExploreSection', ExploreSection);
Vue.component('Filters', Filters);
Vue.component('TopCreators', TopCreators);
Vue.component('Creators', Creators);
Vue.component('Collections', Collections);
Vue.component('CollectionsTwo', CollectionsTwo);
Vue.component('CollectionSlider', CollectionSlider);
Vue.component('ModelMetricsCard', ModelMetricsCard);
Vue.component('Modal', Modal);
Vue.component('ArtifactModal', ArtifactModal);
Vue.component('OrderInfoModal', OrderInfoModal);
Vue.component('PricingOptionModal', PricingOptionModal);
Vue.component('RelatedProducts', RelatedProducts);
Vue.component('AuthorHero', AuthorHero);
Vue.component('Pagination', Pagination);
Vue.component('Comments', Comments);
Vue.component('Form', Form);
Vue.component('Range', Range);
Vue.component('LoginSection', LoginSection);
Vue.component('LoginSectionTwo', LoginSectionTwo);
Vue.component('UserSidebar', UserSidebar);
Vue.component('ListingsSection', ListingsSection);
Vue.component('PurchasesSection', PurchasesSection);
Vue.component('SalesSection', SalesSection);
Vue.component('AccountSection', AccountSection);
Vue.component('NumeraiSettingSection', NumeraiSettingSection);
Vue.component('Notification', Notification);
Vue.component('ThemeSwitcher', ThemeSwitcher);
// Vue.component('LazyHydrate', LazyHydrate);

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

extend('alpha_dash', {
  // eslint-disable-next-line camelcase
  ...alpha_dash,
  message: 'The field should only contain alphabetic characters, numbers, dashes or underscores'
});
