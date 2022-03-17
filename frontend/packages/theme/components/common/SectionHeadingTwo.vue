<template>
    <div class="section-head-md">
        <div class="row align-items-center">
            <div class="col-md-6 mb-3 mb-md-0">
                <h6 class="mb-2 section-meta text-uppercase text-primary">{{ meta }}</h6>
                <h2 v-html="text"></h2>
            </div><!-- end col -->
            <div class="col-md-6">
                <p>{{ content }}</p>
            </div><!-- end col -->
        </div><!-- end row -->
    </div><!-- end section-head -->
</template>
<script>

export default {
  name: 'SectionHeadingTwo',
  props: ['text', 'content', 'isMargin', 'meta']
}
</script>
