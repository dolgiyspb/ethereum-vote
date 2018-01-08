import Vue from 'vue'
import Router from 'vue-router'
import VoteList from '@/components/VoteList'
import VoteDeatils from '@/components/VoteDetails'
import VoteCreate from '@/components/VoteCreate'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'VoteList',
      component: VoteList
    },
    {
      path: '/contract/create',
      component: VoteCreate,
      name: 'VoteCreate'
    },
    {
      path: '/contract/:address',
      component: VoteDeatils,
      name: 'VoteDetails'
    }
  ]
})
