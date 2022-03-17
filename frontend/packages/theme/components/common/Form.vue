<template>
    <form action="#">
        <div class="row g-gs">
            <div class="col-lg-6">
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingInputName" placeholder="Name">
                    <label for="floatingInputName">Name</label>
                </div>
            </div><!-- end col -->
            <div class="col-lg-6">
                <div class="form-floating">
                    <input type="email" class="form-control" id="floatingInputEmail" placeholder="name@example.com">
                    <label for="floatingInputEmail">Email</label>
                </div>
            </div><!-- end col -->
            <div class="col-lg-12">
                <div class="form-floating">
                    <textarea class="form-control" placeholder="Leave a comment here" id="floatingTextarea"></textarea>
                    <label for="floatingTextarea">Comments</label>
                </div>
            </div><!-- end col -->
            <div class="col-lg-12">
                <button type="submit" class="btn btn-dark">Post Comment</button>
            </div><!-- end col -->
        </div><!-- end row -->
    </form>
</template>
<script>
// Import component data. You can change the data in the store to reflect in all component
import SectionData from '@/store/store.js'
export default {
  name: 'Form',
  data () {
    return {
      SectionData
    }
  }
}
</script>
