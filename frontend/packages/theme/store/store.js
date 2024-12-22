// All Section data goes here
const SectionData = {
  logoData: [
    {
      imgClass: 'logo-dark',
      logoImg: require('@/images/logo-black.png'),
      path: '/home'
    },
    {
      imgClass: 'logo-light',
      logoImg: require('@/images/logo-white.png'),
      path: '/home'
    }
  ],
  // Hero data Six
  heroDataSix: {
    title: 'Buy and sell anything Numerai',
    content: 'The easy way to help build the world\'s last hedge fund with NumerBay - the Numerai community marketplace.'
  },
  // Breadcrumb data
  breadcrumbData: {
    breadcrumbList: {
      title: 'Explore',
      navList: [
        {
          title: 'Explore'
        }
      ]
    }
  },
  // Hero btn data
  btnDataThree: [
    {
      btnClass: 'btn-lg btn-dark',
      title: 'Buy',
      path: '/explore/numerai-predictions'
    },
    {
      btnClass: 'btn-lg btn-outline-dark',
      title: 'Sell',
      path: '/create-listing'
    }
  ],
  // Header data
  headerData: {
    btnText: 'Connect',
    inputPlaceholderText: 'Search item here...',
    menuList: {
      title: 'Home',
      navList: [
        {
          id: 1,
          title: 'Home Page 1',
          path: '/'
        },
        {
          id: 2,
          title: 'Home Page 2',
          path: '/home-v2'
        },
        {
          id: 3,
          title: 'Home Page 3',
          path: '/home-v3'
        },
        {
          id: 4,
          title: 'Home Page 4',
          badge: 'New',
          badgeClass: 'badge text-primary bg-primary-50',
          path: '/home-v4'
        },
        {
          id: 5,
          title: 'Home Page 5',
          badge: 'New',
          badgeClass: 'badge text-primary bg-primary-50',
          path: '/home-v5'
        },
        {
          id: 6,
          title: 'Home Page 6',
          badge: 'New',
          badgeClass: 'badge text-primary bg-primary-50',
          path: '/home-v6'
        },
        {
          id: 7,
          title: 'Home Page 7',
          badge: 'New',
          badgeClass: 'badge text-primary bg-primary-50',
          path: '/home-v7'
        }
      ]
    }
  },
  // Freatured creator data
  featuredCreatorsData: {
    title: 'Featured Creators',
    content: 'Sample content.',
    btnText: 'View all creators'
  },
  // Freatured data
  featuredData: {
    title: 'Sample title',
    content: 'Sample content.'
  },
  // how It Work Data
  howItWorkData: {
    title: 'Sample title',
    content: 'Sample content.',
    titleTwo: 'Sample content 2.',
    titleThree: 'Sample content 3.',
    btnText: 'Create Store',
    howItWorkList: [
      {
        id: 1,
        icon: 'icon ni ni-wallet icon-lg icon-circle shadow-sm icon-wbg mx-auto mb-4 text-primary',
        title: 'Set up your wallet',
        content: 'Sample content'
      },
      {
        id: 2,
        icon: 'icon ni ni-file-text icon-lg icon-circle shadow-sm icon-wbg mx-auto mb-4 text-danger',
        title: 'Create collection',
        content: 'Sample content'
      },
      {
        id: 3,
        icon: 'icon ni ni-money icon-lg icon-circle shadow-sm icon-wbg mx-auto mb-4 text-success',
        title: 'List them for sale',
        content: 'Sample content'
      }
    ],
    howItWorkListThree: [
      {
        id: 1,
        icon: 'icon ni ni-wallet icon-md icon-circle icon-wbg me-3 text-blue bg-blue-100',
        title: 'Set up your wallet',
        content: 'Sample content'
      },
      {
        id: 2,
        icon: 'icon ni ni-file-text icon-md icon-circle icon-wbg me-3 text-purple bg-purple-100',
        title: 'Create collection',
        content: 'Sample content'
      },
      {
        id: 3,
        icon: 'icon ni ni-money icon-md icon-circle icon-wbg me-3 text-orange bg-orange-100',
        title: 'List them for sale',
        content: 'Sample content'
      }
    ],
    howItWorkListFour: [
      {
        id: 1,
        title: 'Sample title',
        content: 'Sample content'
      },
      {
        id: 2,
        title: 'Sample title',
        content: 'Sample content'
      }
    ],
    tabNav: [
      {
        id: 1,
        isActive: 'active',
        title: 'Connect Your Wallet',
        slug: 'pills-connect-wallet-tab',
        bsTarget: '#pills-connect-wallet'
      },
      {
        id: 2,
        title: 'Create Your Store',
        slug: 'pills-create-nft-store-tab',
        bsTarget: '#pills-create-store'
      },
      {
        id: 3,
        title: 'Start Selling & Growing',
        slug: 'pills-start-selling-tab',
        bsTarget: '#pills-start-selling'
      }
    ]
  },
  // Category Data
  categoryData: {
    title: 'Browse by category',
    content: 'Explore listed products for the Numerai and Signals tournaments.',
    categoryList: [
      {
        id: 1,
        class: 'text-purple',
        icon: 'icon ni ni-bulb mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Numerai',
        path: '/explore/numerai'
      },
      {
        id: 2,
        class: 'text-purple',
        icon: 'icon ni ni-bulb mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Numerai Predictions',
        path: '/explore/numerai-predictions'
      },
      {
        id: 3,
        class: 'text-purple',
        icon: 'icon ni ni-bulb mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Numerai Models',
        path: '/explore/numerai-models'
      },
      {
        id: 4,
        class: 'text-blue',
        icon: 'icon ni ni-signal mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Signals',
        path: '/explore/signals'
      },
      {
        id: 5,
        class: 'text-blue',
        icon: 'icon ni ni-signal mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Signals Predictions',
        path: '/explore/signals-predictions'
      },
      {
        id: 6,
        class: 'text-blue',
        icon: 'icon ni ni-signal mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Signals Data',
        path: '/explore/signals-data'
      },
      {
        id: 7,
        class: 'text-green',
        icon: 'icon ni ni-bulb mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Crypto',
        path: '/explore/crypto'
      },
      {
        id: 8,
        class: 'text-green',
        icon: 'icon ni ni-bulb mb-3 mx-auto icon-circle icon-wbg icon-lg',
        title: 'Crypto Predictions',
        path: '/explore/crypto-predictions'
      },
    ]
  },
  // account sidebar
  accountSidebarData: {
    title: 'Account Settings',
    navList: [
      {
        id: 1,
        class: 'active',
        icon: 'ni-edit',
        title: 'Edit Profile',
        path: 'account'
      },
      {
        id: 2,
        icon: 'ni-cart',
        title: 'Purchases',
        path: 'purchases'
      },
      {
        id: 3,
        icon: 'ni-money',
        title: 'Sales',
        path: 'sales'
      },
      {
        id: 4,
        icon: 'ni-list-index',
        title: 'My Listings',
        path: 'listings'
      },
      {
        id: 5,
        icon: 'ni-setting',
        title: 'Numerai Settings',
        path: 'numerai-settings'
      },
      {
        id: 6,
        icon: 'ni-gift',
        title: 'My Coupons',
        path: 'coupons'
      },
      {
        id: 7,
        icon: 'ni-bar-c',
        title: 'My Polls',
        path: 'polls'
      }
    ]
  },
  // edit profile data
  editProfileData: {
    title: 'Account Settings',
    editProfileTabNav: [
      {
        id: 1,
        isActive: 'active',
        title: 'Edit Info',
        slug: 'account-information-tab',
        bsTarget: '#account-information'
      },
      {
        id: 2,
        title: 'Password',
        slug: 'change-password-tab',
        bsTarget: '#change-password'
      }
      // {
      //   id: 3,
      //   title: 'Verify Profile',
      //   slug: 'validate-profile-tab',
      //   bsTarget: '#validate-profile'
      // }
    ],
    // edit profile tab mobile
    editProfileTabNavMobile: [
      {
        id: 1,
        isActive: 'active',
        title: 'Account Information',
        slug: 'account-information-tab-mobile',
        bsTarget: '#account-information-mobile'
      },
      {
        id: 2,
        title: 'Change Password',
        slug: 'change-password-tab-mobile',
        bsTarget: '#change-password-mobile'
      },
      {
        id: 3,
        title: 'Validate Profile',
        slug: 'validate-profile-tab-mobile',
        bsTarget: '#validate-profile-mobile'
      }
    ]
  },
  loginData: {
    img: require('@/images/thumb/remote.png'),
    title: 'Welcome Back!',
    subTitle: 'Login to countinue',
    btnText: 'Login Now',
    haveAccountText: 'Don\'t have an account',
    btnTextTwo: 'Sign Up',
    btnTextLink: 'register',
    btns: [
      {
        title: 'Google',
        btnClass: 'bg-red-100 text-red g-btn',
        icon: 'ni-google',
        path: ''
      },
      {
        title: 'Facebook',
        btnClass: 'bg-blue-100 text-blue f-btn',
        icon: 'ni-facebook-f',
        path: ''
      },
      {
        title: 'Twitter',
        btnClass: 'bg-cyan-100 text-cyan t-btn',
        icon: 'ni-twitter',
        path: ''
      }
    ]
  },
  // login tab nav
  loginTabNav: [
    {
      id: 1,
      isActive: 'active',
      img: require('@/images/brand/metamask.svg'),
      title: 'MetaMask',
      slug: 'meta-mask-tab',
      bsTarget: '#meta-mask'
    },
    {
      id: 2,
      img: require('@/images/thumb/icon-users.svg'),
      title: 'Username (Legacy)',
      slug: 'wallet-connect-tab',
      bsTarget: '#wallet-connect'
    }
  ],
  // login data two
  loginDataTwo: {
    title: 'Connect Your MetaMask Wallet',
    titleTwo: 'Login With Username',
    btnText: 'Connect',
    btnTextFour: 'Login',
    btnTextTwo: 'Learn how to use MetaMask Wallet',
    btnTextThree: 'Learn how to use Walletconnect Wallet',
    btnTextLink: 'https://metamask.io/faqs/',
    btnTextLinkTwo: '',
    btnLink: 'login'
  },
  // filter cat data
  filterCatData: {
    title: 'Category'
  },
  placeBidModal: {
    title: 'Place a Bid',
    btnText: 'Place a Bid',
    btnLink: '/purchases'
  },
  // footer data
  footerData: {
    content: 'The Numerai community marketplace funded by the Numerai Council of Elders.',
    footerList: [
      {
        id: 1,
        title: 'Marketplace',
        navList: [
          {
            title: 'All NFTs',
            path: '/explore'
          },
          {
            title: 'Art',
            path: '/explore'
          },
          {
            title: 'Music',
            path: '/explore'
          },
          {
            title: 'Domain Names',
            path: '/explore'
          },
          {
            title: 'Virtual World',
            path: '/explore'
          }
        ]
      },
      {
        id: 2,
        title: 'My Account',
        navList: [
          {
            title: 'Profile',
            path: 'profile'
          },
          {
            title: 'My Offers',
            path: 'offers'
          },
          {
            title: 'Activity',
            path: 'activity'
          },
          {
            title: 'Sales & Purchase',
            path: 'purchases-sales'
          },
          {
            title: 'Payment Methods',
            path: 'payment-methods'
          }
        ]
      },
      {
        id: 3,
        title: 'Company',
        navList: [
          {
            title: 'About',
            path: 'about-us'
          },
          {
            title: 'Blog',
            path: 'blog'
          },
          {
            title: 'Contact',
            path: 'contact'
          },
          {
            title: 'Careers',
            path: 'about-us'
          }
        ]
      }
    ],
    footerListTwo: [
      {
        title: 'Explore',
        path: '/explore'
      },
      {
        title: 'Activity',
        path: 'activity'
      },
      {
        title: 'Login',
        path: 'login'
      },
      {
        title: 'Wallet',
        path: 'wallet'
      }
    ]
  }
};

export default SectionData;
