<template>
    <div class="hero-wrap sub-header">
                <div class="overlay"></div>
                <div class="container">
                    <div class="hero-content py-0 d-flex align-items-center">
<!--                        <div class="avatar flex-shrink-0" :class="avatarSize">
                            <img :src="img" alt="">
                        </div>-->
                        <div class="author-hero-content-wrap d-flex flex-wrap justify-content-between ms-3 flex-grow-1">
                            <div class="author-hero-content me-3">
                                <h4 class="hero-author-title mb-1 text-white">{{ username }}</h4>
<!--                                <p class="hero-author-username mb-1 text-white">{{ username }}</p>-->
<!--                                <div class="d-flex align-items-center" v-if="isCopyInput">
                                    <input type="text" class="copy-input text-white" v-model="message" id="copy-input" readonly>
                                    <div class="tooltip-s1">
                                        <button v-clipboard:copy="message" v-clipboard:success="onCopy"  class="copy-text text-white ms-2" type="button">
                                            <span class="tooltip-s1-text tooltip-text">Copy</span>
                                            <em class="ni ni-copy"></em>
                                        </button>
                                    </div>
                                </div>-->
                            </div><!-- author-hero-conetent -->
<!--                            <div class="hero-action-wrap d-flex align-items-center my-2">
                                <router-link :to="btnlink" class="btn btn-light">{{ btntext }}</router-link>
                                <div class="dropdown ms-3" v-if="isDropdown">
                                    <a class="icon-btn icon-btn-s1" href="#" data-bs-toggle="dropdown" id="reportDropdown">
                                        <em class="ni ni-more-h"></em>
                                    </a>
                                    <ul class="dropdown-menu card-generic p-2 dropdown-menu-end mt-2 card-generic-sm" aria-labelledby="reportDropdown">
                                        <li><a class="dropdown-item card-generic-item" href="#" data-bs-toggle="modal" data-bs-target="#reportModal">Report Page</a></li>
                                    </ul>
                                </div>&lt;!&ndash; end dropdown &ndash;&gt;
                            </div>&lt;!&ndash;end hero-action-wrap &ndash;&gt;-->
                        </div><!-- author-hero-content -->
                    </div><!-- hero-content -->
                </div><!-- .container-->
    </div><!-- end hero-wrap -->
</template>

<script>
// Composables
import { computed } from '@vue/composition-api';
import { useUser } from '@vue-storefront/numerbay';

export default {
  name: 'AuthorHero',
  // props: ['img', 'avatarSize', 'title', 'username', 'isDropdown', 'btntext', 'isCopyInput', 'btnlink', 'coverimg'],
  // setup() {
  //   const message = '0x76669f...a0e9ca52';
  //   const onCopy = (e) => {
  //     const target = e.trigger.querySelector('.tooltip-text');
  //     const prevText = target.innerHTML;
  //     target.innerHTML = 'Copied';
  //     setTimeout(function() {
  //       target.innerHTML = prevText;
  //     }, 1000);
  //   };
  //   return { message, onCopy };
  // }
  setup() {
    const { user } = useUser();

    return {
      username: computed(() => user.value ? user.value.username : '')
    };
  }
};
</script>
