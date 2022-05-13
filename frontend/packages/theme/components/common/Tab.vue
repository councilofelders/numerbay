<template>
  <div class="nav-tabs-wrap">
    <div class="row">
      <div class="col-lg-8 mx-auto">
        <ul id="pills-tab" class="nav nav-pills nav-pills-s1 mb-5 justify-content-center" role="tablist">
          <li v-for="list in SectionData.howItWorkData.tabNav" :key="list.id" class="nav-item" role="presentation">
            <button :id="list.slug" :class="list.isActive" :data-bs-target="list.bsTarget" class="nav-link"
                    data-bs-toggle="pill" type="button">
              {{ list.title }}
            </button>
          </li>
        </ul>
      </div><!-- end col -->
      <div class="col-lg-12">
        <div id="pills-tabContent" class="tab-content">
          <div id="pills-connect-wallet" aria-labelledby="pills-connect-wallet-tab" class="tab-pane show active"
               role="tabpanel">
            <div class="row align-items-center justify-content-center">
              <div class="col-lg-4">
                <div class="card-tab-img mb-5 mb-lg-0">
                  <img :src="require('@/images/thumb/tabs01-img.png')" alt="" class="img">
                </div>
              </div><!-- end col -->
              <div class="col-lg-7 ps-lg-5">
                <div class="card-tab">
                  <h3 class="card-tab-title">Choose from most popular wallets</h3>
                  <p class="card-tab-text">Whether it be Metamask, the go-to wallet for crypto veterans or Fortmatic
                    that works with your phone select your preferred wallet from these and more.</p>
                  <ul class="list-item list-item-icon">
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> 1-Click Login using your
                      Wallet
                    </li>
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Your NFTs &amp; Crypto
                      always stay in your possesion
                    </li>
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Switch between multiple
                      accounts in a jiffy
                    </li>
                  </ul>
                  <ButtonLink :text="SectionData.howItWorkData.btnText" classname="btn btn-outline-dark"
                              link="/wallet"></ButtonLink>
                </div><!-- end card-tab -->
              </div><!-- end col -->
            </div><!-- end row -->
          </div><!-- end tab-pane -->
          <div id="pills-create-nft-store" aria-labelledby="pills-create-nft-store-tab" class="tab-pane"
               role="tabpanel">
            <div class="row align-items-center justify-content-center">
              <div class="col-lg-4">
                <div class="card-tab-img mb-5 mb-lg-0">
                  <img :src="require('@/images/thumb/tabs02-img.png')" alt="" class="img">
                </div>
              </div><!-- end col -->
              <div class="col-lg-7 ps-lg-5">
                <div class="card-tab">
                  <h3 class="card-tab-title">Bring your brand to life</h3>
                  <p class="card-tab-text">Enter your brand details like name, logo, etc and voila! Your NFT Marketplace
                    is ready to conquer the world!</p>
                  <ul class="list-item list-item-icon">
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Integrate your favorite
                      Analytics tools
                    </li>
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Easily connect CRM,
                      Mailchimp, and a lot more
                    </li>
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Enable KYC for your store
                      with 1 click
                    </li>
                  </ul>
                  <ButtonLink :text="SectionData.howItWorkData.btnText" classname="btn btn-outline-dark"
                              link="/wallet"></ButtonLink>
                </div><!-- end card-tab -->
              </div><!-- end col -->
            </div><!-- end row -->
          </div><!-- end tab-pane -->
          <div id="pills-start-selling" aria-labelledby="pills-start-selling-tab" class="tab-pane" role="tabpanel">
            <div class="row align-items-center justify-content-center">
              <div class="col-lg-4">
                <div class="card-tab-img mb-5 mb-lg-0">
                  <img :src="require('@/images/thumb/tabs03-img.png')" alt="" class="img">
                </div>
              </div><!-- end col -->
              <div class="col-lg-7 ps-lg-5">
                <div class="card-tab">
                  <h3 class="card-tab-title">Start selling and growing </h3>
                  <p class="card-tab-text">Upload your assets, add their details like name, description, etc and mint
                    them with a click. Focus on your brand while we take care of the tech.</p>
                  <ul class="list-item list-item-icon">
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Create both Non-Fungible
                      (unique) &amp; Semi-Fungible (limited edition) tokens
                    </li>
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Airdrop millions of tokens
                      in a jiffy
                    </li>
                    <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Secure your assets and
                      enable NFT based ticketing for viewing them
                    </li>
                  </ul>
                  <ButtonLink :text="SectionData.howItWorkData.btnText" classname="btn btn-outline-dark"
                              link="/wallet"></ButtonLink>
                </div><!-- end card-tab -->
              </div><!-- end col -->
            </div><!-- end row -->
          </div><!-- end -->
        </div>
      </div><!-- end col -->
    </div>
  </div><!-- end nav-tabs-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'

export default {
  name: 'Tab',
  data() {
    return {
      SectionData
    }
  }
}
</script>
