<template>
  <b-jumbotron>
    <template slot="header">
      Голосования на платформе Ethereum
    </template>

    <b-card-group deck>
      <b-card header="<b>Открытые голосования</b>">
        <b-list-group  v-for="vote in opened" :key="vote.address">
          <vote-list-item v-bind:vote="vote"></vote-list-item>
        </b-list-group>
        <p class="card-text mt-2" v-if="opened.length">
          Это открытые голования, представляющие собой контракты, расположеные в блокчейне Ethereum.
          Вы можете принять участие в любом голосовании, используя приватный ключ своего аккаунта в сети Ethereum.
        </p>
        <p class="card-text mt-2" v-else>
          Здесь пока ничего нет. Можете подождать пока повится какое-нибудь голосование.
        </p>
        <p class="card-text mt-2">
          Ну или  <b-button variant="primary">Создать новое</b-button>
        </p>
      </b-card>
      <b-card header="<b>Закрытые голосования</b>">
        <b-list-group v-for="vote in closed" :key="vote.address">
          <vote-list-item v-bind:vote="vote"></vote-list-item>
        </b-list-group>
        <p class="card-text mt-2" v-if="closed.length">
          Эти голосования уже завершены. Можно только ознакомиться с результатами.
        </p>
        <p class="card-text mt-2" v-else>
          Здесь пока ничего нет. Но это временно.
        </p>
      </b-card>
    </b-card-group>
  </b-jumbotron>
</template>

<script>
  import VoteListItem from '@/components/VoteListItem.vue'
  export default {
    name: 'VoteList',
    components:{VoteListItem},
    data () {
      return {
        votes: [
          {
            "address": "0x2a0b01E02e10BE9a277A10BF4c50b541C889B45D",
            "candidates": [
              "c1",
              "c2"
            ],
            "closed": false
          }
        ],
      }
    },
    mounted() {
      this.$http.get("votes").then(result => {
        console.log(result)
        this.votes = result.data
      }, error => {
        console.error(error);
      });
    },
    computed: {
      opened: function() {
        return this.votes.filter(function (v) {
          return !v.closed
        })
      },
      closed: function() {
        return this.votes.filter(function (v) {
          return v.closed
        })
      }
    }
  }
</script>
