<template>
  <client-only>
    <div>
      <v-date-picker
        v-model="calendarData"
        :limits="{min: minDate, max: maxDate}"
        :isMultipleDatePicker="isMultipleDatePicker"
        :disabled-day-names="disabledDayNames"
        :is-dark="isDark"
        @choseDay="onDateChosen"
      ></v-date-picker>
    </div>
  </client-only>
</template>
<script>
import moment from 'moment';

export default {
  name: "MultipleDatePicker",
  props: {
    isMultipleDatePicker: {
      type: Boolean,
      default: () => true
    },
    isDark: {
      type: Boolean,
      default: () => false
    },
    disabledDayNames: {
      type: Array,
      default: () => ['Su', 'Mo']
    },
    minDate: {
      type: String,
      default: () => moment.utc().format("DD/MM/YYYY")
    },
    maxDate: {
      type: String,
      default: () => moment.utc().add(10, 'weeks').format("DD/MM/YYYY")
    }
  },
  data() {
    return {
      calendarData: {},
    };
  },
  computed: {
    attributes() {
      return this.dates.map(date => ({
        highlight: true,
        dates: date,
      }));
    },
  },
  methods: {
    onDateChosen(dates) {
      this.$emit("change", this.calendarData)
    },
  },
};
</script>
<style lang="scss">
.vfc-week .vfc-day span.vfc-span-day.vfc-today {
    background-color: inherit;
    color: inherit;
}
.vfc-week .vfc-day span.vfc-span-day.vfc-marked {
      background-color: #66b3cc;
    }
</style>
