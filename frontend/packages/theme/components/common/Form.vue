<template>
  <form action="#">
    <div class="row g-gs">
      <div class="col-lg-6">
        <div class="form-floating">
          <input id="floatingInputName" class="form-control" placeholder="Name" type="text">
          <label for="floatingInputName">Name</label>
        </div>
      </div><!-- end col -->
      <div class="col-lg-6">
        <div class="form-floating">
          <input id="floatingInputEmail" class="form-control" placeholder="name@example.com" type="email">
          <label for="floatingInputEmail">Email</label>
        </div>
      </div><!-- end col -->
      <div class="col-lg-12">
        <div class="form-floating">
          <textarea id="floatingTextarea" class="form-control" placeholder="Leave a comment here"></textarea>
          <label for="floatingTextarea">Comments</label>
        </div>
      </div><!-- end col -->
      <div class="col-lg-12">
        <button class="btn btn-dark" type="submit">Post Comment</button>
      </div><!-- end col -->
    </div><!-- end row -->
  </form>
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'

export default {
  name: 'Form',
  data() {
    return {
      SectionData
    }
  }
}
</script>
