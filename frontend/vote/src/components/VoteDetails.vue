<template>
  <b-container class="bv-example-row">
    <b-jumbotron :header="header" lead="Bootstrap 4 Components for Vue.js 2" >
      <p>For more information visit website</p>
      <b-btn variant="primary" href="#">More Info</b-btn>
    </b-jumbotron>
  </b-container>
</template>

<script>
    export default {
        name: "VoteDetails",
        data: function () {
          return {
            "results": [
              {
                "name": "c1",
                "votes": 0
              },
              {
                "name": "c2",
                "votes": 0
              },
              {
                "name": "against_all",
                "votes": 0
              }
            ],
            "owner": "0x844Fbe41E055c9129dF7dF9e15ca276B2d6C5ee1",
            "closed": false
          }
        },
        computed: {
          header: function () {
            var results = this.results
            return `${results[0]['name']} VS ${results[1]['name']}`
          }
        }
    }
</script>

<style scoped>

</style>
