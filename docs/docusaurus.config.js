// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'NumerBay',
  tagline: 'The Numerai Community Marketplace',
  url: 'https://docs.numerbay.ai',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'councilofelders', // Usually your GitHub org/user name.
  projectName: 'numerbay', // Usually your repo name.

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          sidebarCollapsed: false,
          // Please change this to your repo.
          editUrl:
            'https://github.com/councilofelders/numerbay/tree/master/docs/',
        },
        blog: {
          path: 'updates',
          blogTitle: 'Project Updates',
          blogDescription: 'Project Updates',
          routeBasePath: 'updates',
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/councilofelders/numerbay/tree/master/docs/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'NumerBay',
        logo: {
          alt: 'Numerai Logo 2021',
          src: 'img/Numerai-Logo-Icon.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Tutorial',
          },
          {
            "to": "/docs/reference/numerbay",
            "label": "Python Client",
            "position": "left"
          },
          { to: '/updates', label: 'Project Updates', position: 'left' },
          {
            href: 'https://github.com/councilofelders/numerbay',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: '/docs/intro',
              },
              {
                label: 'API Reference (Swagger)',
                href: 'https://numerbay.ai/docs',
              },
              {
                label: 'API Reference (ReDoc)',
                href: 'https://numerbay.ai/redoc',
              },
            ],
          },
          {
            title: 'Official Numerai',
            items: [
              {
                label: 'Numerai',
                href: 'https://numer.ai/',
              },
              {
                label: 'Signals',
                href: 'https://signals.numer.ai/',
              },
              {
                label: 'Forum',
                href: 'https://forum.numer.ai/',
              },
              {
                label: 'Discord',
                href: 'https://discord.gg/numerai',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'NumerBay',
                href: 'https://numerbay.ai/',
              },
              {
                label: 'CoE Wallet',
                href: 'https://gnosis-safe.io/app/#/safes/0xF58B7c28DAF13926329ef0c74FA3f7258f5A9131/',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Project Updates',
                to: '/updates',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/councilofelders/numerbay',
              },
            ],
          },
        ],
        copyright: `Logo: Numerai, ${new Date().getFullYear()}. Sponsored by Numerai Council of Elders. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
  plugins: [
    // ... Your other plugins.
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        // ... Your options.
        // `hashed` is recommended as long-term-cache of index file is possible.
        hashed: true,
        blogDir:"./updates/"
        // For Docs using Chinese, The `language` is recommended to set to:
        // ```
        // language: ["en", "zh"],
        // ```
        // When applying `zh` in language, please install `nodejieba` in your project.
      },
    ],
  ],
};

module.exports = config;
