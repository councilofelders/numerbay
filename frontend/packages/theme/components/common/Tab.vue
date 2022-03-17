<template>
  <div class="nav-tabs-wrap">
       <div class="row">
            <div class="col-lg-8 mx-auto">
                <ul class="nav nav-pills nav-pills-s1 mb-5 justify-content-center" id="pills-tab" role="tablist">
                    <li class="nav-item" role="presentation" v-for="list in SectionData.howItWorkData.tabNav" :key="list.id">
                        <button class="nav-link" :class="list.isActive" :id="list.slug" data-bs-toggle="pill" :data-bs-target="list.bsTarget" type="button">
                            {{ list.title }}
                        </button>
                    </li>
                </ul>
            </div><!-- end col -->
            <div class="col-lg-12">
                <div class="tab-content" id="pills-tabContent">
                    <div class="tab-pane show active" id="pills-connect-wallet" role="tabpanel" aria-labelledby="pills-connect-wallet-tab">
                        <div class="row align-items-center justify-content-center">
                            <div class="col-lg-4">
                                <div class="card-tab-img mb-5 mb-lg-0">
                                    <img :src="require('@/images/thumb/tabs01-img.png')" alt="" class="img">
                                </div>
                            </div><!-- end col -->
                            <div class="col-lg-7 ps-lg-5">
                                <div class="card-tab">
                                    <h3 class="card-tab-title">Choose from most popular wallets</h3>
                                    <p class="card-tab-text">Whether it be Metamask, the go-to wallet for crypto veterans or Fortmatic that works with your phone select your preferred wallet from these and more.</p>
                                    <ul class="list-item list-item-icon">
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> 1-Click Login using your Wallet</li>
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Your NFTs &amp; Crypto always stay in your possesion</li>
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Switch between multiple accounts in a jiffy</li>
                                    </ul>
                                    <ButtonLink :text="SectionData.howItWorkData.btnText" link="/wallet" classname="btn btn-outline-dark"></ButtonLink>
                                </div><!-- end card-tab -->
                            </div><!-- end col -->
                        </div><!-- end row -->
                    </div><!-- end tab-pane -->
                    <div class="tab-pane" id="pills-create-nft-store" role="tabpanel" aria-labelledby="pills-create-nft-store-tab">
                        <div class="row align-items-center justify-content-center">
                            <div class="col-lg-4">
                                <div class="card-tab-img mb-5 mb-lg-0">
                                    <img :src="require('@/images/thumb/tabs02-img.png')" alt="" class="img">
                                </div>
                            </div><!-- end col -->
                            <div class="col-lg-7 ps-lg-5">
                                <div class="card-tab">
                                    <h3 class="card-tab-title">Bring your brand to life</h3>
                                    <p class="card-tab-text">Enter your brand details like name, logo, etc and voila! Your NFT Marketplace is ready to conquer the world!</p>
                                    <ul class="list-item list-item-icon">
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Integrate your favorite Analytics tools</li>
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Easily connect CRM, Mailchimp, and a lot more</li>
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Enable KYC for your store with 1 click</li>
                                    </ul>
                                    <ButtonLink :text="SectionData.howItWorkData.btnText" link="/wallet" classname="btn btn-outline-dark"></ButtonLink>
                                </div><!-- end card-tab -->
                            </div><!-- end col -->
                        </div><!-- end row -->
                    </div><!-- end tab-pane -->
                    <div class="tab-pane" id="pills-start-selling" role="tabpanel" aria-labelledby="pills-start-selling-tab">
                        <div class="row align-items-center justify-content-center">
                            <div class="col-lg-4">
                                <div class="card-tab-img mb-5 mb-lg-0">
                                    <img :src="require('@/images/thumb/tabs03-img.png')" alt="" class="img">
                                </div>
                            </div><!-- end col -->
                            <div class="col-lg-7 ps-lg-5">
                                <div class="card-tab">
                                    <h3 class="card-tab-title">Start selling and growing </h3>
                                    <p class="card-tab-text">Upload your assets, add their details like name, description, etc and mint them with a click. Focus on your brand while we take care of the tech.</p>
                                    <ul class="list-item list-item-icon">
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Create both Non-Fungible (unique) &amp; Semi-Fungible (limited edition) tokens</li>
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Airdrop millions of tokens in a jiffy</li>
                                        <li><span class="ni ni-check icon icon-circle icon-wbg icon-xs"></span> Secure your assets and enable NFT based ticketing for viewing them</li>
                                    </ul>
                                    <ButtonLink :text="SectionData.howItWorkData.btnText" link="/wallet" classname="btn btn-outline-dark"></ButtonLink>
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
  data () {
    return {
      SectionData
    }
  }
}
</script>