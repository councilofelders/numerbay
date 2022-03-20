<template>
  <div ref="range" type="range" class="range-slider" :disabled="disabled">
    <slot v-bind="$attrs" />
  </div>
</template>
<script>
import noUiSlider from "nouislider";
import "nouislider/dist/nouislider.css";
export default {
  name: "Range",
  props: {
    value: {
      type: Array,
      default: () => [0, 1],
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    config: {
      type: Object,
      default: () => {
        return {
          start: [0, 1],
          range: {
            min: 0,
            max: 10,
          },
          step: 1,
        };
      },
    },
  },
  watch: {
    config: {
      handler(newConfig) {
        if (this.$refs && this.$refs.range && this.$refs.range.noUiSlider) {
          this.$refs.range.noUiSlider.destroy();
          const newSlider = this.noUiSliderInit(newConfig);
          return newSlider;
        }
      },
      deep: true,
    },
    value: {
      handler(values) {
        if (this.$refs && this.$refs.range && this.$refs.range.noUiSlider) {
          return this.$refs.range.noUiSlider.set(values);
        }
      },
      immediate: true,
    },
  },
  mounted() {
    this.noUiSliderInit(this.config);
  },
  beforeDestroy() {
    if (this.$refs && this.$refs.range && this.$refs.range.noUiSlider) {
      this.$refs.range.noUiSlider.destroy();
    }
  },
  methods: {
    noUiSliderInit(config) {
      const configSettings = Object.assign(this.config, config);
      noUiSlider
        .create(this.$refs.range, configSettings)
        .on("change", (values) => {
          this.$emit("change", values);
        });
    },
  },
};
</script>
<style lang="scss">
.range-slider {
  position: relative;
  width: 90%;
  height: 7px;
  margin: 1rem;
  background-color: #dee2e6;
  border: none;
  box-shadow: none;
  .noUi {
    &-handle {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      transform: translate3d(0, -20%, 0);
      box-shadow: none;
      //@include border(--range-handle-border, 1px, solid, var(--c-primary));
      background-color: #ffffff;
      &::before,
      &::after {
        display: none;
      }
      &:focus {
        outline: none;
      }
      &.noUi-active .noUi-touch-area {
        background-color: #7952b3;
      }
    }
    &-connect {
      background-color: #7952b3;
    }
    &-touch-area {
      background-color: #ffffff;
      border-radius: 50%;
      //&:hover {
      //  background-color: #7952b3;
      //}
    }
    &-tooltip {
      bottom: -200%;
      color: #8091a7;
      //@include font(
      //  --range-tooltip-font,
      //  var(--font-weight--normal),
      //  var(--font-size--xs),
      //  1.2,
      //  (--font-family--secondary)
      //);
      //@include border(--range-tooltip-border, 0, none, var(--c-primary));
    }
  }
  &[disabled="disabled"] {
    .noUi {
      &-handle {
        border-color: #6c757d;
      }
      &-connect {
        background-color: #6c757d;
      }
      &-touch-area:hover {
        background-color: #f8f9fa;
      }
      &-tooltip {
        display: none;
      }
    }
  }
}
.noUi-vertical {
  height: 300px;
  width: 7px;
  .noUi-handle {
    transform: translate3d(20%, 0, 0);
  }
}
</style>
