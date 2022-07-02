<template>
  <div class="page-wrap">
    <!-- Hero  -->
    <HeroSeven></HeroSeven>
    <!-- Category  -->
    <Category classname="section-space bg-gray"></Category>
    <!-- product  -->
    <!--        <section class="section-space trending-section bg-gray">
            <div class="container">
                &lt;!&ndash; section heading &ndash;&gt;
                <SectionHeading classname="text-center" :text="SectionData.productData.title" :content="SectionData.productData.content" isMargin="mb-3"></SectionHeading>
                &lt;!&ndash; product &ndash;&gt;
                <ProductsContainer></ProductsContainer>
                <div class="text-center mt-4 mt-md-5">
                    <ButtonLink :text="SectionData.productData.btnText" :link="SectionData.productData.btnLink" classname="btn-link btn-link-s1"></ButtonLink>
                </div>
            </div>&lt;!&ndash; .container &ndash;&gt;
        </section>&lt;!&ndash; trending-section &ndash;&gt;-->
    <!-- HowItWork  -->
    <!--        <HowItWork classname="col-lg-3" :title="SectionData.howItWorkData.title" :subtitle="SectionData.howItWorkData.content" gutterBottom="mb-3"></HowItWork>-->
    <!-- Community Apps  -->
    <section class="section-space app-section">
      <div class="container">
        <!-- section heading -->
        <SectionHeading classname="text-center" content="Featured apps created by the Numerai community members."
                        isMargin="mb-3"
                        text="Community Apps"></SectionHeading>
        <!-- product -->
        <div class="row g-gs">
          <div v-for="app in apps" :key="app.id" class="col-xl-3 col-lg-4 col-sm-6">
            <div class="card card-full card-blog">
              <div class="d-block card-image">
                <img :src="app.img" alt="" class="card-img-top">
                <div class="bg-dark-transparent card-overlay">
                  <div class="d-flex align-items-center card-author">
                    <div class="flex-shrink-0 avatar avatar-2">
                      <img :src="app.avatar" alt="" class="rounded-circle">
                    </div>
                    <div class="flex-grow-1 ms-2 text-white">
                      <span>{{ app.author }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-body card-body-s1">
                <h4 class="card-title mb-3">{{ app.title }}</h4>
                <p class="card-text">{{ app.desc }}</p>
              </div><!-- end card-body -->
              <a :href="app.link" class="details" target="_blank">
              </a>
            </div><!-- end card -->
            <!--                <div class="card">
                              <div class="card-image">
                                  <img :src="app.img" alt="" class="card-img-top">
                              </div>
                              <div class="card-body d-flex align-items-center">
                                  <div class="avatar flex-shrink-0 me-2">
                                      <img :src="app.avatar" alt="">
                                  </div>
                                  <div class="text-truncate">
                                      <h6 class="card-title text-truncate mb-0">{{ app.title }}</h6>
                                      <span class="small text-secondary author-link">{{ app.author }}</span>
                                  </div>
                              </div>&lt;!&ndash; end card-body &ndash;&gt;
                              <a
                                  class="details"
                                  :href="app.link"
                              >
                              </a>
                          </div>&lt;!&ndash; end card &ndash;&gt;-->
          </div>
        </div>
        <!--            <div class="text-center mt-4 mt-md-5">
                        <ButtonLink text="View more" link="/" classname="btn-link btn-link-s1"></ButtonLink>
                    </div>-->
      </div><!-- .container -->
    </section><!-- app-section -->
    <!-- Community Content  -->
    <section class="section-space content-section bg-gray">
      <div class="container">
        <!-- section heading -->
        <SectionHeading classname="text-center" content="Numerai educational content created by the community."
                        isMargin="mb-3"
                        text="Community Content"></SectionHeading>
        <!-- product -->
        <div class="row g-gs">
          <div v-for="content in contents" :key="content.id" class="col-xl-4 col-lg-4 col-sm-6">
            <div class="card card-full card-blog">
              <div class="d-block card-image">
                <img :src="content.img" alt="" class="card-img-top">
                <div class="bg-dark-transparent card-overlay">
                  <div class="d-flex align-items-center card-author">
                    <div class="flex-shrink-0 avatar avatar-2">
                      <img :src="content.avatar" alt="" class="rounded-circle">
                    </div>
                    <div class="flex-grow-1 ms-2 text-white">
                      <span>{{ content.author }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-body card-body-s1">
                <h4 class="card-title mb-3">{{ content.title }}</h4>
                <p class="card-text">{{ content.desc }}</p>
              </div><!-- end card-body -->
              <a :href="content.link" class="details" target="_blank">
              </a>
            </div><!-- end card -->
          </div>
        </div>
      </div><!-- .container -->
    </section><!-- content-section -->
    <!-- Newsletter  -->
    <Newsletter></Newsletter>
  </div><!-- end page-wrap -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';

import Category from "@/components/section/Category";
import HeroSeven from '@/components/section/HeroSeven';
import Newsletter from "@/components/section/Newsletter";

export default {
  name: 'Home',
  components: {
    Category,
    HeroSeven,
    Newsletter
  },
  data() {
    return {
      apps: [
        {
          id: 0,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651291135/dashboard-ceunen_rlx2g1.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/ceunen/90/606_2.png',
          title: 'Numerai Payouts Dashboard',
          desc: 'See how well your Numerai model is doing compared to everyone',
          author: '@ceunen',
          link: 'https://dashboard.numeraipayouts.com/'
        },
        {
          id: 1,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651292606/dashboard-james-g9_bsa9h1.webp',
          avatar: 'https://res.cloudinary.com/numerbay/image/upload/v1651292377/avatar-james-g9_du1lef.webp',
          title: 'Numerai Insights Dashboard',
          desc: 'Compare the performance of all your models side by side',
          author: '@james.g9',
          link: 'https://www.numerai-insights.com/'
        },
        {
          id: 2,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651290239/dashboard-qe_okmvcb.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/qeintelligence/90/915_2.png',
          title: 'Power BI Numerai Dashboard',
          desc: 'Numerai leaderboard, round performances, payouts and more',
          author: '@QE',
          link: 'https://app.powerbi.com/view?r=eyJrIjoiYTI4N2FkY2YtYTliYy00ZjQ5LWE2NjMtMTBjOTkwYTg2NDE2IiwidCI6Ijg3ZDc2ZDQ2LWYxZmYtNDkzMi05MGNiLTUyNzY3Yzg2OTk2ZiIsImMiOjl9'
        },
        {
          id: 3,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651293432/dashboard-yifanxie_rlmmpr.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/yxbot/90/979_2.png',
          title: 'Numerai Streamlit Dashboard',
          desc: 'Portfolio performance, trend tracking and comparison',
          author: '@yifanxie',
          link: 'https://share.streamlit.io/yifanxie/numerdash/main/numerdash_app.py'
        },
        {
          id: 4,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651997905/dashboard-aventurine_orsa68.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/aventurine/90/790_2.png',
          title: 'Numerai Dune Dashboard',
          desc: 'Dune Dashboard for NMR and NFTee\'s',
          author: '@Aventurine',
          link: 'https://dune.com/aventurine/NumeraiNMR'
        },
        {
          id: 5,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1656766465/dashboard-quantized_u4fpgx.webp',
          avatar: 'https://res.cloudinary.com/numerbay/image/upload/v1656766000/avatar-quantized_us7fda.svg',
          title: 'Numerai Earnings Dashboard',
          desc: 'Calculate earnings in fiat equivalent',
          author: '@quantized',
          link: 'https://numerai-earnings.herokuapp.com/'
        },
        {
          id: 6,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651305377/plugin-wigglemuse_nlu8qy.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/wigglemuse/90/593_2.png',
          title: 'USD Payout Plugin',
          desc: 'Browser plugin for displaying Numerai payout in USD',
          author: '@wigglemuse',
          link: 'https://forum.numer.ai/t/payouts-as-usd-unofficial-improvement-implemented/5074'
        },
        {
          id: 7,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651307200/lib-opensignals-jrdi_qxwzy1.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/jrdi/240/1067_2.png',
          title: 'Open Signals',
          desc: 'Library to enable quick development for the Signals tournament',
          author: '@jrdi',
          link: 'https://github.com/councilofelders/opensignals'
        },
        {
          id: 8,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651313166/lib-numerblox-crowdcent_fkpvqp.webp',
          avatar: 'https://res.cloudinary.com/numerbay/image/upload/v1651312887/avatar-crowdcent_bbmydw.webp',
          title: 'NumerBlox',
          desc: 'A pipeline library to help you focus on building Numerai models',
          author: '@crowdcent',
          link: 'https://crowdcent.github.io/numerblox/'
        }
      ],
      contents: [
        {
          id: 0,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651296941/video-ohwa_ztdelk.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/arbitrage/90/1054_2.png',
          title: 'Office Hours with Arbitrage',
          desc: 'YouTube playlist of the Office Hours with Arbitrage series',
          author: '@arbitrage',
          link: 'https://www.youtube.com/watch?v=QbxT_0WbJuM&list=PLz3D6SeXhT3vi9gRLCQLNuYs8aAROGtgV&ab_channel=Numerai'
        },
        {
          id: 1,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651304151/video-nsp_mqfhvy.webp',
          avatar: 'https://yt3.ggpht.com/ytc/AKedOLTnUTZLjYX3WJCe6oKsCE9chRUtpz77YIgbtoLO=s68-c-k-c0x00ffffff-no-rj',
          title: 'Numerai Starter Pack',
          desc: 'YouTube playlist of the Numerai Starter Pack series',
          author: '@StudyM8',
          link: 'https://www.youtube.com/watch?v=YeEpOm5JjFk&list=PLlOOibxKpQUlM28lqa4TiUTJ5gjLG5haQ&ab_channel=StudyM8'
        },
        {
          id: 2,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651306488/video-swr_obxmu1.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/liz/90/1103_2.png',
          title: 'Signals with R',
          desc: 'YouTube archive of the Signals with R series',
          author: '@liz',
          link: 'https://www.youtube.com/channel/UCGrwtxQ9LFMYLlz6MEjuQ5g'
        },
        {
          id: 3,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651308175/article-gosuto-lending_akxcra.webp',
          avatar: 'https://miro.medium.com/fit/c/96/96/1*_hdQwgAjwEp64xgeIyX7Mg.png',
          title: 'Kashi NMR Lending',
          desc: 'Tutorial to earn APR without staking on a model',
          author: '@gosuto',
          link: 'https://gosuto.medium.com/kashi-nmr-lending-earn-apr-without-staking-on-a-model-108c49bc464d'
        },
        {
          id: 4,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651308537/article-gosuto-borrowing_wbtjah.webp',
          avatar: 'https://miro.medium.com/fit/c/96/96/1*_hdQwgAjwEp64xgeIyX7Mg.png',
          title: 'Kashi NMR Borrowing',
          desc: 'Tutorial to stake on your model without NMR price exposure',
          author: '@gosuto',
          link: 'https://gosuto.medium.com/kashi-nmr-borrowing-stake-on-your-model-without-nmr-price-exposure-bc687fcacd9f'
        },
        {
          id: 5,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651312657/newsletter-coe_ioyxln.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/aventurine/90/790_2.png',
          title: 'The CoE Numerai Newsletter',
          desc: 'A monthly newsletter for all Numerai participants',
          author: '@Aventurine',
          link: 'https://coenumerainewsletter.substack.com/'
        },
        {
          id: 6,
          img: 'https://res.cloudinary.com/numerbay/image/upload/v1651997154/resource-uuazed_xymyh0.webp',
          avatar: 'https://forum.numer.ai/user_avatar/forum.numer.ai/uuazed/90/1229_2.png',
          title: 'Awesome Numerai',
          desc: 'A curated list of awesome numerai libraries, tutorials and other resources',
          author: '@uuazed',
          link: 'https://github.com/uuazed/awesome-numerai'
        }
      ],
      SectionData
    };
  }
};
</script>

<style lang="css" scoped>
.details {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.author-link {
  z-index: 2;
  position: relative;
}
</style>
