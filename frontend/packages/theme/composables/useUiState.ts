import Vue from 'vue';
import VueCompositionAPI, { reactive, computed } from '@vue/composition-api';

// We need to register it again because of Vue instance instantiation issues
Vue.use(VueCompositionAPI);

const state = reactive({
  isCartSidebarOpen: false,
  isWishlistSidebarOpen: false,
  isLoginModalOpen: false,
  isListingModalOpen: false,
  currentListing: null,
  isPollModalOpen: false,
  currentPoll: null,
  isCategoryGridView: false,
  isFilterSidebarOpen: false,
  isMobileMenuOpen: false
});

const useUiState = () => {
  const isMobileMenuOpen = computed(() => state.isMobileMenuOpen);
  const toggleMobileMenu = () => {
    state.isMobileMenuOpen = !state.isMobileMenuOpen;
  };

  const isCartSidebarOpen = computed(() => state.isCartSidebarOpen);
  const toggleCartSidebar = () => {
    if (state.isMobileMenuOpen) toggleMobileMenu();
    state.isCartSidebarOpen = !state.isCartSidebarOpen;
  };

  const isWishlistSidebarOpen = computed(() => state.isWishlistSidebarOpen);
  const toggleWishlistSidebar = () => {
    if (state.isMobileMenuOpen) toggleMobileMenu();
    state.isWishlistSidebarOpen = !state.isWishlistSidebarOpen;
  };

  const isLoginModalOpen = computed(() => state.isLoginModalOpen);
  const toggleLoginModal = () => {
    if (state.isMobileMenuOpen) toggleMobileMenu();
    state.isLoginModalOpen = !state.isLoginModalOpen;
  };

  const isListingModalOpen = computed(() => state.isListingModalOpen);
  const currentListing = computed(() => state.currentListing);
  const toggleListingModal = (product) => {
    if (state.isMobileMenuOpen) toggleMobileMenu();
    state.isListingModalOpen = !state.isListingModalOpen;
    if (!state.isListingModalOpen) {
      state.currentListing = null;
    } else {
      state.currentListing = product;
    }
  };

  const isPollModalOpen = computed(() => state.isPollModalOpen);
  const currentPoll = computed(() => state.currentPoll);
  const togglePollModal = (product) => {
    if (state.isMobileMenuOpen) toggleMobileMenu();
    state.isPollModalOpen = !state.isPollModalOpen;
    if (!state.isPollModalOpen) {
      state.currentPoll = null;
    } else {
      state.currentPoll = product;
    }
  };

  const isCategoryGridView = computed(() => state.isCategoryGridView);
  const changeToCategoryGridView = () => {
    state.isCategoryGridView = true;
  };
  const changeToCategoryListView = () => {
    state.isCategoryGridView = false;
  };

  const isFilterSidebarOpen = computed(() => state.isFilterSidebarOpen);
  const toggleFilterSidebar = () => {
    state.isFilterSidebarOpen = !state.isFilterSidebarOpen;
  };

  return {
    isCartSidebarOpen,
    isWishlistSidebarOpen,
    isLoginModalOpen,
    isListingModalOpen,
    currentListing,
    isPollModalOpen,
    currentPoll,
    isCategoryGridView,
    isFilterSidebarOpen,
    isMobileMenuOpen,
    toggleCartSidebar,
    toggleWishlistSidebar,
    toggleLoginModal,
    toggleListingModal,
    togglePollModal,
    changeToCategoryGridView,
    changeToCategoryListView,
    toggleFilterSidebar,
    toggleMobileMenu
  };
};

export default useUiState;
