<template>
  <router-link :to="details_href">
    <b-list-group-item>{{text}}</b-list-group-item>
  </router-link>
</template>

<script>
    export default {
        name: "vote-list-item",
        props: ['vote'],
        computed: {
          text: function() {
            var candidates = this.vote.candidates
            return `${candidates[0]} vs ${candidates[1]}`
          },
          details_href: function () {
            return `contract/${this.vote.address}`
          }
        }
    }
</script>

<style scoped>

</style>
