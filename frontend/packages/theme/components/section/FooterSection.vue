<template>
  <div class="container">
    <div class="section-space-sm">
      <div class="row">
        <div class="col-lg-3 col-md-9 me-auto">
          <div class="footer-item mb-5 mb-lg-0">
            <!-- logo link -->
            <LogoLink class="footer-logo-link"></LogoLink>
            <p class="my-4 footer-para">The Numerai community marketplace funded by the Numerai Council of Elders.</p>
            <ul class="styled-icon">
              <li><a href="https://twitter.com/NumeraiCoE" target="_blank"><em class="icon ni ni-twitter"></em></a></li>
            </ul>
          </div><!-- end footer-item -->
        </div><!-- end col-lg-3 -->
        <div class="col-lg-8">
          <div class="row g-gs">
            <div class="col-lg-4 col-md-4 col-sm-4">
              <div class="footer-item">
                <h5 class="mb-4">Marketplace</h5>
                <ul class="list-item list-item-s1">
                  <li>
                    <router-link to="/explore/numerai">Numerai</router-link>
                  </li>
                  <li>
                    <router-link to="/explore/signals">Signals</router-link>
                  </li>
                  <li>
                    <router-link to="/explore/onlyfams">OnlyFams</router-link>
                  </li>
                  <li><a href="https://docs.numerbay.ai/" target="_blank">Docs</a></li>
                </ul>
              </div><!-- end footer-item -->
            </div><!-- end col -->
            <div class="col-lg-4 col-md-4 col-sm-4">
              <div class="footer-item">
                <h5 class="mb-4">My Account</h5>
                <ul class="list-item list-item-s1">
                  <li>
                    <router-link to="/account">Profile</router-link>
                  </li>
                  <li>
                    <router-link to="/purchases">Purchases</router-link>
                  </li>
                  <li>
                    <router-link to="/sales">Sales</router-link>
                  </li>
                  <li>
                    <router-link to="/listings">My Listings</router-link>
                  </li>
                  <li>
                    <router-link to="/numerai-settings">Numerai Settings</router-link>
                  </li>
                </ul>
              </div><!-- end footer-item -->
            </div><!-- end col -->
            <div class="col-lg-4 col-md-4 col-sm-4">
              <div class="footer-item">
                <h5 class="mb-4">Official Numerai</h5>
                <ul class="list-item list-item-s1">
                  <li><a href="https://numer.ai/" target="_blank">Numerai</a></li>
                  <li><a href="https://signals.numer.ai/" target="_blank">Signals</a></li>
                  <li><a href="https://forum.numer.ai/" target="_blank">Forum</a></li>
                  <li><a href="https://rocketchat.numer.ai/" target="_blank">RocketChat</a></li>
                </ul>
              </div><!-- end footer-item -->
            </div><!-- end col -->
          </div>
        </div>
      </div><!-- end row -->
    </div>
    <hr class="bg-white-slim my-0">
    <div class="copyright-wrap d-flex flex-wrap py-3 align-items-center justify-content-between">
      <p class="footer-copy-text py-2">Logo: <a href="https://numer.ai/" target="_blank">Numerai</a>, 2022. Maintained
        by the Numerai Community.</p>
      <ul class="list-item list-item-s1 list-item-inline">
        <li>
          <router-link to="/explore/numerai">Explore</router-link>
        </li>
        <li>
          <router-link to="/account">Account</router-link>
        </li>
      </ul>
    </div><!-- end d-flex -->
  </div><!-- .container -->
</template>
<script>
export default {
  name: 'FooterSection'
};
</script>
