---
sidebar_position: 2
---

# Buy a Product

Documents are **groups of pages** connected through:

- a **sidebar**
- **previous/next navigation**
- **versioning**

## Browse products

- [Classic Numerai Tournament Products](https://numerbay.ai/c/numerai)
- [Signals Tournament Products](https://numerbay.ai/c/signals)
- [NFTs and Others](https://numerbay.ai/c/onlyfams)

## Checkout

You need to have a [NumerBay account](/docs/tutorial-basics/set-up-account) with Numerai API Key in order to checkout.

## Payment

## Download artifacts

## Submission

## Manage orders

Docusaurus automatically **creates a sidebar** from the `docs` folder.

Add metadata to customize the sidebar label and position:

```md title="docs/hello.md" {1-4}
---
sidebar_label: 'Hi!'
sidebar_position: 3
---

# Hello

This is my **first Docusaurus document**!
```

It is also possible to create your sidebar explicitly in `sidebars.js`:

```diff title="sidebars.js"
module.exports = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Tutorial',
-     items: [...],
+     items: ['hello'],
    },
  ],
};
```

