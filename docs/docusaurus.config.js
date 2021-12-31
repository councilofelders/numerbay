// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'NumerBay',
  tagline: 'The Numerai Community Marketplace',
  url: 'https://your-docusaurus-test-site.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'facebook', // Usually your GitHub org/user name.
  projectName: 'docusaurus', // Usually your repo name.

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
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
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
          { to: '/blog', label: 'Blog', position: 'left' },
          {
            href: 'https://github.com/facebook/docusaurus',
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
                label: 'RocketChat',
                href: 'https://community.numer.ai/',
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
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/councilofelders/numerbay',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
