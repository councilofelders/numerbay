import webpack from 'webpack';
// import { Integrations } from '@sentry/tracing';
import { getRoutes } from './routes';

export default {
  mode: 'universal',
  server: {
    port: 3000,
    host: '0.0.0.0'
  },
  head: {
    title: 'NumerBay - The Numerai Community Marketplace',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico'
      },
      {
        rel: 'preconnect',
        href: 'https://fonts.gstatic.com',
        crossorigin: 'crossorigin'
      },
      {
        rel: 'preload',
        href: 'https://fonts.googleapis.com/css?family=Raleway:300,400,400i,500,600,700|Roboto:300,300i,400,400i,500,700&display=swap',
        as: 'style'
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Raleway:300,400,400i,500,600,700|Roboto:300,300i,400,400i,500,700&display=swap',
        media: 'print',
        onload: 'this.media=\'all\'',
        once: true
      }
    ]
  },
  loading: { color: '#fff' },
  plugins: [
    { src: 'plugins/theme-components', ssr: true },
    { src: 'plugins/theme-components-client', ssr: false, mode: 'client' },
    { src: 'plugins/wallet', ssr: false },
    // { src: 'plugins/nuxt-star-rating-plugin', ssr: false },
    { src: 'plugins/nuxt-multiselect-plugin', ssr: false },
    { src: 'plugins/nuxt-quill-plugin', ssr: false },
    { src: 'plugins/nuxt-clipboard2', ssr: false },
    { src: 'plugins/nuxt-poll-plugin', ssr: false }
  ],
  css: [
    'quill/dist/quill.core.css',
    // for snow theme
    'quill/dist/quill.snow.css',
    'vue-multiselect/dist/vue-multiselect.min.css'
  ],
  buildModules: [
    // to core
    '@nuxt/typescript-build',
    '@nuxtjs/style-resources',
    ['@vue-storefront/nuxt', {
      logger: {
        verbosity: 'debug'
      },
      // @core-development-only-start
      coreDevelopment: true,
      // @core-development-only-end
      useRawSource: {
        dev: [
          '@vue-storefront/numerbay',
          '@vue-storefront/core'
        ],
        prod: [
          '@vue-storefront/numerbay',
          '@vue-storefront/core'
        ]
      }
    }],
    ['@vue-storefront/numerbay/nuxt', {
      i18n: {
        useNuxtI18nConfig: true
      }
    }]
  ],
  modules: [
    'nuxt-i18n',
    'cookie-universal-nuxt',
    'vue-scrollto/nuxt',
    '@vue-storefront/middleware/nuxt',
    '@nuxtjs/sentry',
    ['v-sanitize/nuxt', {}]
  ],
  sanitize: {
    allowedTags: [
      "address", "article", "aside", "footer", "header", "h1", "h2", "h3", "h4",
      "h5", "h6", "hgroup", "main", "nav", "section", "blockquote", "dd", "div",
      "dl", "dt", "figcaption", "figure", "hr", "li", "main", "ol", "p", "pre",
      "ul", "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "dfn",
      "em", "i", "kbd", "mark", "q", "rb", "rp", "rt", "rtc", "ruby", "s", "samp",
      "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr", "caption",
      "col", "colgroup", "table", "tbody", "td", "tfoot", "th", "thead", "tr",
      "img"
    ],
    disallowedTagsMode: 'discard',
    allowedAttributes: {
      a: [ 'href', 'name', 'target' ],
      img: [ 'src', 'srcset', 'alt', 'title', 'width', 'height', 'loading' ],
      pre: ['class'],
      ul: ['data-checked']
    },
    selfClosing: [ 'img', 'br', 'hr', 'area', 'base', 'basefont', 'input', 'link', 'meta' ],
    allowedSchemes: [ 'http', 'https', 'ftp', 'mailto', 'tel' ],
    allowedSchemesByTag: {
      img: [ 'data', 'http', 'https' ]
    },
    allowedSchemesAppliedToAttributes: [ 'href', 'src', 'cite' ],
    allowProtocolRelative: true,
    enforceHtmlBoundary: false
  },
  sentry: {
    dsn: `${process.env.SENTRY_DSN || 'https://9408b20ebf9e4d8e9c2466c9d8fe50b2@o920394.ingest.sentry.io/5865987'}`,
    tracing: {
      tracesSampleRate: 1.0,
      vueOptions: {
        tracing: true,
        tracingOptions: {
          hooks: ['mount', 'update'],
          timeout: 2000,
          trackComponents: true
        }
      },
      browserOptions: {}
    },
    config: {
      // Add native Sentry config here
      // https://docs.sentry.io/platforms/javascript/guides/vue/configuration/options/
      debug: false,
      autoSessionTracking: true
    }
  },
  i18n: {
    currency: 'USD',
    country: 'US',
    countries: [
      { name: 'US',
        label: 'United States'
      },
      { name: 'AT',
        label: 'Austria' },
      { name: 'DE',
        label: 'Germany' },
      { name: 'NL',
        label: 'Netherlands' }
    ],
    currencies: [
      {
        name: 'EUR',
        label: 'Euro'
      },
      {
        name: 'USD',
        label: 'Dollar'
      },
      {
        name: 'NMR',
        label: 'Numeraire'
      }
    ],
    locales: [
      {
        code: 'en',
        label: 'English',
        file: 'en.js',
        iso: 'en'
      }
    ],
    defaultLocale: 'en',
    strategy: 'no_prefix',
    vueI18n: {
      silentTranslationWarn: true,
      silentFallbackWarn: true,
      fallbackLocale: 'en',
      numberFormats: {
        en: {
          currency: {
            style: 'currency', currency: 'USD', currencyDisplay: 'symbol'
          }
        },
        de: {
          currency: {
            style: 'currency', currency: 'EUR', currencyDisplay: 'symbol'
          }
        }
      },
      messages: {
        en: {
          welcome: 'Welcome 1'
        }
      }
    }
  },
  styleResources: {
  },
  build: {
    transpile: [
      'vee-validate/dist/rules'
    ],
    plugins: [
      new webpack.DefinePlugin({
        'process.VERSION': JSON.stringify({
          // eslint-disable-next-line global-require
          version: require('./package.json').version,
          lastCommit: process.env.LAST_COMMIT || ''
        })
      })
    ]
  },
  router: {
    scrollBehavior (_to, _from, savedPosition) {
      if (savedPosition) {
        return savedPosition;
      } else {
        return { x: 0, y: 0 };
      }
    },
    extendRoutes(routes) {
      getRoutes(`${__dirname}`).forEach((route) => routes.unshift(route));
    }
  }
};
