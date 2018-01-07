<template>
  <b-jumbotron>
    <template slot="header">
      Голосования на платформе Ethereum
    </template>

    <b-card-group deck>
      <b-card header="<b>Открытые голосования</b>">
        <b-list-group>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
        </b-list-group>
        <p class="card-text mt-2">
          Это открытые голования, представляющие собой контракты, расположеные в блокчейне Ethereum.
          Вы можете принять участие в любом голосовании, используя приватный ключ своего аккаунта в сети Ethereum.
        </p>
      </b-card>
      <b-card header="<b>Закрытые голосования</b>">
        <b-list-group>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
          <b-list-group-item href="#">Навальный vs Путин</b-list-group-item>
        </b-list-group>
        <p class="card-text mt-2">
          Эти голосования уже завершены. Можно только ознакомиться с результатами.
        </p>
      </b-card>
    </b-card-group>
  </b-jumbotron>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data () {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    }
  }
</script>
