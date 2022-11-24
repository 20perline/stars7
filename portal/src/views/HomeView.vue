<script setup>
import { onMounted, nextTick, ref, reactive, computed } from "vue";
import { useToast } from "vue-toastification";
import http from "@/utils/http";
import store from "@/store/index";

const toast = useToast();

//获取坐标函数
function getAxisId(row, col) {
  return row + col;
}

function getMaskInputId(index) {
  return "mi" + index;
}

function getPlaceholder(index) {
  let names = ['千', '百', '十', '个'];
  return names[index];
}

//主面板数据
const num = ref(0);
const drawTotal = ref(0);
const drawItems = ref([]);

onMounted(() => {
  http.get("/home").then((response) => {
    store.updateNum(response.data.num);
    num.value = response.data.num;
    drawTotal.value = response.data.total;
    drawItems.value = response.data.items;
    nextTick(() => {
      window.scrollTo({ top: 800, behavior: "smooth" });
    });
  });
});

//负责显示结果集
const indicator = reactive({
  colors: [
    "bg-yellow",
    "bg-brown",
    "bg-orange",
    "bg-grey",
    "bg-amber",
    "bg-lime",
  ],
  total: 0,
  items: [],
  cells: [],
  currentIndex: -1,

  init(items) {
    this.items = items;
    this.total = this.items.length;
    this.currentIndex = -1;
    if (this.total > 0) {
      this.showIndex(0);
    }
  },

  reset() {
    if (this.cells.length > 0) {
      for (let cell of this.cells) {
        for (let color of this.colors) {
          cell.classList.remove(color);
        }
      }
      this.cells = [];
    }
  },

  showIndex(idx) {
    if (idx < 0 || idx >= this.total) {
      return;
    }
    this.reset();
    let sign = this.items[idx].signature;
    // toast.info(sign);
    let round_list = this.items[idx].round_list;

    for (var round = 0; round < round_list.length; round++) {
      for (var ci in round_list[round].coordinates) {
        let coord = round_list[round].coordinates[ci];
        let cell = document.getElementById(getAxisId(coord.row, coord.col));
        cell.classList.add(this.colors[round]);
        this.cells.push(cell);
      }
    }
    this.currentIndex = idx;
  },

  //没参数的绑定时带上括号 this拿得到值?
  showNext() {
    let idx = this.currentIndex + 1;
    this.showIndex(idx);
  },
  showPrevious() {
    let idx = this.currentIndex - 1;
    this.showIndex(idx);
  },

});

const hasNext = computed(() => indicator.total > 0 && indicator.currentIndex < indicator.total - 1);
const hasPrevious = computed(() => indicator.total > 0 && indicator.currentIndex > 0);

//有参数的函数绑定时不带括号，默认会以event作为第一个参数调用
const assertion = reactive({
  posValues: ["*", "*", "*", "*"],
  check() {
    let mask = this.posValues.join("");
    if (mask === '****') {
      toast.error('请先输入一位数字');
      return;
    }
    if (mask.length > 4) {
      toast.error('只能输入一位数字');
      return;
    }
    http.get("/patterns/" + num.value + "/" + mask).then((response) => {
      toast.success('共有' + response.data.total + '局')
      indicator.init(response.data.items);
    });
  },
  reset(event) {
    indicator.reset();
    let idx = event.target.dataset.idx;
    for (var i = 0; i < 4; i++) {
      if (i != idx) {
        document.getElementById(getMaskInputId(i)).value = "";
        this.posValues[i] = "*";
      }
    }
  },
  update(event) {
    let idx = event.target.dataset.idx;
    this.posValues[idx] = event.target.value;
  },
});

</script>

<template>
  <v-container fluid class="pa-0">
    <template v-for="(draw, index) in drawItems">
      <v-row no-gutters class="d-md-flex flex-row flex-nowrap justify-center text-center">
        <v-col cols="2">
          <v-sheet
            elevation="1"
            class="d-flex col-cell bg-light-green-lighten-2"
          >
            {{ draw.num }}
          </v-sheet>
        </v-col>

        <template v-for="n in 8">
          <v-col
            v-if="n >= 2 && n <= 5"
            :key="n"
            sm="1"
            class="font-weight-bold"
          >
            <v-sheet
              elevation="1"
              class="d-flex col-cell"
              :id="getAxisId(drawTotal - index - 1, 'c' + (n - 1))"
            >
              {{ draw["c" + (n - 1)] }}
            </v-sheet>
          </v-col>
          <v-col v-else :key="n + 1" sm="1">
            <v-sheet
              elevation="1"
              class="d-flex col-cell bg-light-green-lighten-4"
              :id="getAxisId(drawTotal - index - 1, 'c' + (n - 1))"
            >
              {{ draw["c" + (n - 1)] }}
            </v-sheet>
          </v-col>
        </template>
      </v-row>
      <v-divider
        v-if="(draw.num + 1) % 4 == 0"
        color="light-green"
        thickness="2"
      ></v-divider>
    </template>

    <v-row
      no-gutters
      class="d-md-flex flex-row flex-nowrap justify-center text-center"
      align="center"
    >
      <v-col cols="2">
        <v-sheet elevation="1" class="d-flex col-cell bg-light-green-lighten-2">
          {{ num }}
        </v-sheet>
      </v-col>

      <template v-for="n in 8">
        <v-col v-if="n >= 2 && n <= 5" :key="n" sm="1" class="font-weight-bold">
          <v-sheet
            elevation="1"
            class="d-flex col-cell"
            :id="getAxisId(-1, 'c' + (n - 1))"
          >
            <input
              type="number"
              :placeholder="getPlaceholder(n - 2)"
              :id="getMaskInputId(n - 2)"
              class="d-flex h-100 w-100 text-center"
              :data-idx="n - 2"
              @focus="assertion.reset"
              @blur="assertion.update"
            />
          </v-sheet>
        </v-col>
        <v-col v-else :key="n + 1" sm="1">
          <v-sheet
            elevation="1"
            class="d-flex col-cell bg-light-green-lighten-4"
          >
          </v-sheet>
        </v-col>
      </template>
    </v-row>

    <div class="d-flex justify-space-between bg-light-green-lighten-5" v-if="num > 0">
      <v-btn class="ma-1" :disabled="!hasPrevious" @click="indicator.showPrevious()">
        <v-icon start icon="mdi-arrow-left"></v-icon>
        上一个
      </v-btn>
      <v-btn class="ma-1" color="light-green" @click="assertion.check()">
        <v-icon center icon="mdi-magnify"></v-icon>
        查询
      </v-btn>
      <v-btn class="ma-1" :disabled="!hasNext"  @click="indicator.showNext()">
        下一个
        <v-icon end icon="mdi-arrow-right"></v-icon>
      </v-btn>
    </div>

  </v-container>
</template>

<style>
.col-cell {
  height: 40px;
  justify-content: center;
  align-items: center;
}
</style>
