<template>
  <section class="subscibe-section section-space-sm">
    <div class="container">
      <div class="join-form-wrap">
        <form action="https://coenumerainewsletter.substack.com/api/v1/free?nojs=true" method="post">
          <div class="row g-gs align-items-center">
            <input name="first_url" type="hidden" value="https://coenumerainewsletter.substack.com/">
            <input name="current_url" type="hidden" value="https://coenumerainewsletter.substack.com/">
            <input name="current_referrer" type="hidden">
            <input name="referral_code" type="hidden">
            <input name="source" type="hidden" value="cover_page">
            <div class="col-lg-6">
              <h3 class="form-title">Join the <a href="https://coenumerainewsletter.substack.com/" target="_blank">Numerai
                COE Newsletter</a></h3>
            </div><!-- end col -->
            <div class="col-lg-3 col-md-4">
              <input class="form-control form-control-s1" name="email" placeholder="Enter email" type="text">
            </div><!-- end col -->
            <div class="col-lg-3 col-md-4">
              <button class="btn btn-dark d-md-block" type="submit">Subscribe Now</button>
            </div><!-- end col -->
          </div><!-- row -->
        </form>
      </div><!-- end join-form-wrap -->
    </div><!-- end container -->
  </section><!-- end subscibe-section -->
</template>

<script>
export default {
  name: 'Newsletter'
};
</script>
