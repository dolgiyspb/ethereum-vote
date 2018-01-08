import Vue from 'vue'
import Router from 'vue-router'
import VoteList from '@/components/VoteList'
import VoteDeatils from "@/components/VoteDetails"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'VoteList',
      component: VoteList
    },
    {
      path: '/contract/:address',
      component: VoteDeatils,
      name: 'VoteDetails'
    }
  ]
})
