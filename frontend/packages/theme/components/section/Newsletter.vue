<template>
  <section class="subscibe-section section-space-sm">
    <div class="container">
        <div class="join-form-wrap">
            <form action="https://coenumerainewsletter.substack.com/api/v1/free?nojs=true" method="post">
                <div class="row g-gs align-items-center">
                    <input type="hidden" name="first_url" value="https://coenumerainewsletter.substack.com/">
                    <input type="hidden" name="current_url" value="https://coenumerainewsletter.substack.com/">
                    <input type="hidden" name="current_referrer">
                    <input type="hidden" name="referral_code">
                    <input type="hidden" name="source" value="cover_page">
                    <div class="col-lg-6">
                      <h3 class="form-title">Join the <a href="https://coenumerainewsletter.substack.com/" target="_blank">Numerai COE Newsletter</a></h3>
                    </div><!-- end col -->
                    <div class="col-lg-3 col-md-4">
                        <input class="form-control form-control-s1" type="text" name="email" placeholder="Enter email">
                    </div><!-- end col -->
                    <div class="col-lg-3 col-md-4">
                        <button type="submit" class="btn btn-dark d-md-block">Subscribe Now</button>
                    </div><!-- end col -->
                </div><!-- row -->
            </form>
        </div><!-- end join-form-wrap -->
    </div><!-- end container -->
    </section><!-- end subscibe-section -->
</template>

<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js';
export default {
  name: 'Newsletter',
  data () {
    return {
      SectionData
    };
  }
};
</script>
