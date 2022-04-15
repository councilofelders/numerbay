<template>
  <div class="wrapper">
    <div class="row mb-2">
      <div class="col-10"><h4>{{ question }}</h4></div>
      <div class="col-2"><span class="spinner-border spinner-border-sm text-primary float-end" role="status"
                               v-if="loading"></span></div>
    </div>
    <div class="item-detail-meta d-flex flex-wrap align-items-center mb-3">
      <span class="item-detail-text-meta">By <span class="text-primary fw-semibold">{{ owner }}</span></span>
      <span class="dot-separeted"></span>
      <span class="item-detail-text-meta">Ends <span class="text-primary fw-semibold">{{ deadline }}</span></span>
      <span class="dot-separeted"></span>
      <span class="item-detail-text-meta">Weight <span class="text-primary fw-semibold">{{ weightMode }}</span></span>
      <div v-if="!canShowResults">
        <span class="item-detail-text-meta">Results to be shown after poll ends</span>
      </div>
    </div>
    <div class="row mb-2" v-if="Boolean(description)">
      <div class="col-12">{{ description }}</div>
    </div>
    <div class="poll-area">
      <div v-for="(a,index) in calcAnswers" :key="index">
        <input :type="multiple ? `checkbox` : `radio`" name="poll" :id="`opt-${index}`" @click.prevent="handleVote(a)">
        <label :for="`opt-${index}`" :class="[(a.selected ? 'selected' : ''), (visibleResults ? 'selectall' : '')]">
              <span class="poll-row">
                  <span class="poll-column">
                      <span class="circle"></span>
                      <span class="text">{{ a.text }}</span>
                  </span>
                  <span class="percent" v-if="canShowResults">{{ getPercent(a) }}%</span>
              </span>
          <div class="progress" :style='`--w:${getPercent(a)};`' v-if="canShowResults"></div>
        </label>
      </div>
    </div>
    <transition name="fade">
      <div class="text-center mt-4" v-if="multiple && canSubmit && totalSelections > 0">
        <button type="button" class="btn btn-outline-dark" @click.prevent="handleMultiple">{{
            submitButtonText
          }}
        </button>
      </div>
    </transition>
  </div>
</template>

<script>

