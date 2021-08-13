import Category from './category';
import Cart from './components/cart-sidebar';
import LoginModal from './components/login-modal';
import Home from './home';
import Product from './product';
import { Sidebar } from './my-account';

const page = {
  get cart() {
    return Cart;
  },
  get category() {
    return Category;
  },
  get components() {
    return {
      cart: Cart,
      loginModal: LoginModal
    };
  },
  get home() {
    return Home;
  },
  get myAccount() {
    return {
      sidebar: new Sidebar()
    };
  },
  get product() {
    return Product;
  }
};

export default page;
