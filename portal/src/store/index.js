import { reactive } from 'vue'

//为了确保改变状态的逻辑像状态本身一样集中，
//建议在 store 上定义方法，方法的名称应该要能表达出行动的意图
const store = reactive({
  num: 0,
  updateNum(num) {
    this.num = num
  }
})

export default store