export default {
  name: 'Poll',
  props: {
    owner: {
      type: String,
      required: false,
      default: '-'
    },
    deadline: {
      type: String,
      required: false,
      default: '-'
    },
    weightMode: {
      type: String,
      required: false,
      default: '-'
    },
    question: {
      type: String,
      required: false,
      default: 'Poll'
    },
    description: {
      type: String,
      required: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    answers: {
      type: Array,
      required: true
    },
    canShowResults: {
      type: Boolean,
      default: true
    },
    showResults: {
      type: Boolean,
      default: false
    },
    showTotalVotes: {
      type: Boolean,
      default: true
    },
    finalResults: {
      type: Boolean,
      default: false
    },
    multiple: {
      type: Boolean,
      default: false
    },
    maxOptions: {
      type: Number,
      default: 1
    },
    submitButtonText: {
      type: String,
      default: 'Submit'
    },
    customId: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      visibleResults: JSON.parse(this.showResults)
    }
  },
  computed: {
    totalVotes() {
      let totalVotes = 0
      this.answers.filter(a => {
        if (!isNaN(a.votes) && a.votes > 0)
          totalVotes += Number(a.votes)
      })
      return totalVotes
    },
    totalVotesFormatted() {
      return this.totalVotes.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    mostVotes() {
      let max = 0
      this.answers.filter(a => {
        if (!isNaN(a.votes) && a.votes > 0 && a.votes >= max)
          max = a.votes
      })

      return max
    },
    calcAnswers() {

      if (this.totalVotes === 0)
        return this.answers.map(a => {
          a.percent = '0%'
          return a
        })

      //Calculate percent
      return this.answers.filter(a => {
        if (!isNaN(a.votes) && a.votes > 0)
          a.percent = (Math.round((Number(a.votes) / this.totalVotes) * 100)) + '%'
        else
          a.percent = '0%'

        return a
      })
    },
    totalSelections() {
      return this.calcAnswers.filter(a => a.selected).length
    },
    canSubmit() {
      return (!this.finalResults && !this.visibleResults);
    }
  },
  methods: {
    getPercent(a) {
      return Math.round((Number(a.votes) / this.totalVotes) * 100) || 0;
    },
    handleMultiple() {

      let arSelected = []
      this.calcAnswers.filter(a => {
        if (a.selected) {
          a.votes++
          arSelected.push({value: a.value, votes: a.votes})
        }
      })

      this.visibleResults = true

      let obj = {arSelected: arSelected, totalVotes: this.totalVotes}

      if (this.customId)
        obj.customId = this.customId

      this.$emit('addvote', obj)
    },
    handleVote(a) { //Callback
      if (!this.canSubmit) {
        return;
      }

      if (this.multiple) {
        if (!a.selected && this.calcAnswers.filter(a => a.selected)?.length >= this.maxOptions) {
          console.log("Max votes reached")
          return
        }

        if (a.selected === undefined)
          console.log("Please add 'selected: false' on the answer object")

        a.selected = !a.selected
        return
      }

      a.votes++
      a.selected = true
      this.visibleResults = true

      let obj = {value: a.value, votes: a.votes, totalVotes: this.totalVotes}

      if (this.customId)
        obj.customId = this.customId

      this.$emit('addvote', obj)
    }
  }
}
</script>

<style lang="scss" scoped>
::selection {
  color: #fff;
  background: var(--bs-primary);
}

.wrapper {
  //border-radius: 15px;
  //padding: 25px;
  width: 100%;
  box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(28, 43, 70, 0.05);
  padding: 15px;
  border-radius: 6px;
}

.dark-mode .wrapper {
  border-color: #202020;
}

.wrapper header {
  font-size: 22px;
  font-weight: 600;
}

.wrapper .poll-area {
  margin: 20px 0 15px 0;
}

.poll-area label {
  display: block;
  margin-bottom: 10px;
  border-radius: 5px;
  padding: 8px 15px;
  border: 2px solid var(--vs-state-disabled-bg);
  transition: all 0.2s ease;
}

.poll-area label:hover {
  border-color: #ddd;
}

label.selected {
  border-color: var(--bs-primary) !important;
}

label .poll-row {
  display: flex;
  pointer-events: none;
  justify-content: space-between;
}

label .poll-row .poll-column {
  display: flex;
  align-items: center;
}

label .poll-row .circle {
  min-width: 19px;
  height: 19px;
  width: 19px;
  display: block;
  border: 2px solid #ccc;
  border-radius: 50%;
  margin-right: 10px;
  position: relative;
}

label.selected .poll-row .circle {
  border-color: var(--bs-primary);
}

label .poll-row .circle::after {
  content: "";
  height: 11px;
  width: 11px;
  background: var(--bs-primary);
  border-radius: inherit;
  position: absolute;
  left: 2px;
  top: 2px;
  display: none;
}

.poll-area label:hover .poll-row .circle::after {
  display: block;
  background: var(--vs-state-disabled-bg);
}

label.selected .poll-row .circle::after {
  display: block;
  background: var(--bs-primary) !important;
}

label .poll-row span {
  font-size: 16px;
  font-weight: 500;
}

label .poll-row .percent {
  display: none;
}

label .progress {
  height: 7px;
  width: 100%;
  position: relative;
  background: #f0f0f0;
  margin: 8px 0 3px 0;
  border-radius: 30px;
  display: none;
  pointer-events: none;
}

label .progress:after {
  position: absolute;
  content: "";
  height: 100%;
  background: #ccc;
  width: calc(1% * var(--w));
  border-radius: inherit;
  transition: all 0.2s ease;
}

label.selected .progress::after {
  background: var(--bs-primary);
}

label.selectall .progress,
label.selectall .poll-row .percent {
  display: block;
}

input[type="radio"],
input[type="checkbox"] {
  display: none;
}

.fade {
  &-enter-active,
  &-leave-active {
    transition: opacity 0.25s linear;
  }

  &-enter,
  &-leave,
  &-leave-to {
    opacity: 0;
  }
}
</style>
