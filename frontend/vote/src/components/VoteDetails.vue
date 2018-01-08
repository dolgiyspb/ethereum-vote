<template>
  <b-container>
    <b-jumbotron :header="header" :lead="address" v-if="results">
      <p v-if="!closed">Для голосования введите свой приватный ключ и выберите один из трех вариантов</p>
      <p v-if="closed">Это голосование уже закрыто. Можно смотреть, но все уже решено.</p>
      <b-container v-if="!closed">
        <b-row>
          <b-col sm="3"><label for="key">Приватный ключ:</label></b-col>
          <b-col sm="9">
            <b-form-input
              id="key"
              v-model="key"
              type="text"
              placeholder="0000000000000000000000000000000000000000000000000000000000000000"
              v-validate="'private-key'"
              name="key"
              :state="!errors.has('key')"
              aria-describedby="keyError"
            />
            <b-form-invalid-feedback id="keyError">
              {{ errors.first('key') }}
            </b-form-invalid-feedback>
          </b-col>
        </b-row>
        <b-row>
          <b-col  v-for="(value, index) in variants" :key="value" sm="4">
            <b-button @click="vote_for(index)" variant="primary">{{value}}</b-button>
          </b-col>
        </b-row>
        <b-row>
        <b-btn @click="showCollapse = !showCollapse"
               :class="showCollapse ? 'collapsed' : null"
               aria-controls="collapse4"
               :aria-expanded="showCollapse ? 'true' : 'false'">
          Дополнительно
        </b-btn>

        </b-row>
        <b-row>
          <b-collapse class="mt-2" v-model="showCollapse" id="collapse4">
            <p>Если вы создали это голосование, то вы можете его закрыть.</p>
            <p>Для этого введите укажите свой приватный ключ и нажмите ниже.</p>
            <b-button @click="close_vote" variant="primary">Закрыть голосование</b-button>
          </b-collapse>
        </b-row>
      </b-container>
      <chartjs-bar :labels="variants" :data="chart_data":bind="true" datalabel="Количество голосов"></chartjs-bar>
      <b-link :to="{'name': 'VoteList'}">На главную</b-link>
    </b-jumbotron>
    <b-modal ref="successConfiramtion" hide-footer title="Голос учтен" size="lg">
      <div class="d-block text-center">
        <h3>Спасибо за участие!</h3>
        <b-container>
          <b-row>
            <b-col sm="3">Хэш транзакции:</b-col><b-col sm="9">{{last_tx_hash}}</b-col>
          </b-row>
        </b-container>
      </div>
      <b-btn class="mt-3" variant="outline-danger" block @click="hideModal">Закрыть</b-btn>
    </b-modal>
  </b-container>
</template>

<script>
  export default {
    name: 'VoteDetails',
    data: function () {
      return {
        results: [],
        owner: '',
        closed: false,
        key: '',
        last_tx_hash:'',
        showCollapse: false
      }
    },
    computed: {
      header: function () {
        const results = this.results
        if (results.length) return `${results[0]['name']} vs ${results[1]['name']}`
      },
      address: function() {
        return `Адрес контракта в сети Ethereum: ${this.$route.params.address}`
      },
      variants: function () {
        const results = this.results
        if (results.length) {
          return [results[0]['name'], results[1]['name'], 'Против всех']
        } else {
          return []
        }
      },
      chart_data: function () {
        return this.results.map((r) => r['votes'])
      }
    },
    methods: {
      _path: function () {
        return `votes/${this.$route.params.address}`;
      },
      _vote_for_path: function () {
        return `${this._path()}/vote-for`
      },
      fetch_data: function () {
        this.$http.get(this._path()).then(result => {
          let data = result.data
          this.results = data.results
          this.votes = data.votes
          this.owner = data.owner
          this.closed = data.closed
        }, error => {
          console.error(error)
        });
      },
      vote_for: function (index) {
        this.$http.post(
          this._vote_for_path(), {"candidate_index": index, "key": this.key}
        ).then(result => {
          this.last_tx_hash = result.data.tx_hash
          this.showModal()
          this.fetch_data()
        }, result => {
          console.log(`Error: ${result}`)
        })
      },
      close_vote() {
        this.$http.delete(
          this._path(), {body: JSON.stringify({key: this.key})}
        ).then(result => {
          this.fetch_data()
        }, result => {
          console.log(`Error: ${result}`)
        })
      },
      showModal () {
        this.$refs.successConfiramtion.show()
      },
      hideModal () {
        this.$refs.successConfiramtion.hide()
      }
    },

    created(){
      this.fetch_data()
      this.$validator.extend('private-key', {
        getMessage: field => 'Некорректный формат приватного ключа',
        validate: value => {
          if (value === '0000000000000000000000000000000000000000000000000000000000000000') return false
          let rex = /^[0-9A-F]{64}$/g
          return rex.test(value.toUpperCase())
        }
      })
    },

    watch: {
      '$route': 'fetchData'
    },
  }
</script>

<style scoped>
  .row {
    margin-bottom: 10px;
  }
</style>
