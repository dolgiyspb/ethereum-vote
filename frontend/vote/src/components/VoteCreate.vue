<template>
  <b-container>
    <b-jumbotron header="Новое голосование" lead="Введите имена кандидатов и свой приватный ключ. После нажатия кнопки 'Создать' будет создан новый контракт в сети Ethereum.">
      <b-row v-for="name in ['first_candidate', 'second_candidate']" :key="name">
        <b-col sm="3"><label :for="name">Первый кандидат</label></b-col>
        <b-col sm="9">
          <b-form-input :id="name" :name="name" type="text" v-model="data[name]"" placeholder="Иван Иванович" />
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="3"><label for="key">Приватный ключ</label></b-col>
        <b-col sm="9">
          <b-form-input id="key" v-validate="'required'" type="text" v-model="data.key" placeholder="0000000000000000000000000000000000000000000000000000000000000000"></b-form-input>
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="5"></b-col>
        <b-col sm="2"><b-button variant="primary" @click="create">Создать</b-button></b-col>
        <b-col sm="5"></b-col>
      </b-row>
    </b-jumbotron>
    <b-modal ref="successConfiramtion" hide-footer title="Голосование создано" size="lg">
      <div class="d-block text-center">
        <h3>Создано новое голосование!</h3>
        <b-container>
          <b-row>
            <b-col sm="3">Адрес контракта:</b-col><b-col sm="9">{{data.address}}</b-col>
          </b-row>
          <b-row>
            <b-col sm="3">Хэш транзакции:</b-col><b-col sm="9">{{data.tx_hash}}</b-col>
          </b-row>
        </b-container>
      </div>
      <b-btn class="mt-3" variant="outline-danger" block @click="hideModal">Перейти к голосованию</b-btn>
    </b-modal>
  </b-container>

</template>

<script>
  export default {
    name: 'VoteCreate',
    data() {
      return {
        data: {
          first_candidate: '',
          second_candidate: '',
          key: '',
          address: '',
          tx_hash: ''
        }
      }
    },
    methods: {
      create: function () {
        this.$http.post(
          'votes', {'names': [this.data.first_candidate, this.data.second_candidate], 'key': this.data.key}
        ).then(result => {
          console.log(result)
          this.data.address = result.data.address
          this.data.tx_hash = result.data.tx_hash
          this.showModal()
        }, result => {
          console.log(`Error: ${result}`)
        })
      },
      showModal () {
        this.$refs.successConfiramtion.show()
      },
      hideModal () {
        this.$refs.successConfiramtion.hide()
        this.$router.push({ name: 'VoteDetails', params: { address: this.data.address }})
      }
    }
  }
</script>

<style scoped>
  .row {
    margin-bottom: 10px;
  }
</style>
