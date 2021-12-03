<template>
  <div>
    <!--<div
      v-if="reviewSent && !error.addReview"
    >
      <p>Your review was submitted!</p>
    </div>
    <div
      v-else-if="error.addReview"
    >
      <p>{{ error.addReview }}</p>
    </div>-->
    <ValidationObserver
      v-slot="{ handleSubmit, reset }"
    >
      <form
        id="billing-details-form"
        class="form"
        @submit.prevent="handleSubmit(submitForm(reset))"
      >
        <div class="form__horizontal">
          <star-rating name="rating" active-color="#5ece7b" :star-size="25" v-model="form.ratings[0]"/>
        </div>
        <div class="form__horizontal">
          <div class="editor">
            <quill-editor
              ref="reviewEditor"
              name="review"
              v-model="form.text"
              :options="editorOption"
            />
          </div>
        </div>
        <SfButton class="form__button" :disabled="!form.ratings[0]">
          Add review
        </SfButton>
      </form>
    </ValidationObserver>
  </div>
</template>
<script>
import {
  defineComponent,
  ref,
  // onBeforeMount,
  computed
} from '@vue/composition-api';
import {
  reviewGetters, useReview
} from '@vue-storefront/numerbay';
import { ValidationObserver, ValidationProvider } from 'vee-validate';
import {
  SfButton
} from '@storefront-ui/vue';
import { useVueRouter } from '~/helpers/hooks/useVueRouter';

const BASE_FORM = (id) => ({
  // nickname: '',
  ratings: {},
  productId: id,
  // summary: '',
  text: ''
});

export default defineComponent({
  name: 'ProductAddReview',
  components: {
    SfButton,
    ValidationProvider,
    ValidationObserver
  },
  data () {
    return {
      editorOption: {
        theme: 'snow',
        modules: {
          toolbar: {
            container: [
              ['bold', 'italic', 'underline', 'strike'],
              ['blockquote', 'code-block'],
              [{ list: 'ordered' }, { list: 'bullet' }],
              [{ indent: '-1' }, { indent: '+1' }],
              [{ header: [1, 2, 3, 4, 5, 6, false] }],
              [{ color: [] }, { background: [] }],
              [{ font: [] }],
              ['link']
            ]
          }
        },
        placeholder: 'Review your most recent order'
      }
    };
  },
  emits: ['add-review'],
  setup(_, { emit }) {
    const { route } = useVueRouter();
    const { id } = route.params;
    const {
      loading,
      // loadReviewMetadata,
      // metadata,
      error
    } = useReview(`productReviews-${id}`);
    // const { isAuthenticated, user } = useUser();
    const reviewSent = ref(false);
    const form = ref(BASE_FORM(id));
    // const ratingMetadata = computed(() => reviewGetters.getReviewMetadata([...metadata.value]));
    const formSubmitValue = computed(() => {
      // const nickname = isAuthenticated.value
      //   ? userGetters.getFullName(user.value)
      //   : form.value.nickname;
      const ratings = Object.keys(form.value.ratings).map((key) => ({
        id: key,
        // eslint-disable-next-line camelcase
        value_id: `${form.value.ratings[key]}`
      }));
      return {
        ...form.value,
        // nickname,
        ratings
      };
    });
    const submitForm = (reset) => () => {
      if (!(
        formSubmitValue.value.ratings[0].value_id ||
        formSubmitValue.value.ratings[0].id ||
        // formSubmitValue.value.nickname ||
        // formSubmitValue.value.summary ||
        formSubmitValue.value.productId ||
        formSubmitValue.value.text
      )) return;
      try {
        reviewSent.value = true;
        emit('add-review', formSubmitValue.value);
        reset();
      } catch {
        reviewSent.value = false;
      }
    };
    // onBeforeMount(async () => {
    //   await loadReviewMetadata();
    // });
    return {
      error,
      form,
      formSubmitValue,
      // isAuthenticated,
      loading,
      // ratingMetadata,
      reviewGetters,
      reviewSent,
      submitForm
    };
  }
});
</script>

<style lang='scss' scoped>
.form {
  &__element {
    display: block;
    margin-bottom: var(--spacer-base);
  }
  &__select {
    display: flex;
    align-items: center;
    --select-option-font-size: var(--font-size--lg);
    flex-wrap: wrap;
    ::v-deep .sf-select__dropdown {
      font-size: var(--font-size--lg);
      // margin: 0;
      font-family: var(--font-family--secondary);
      font-weight: var(--font-weight--normal);
    }
  }
  &__button {
    display: block;
    margin-top: var(--spacer-md);
  }
  &__horizontal {
    @include for-desktop {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }
    .form__element {
      @include for-desktop {
        flex: 1;
        margin-right: var(--spacer-lg);
      }
      &:last-child {
        margin-right: 0;
        margin-bottom: 0;
      }
    }
  }
}
.editor {
  margin: 0 0 var(--spacer-xl) 0;
  width: 100%;
  height: 300px;
  .quill-editor {
    height: 250px;
  }
  @include for-mobile {
    margin: 0 0 var(--spacer-2xl) 0;
  }
}
</style>
