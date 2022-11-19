<script setup>
import { onMounted, nextTick, ref, reactive, computed } from "vue";
import http from "@/utils/http";

//获取坐标函数
function getAxisId(row, col) {
  return row + col;
}

function getMaskInputId(index) {
  return "mi" + index;
}

//主面板数据
const num = ref(0);
const drawTotal = ref(0);
const drawItems = ref([]);
const hitCells = reactive([]);
const colors = [
  "bg-yellow",
  "bg-brown",
  "bg-orange",
  "bg-grey",
  "bg-amber",
  "bg-lime",
];

function resetAllHitCells() {
  if (hitCells.length > 0) {
    for (let cell of hitCells) {
      for (let color of colors) {
        cell.classList.remove(color);
      }
    }
    hitCells.value = [];
  }
}

function rememberHitCell(cell) {
  hitCells.push(cell);
}

onMounted(() => {
  http.get("/home").then((response) => {
    num.value = response.data.num;
    drawTotal.value = response.data.total;
    drawItems.value = response.data.items;
    nextTick(() => {
      window.scrollTo({ top: 800, behavior: "smooth" });
    });
  });
});

// 输入框
const maskInput = ref(["*", "*", "*", "*"]);
const mask = computed(() => maskInput.value.join(""));

function onMaskInputFocus(event) {
  resetAllHitCells();
  let idx = event.target.dataset.idx;
  for (var i = 0; i < 4; i++) {
    if (i != idx) {
      let mInput = document.getElementById(getMaskInputId(i));
      mInput.value = "";
      maskInput.value[i] = "*";
    }
  }
}

function onMaskInputBlur(event) {
  let idx = event.target.dataset.idx;
  maskInput.value[idx] = event.target.value;
}

//查询结果数据
const patterns = reactive({
  viewIdx: -1,
  total: 0,
  items: [],
  lastRoundPoints: [],
});

const hasNext = computed(
  () => patterns.total > 0 && patterns.viewIdx < patterns.total
);
const hasPrevious = computed(() => patterns.total > 0 && patterns.viewIdx > 0);

function queryPatterns() {
  http.get("/patterns/" + num.value + "/" + mask.value).then((response) => {
    patterns.total = response.data.total;
    patterns.items = response.data.items;
    viewNext(1);
  });
}

function viewNext(direction) {
  let idx = direction > 0 ? patterns.viewIdx + 1 : patterns.viewIdx - 1;
  if (idx < 0 || idx >= patterns.total) {
    return;
  }
  resetAllHitCells();
  let round_list = patterns.items[idx].round_list;

  for (var round = 0; round < round_list.length; round++) {
    for (var ci in round_list[round].coordinates) {
      let coord = round_list[round].coordinates[ci];
      console.log(coord);
      let cell = document.getElementById(getAxisId(coord.row, coord.col));
      cell.classList.add(colors[round]);
      rememberHitCell(cell);
    }
  }
  patterns.viewIdx = idx;
}
</script>

<template>
  <v-container fluid class="pa-0">
    <template v-for="(draw, index) in drawItems">
      <v-row no-gutters class="d-md-flex flex-row flex-nowrap text-center">
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
      class="d-md-flex flex-row flex-nowrap text-center"
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
              placeholder="*"
              :id="getMaskInputId(n - 2)"
              class="d-flex h-100 w-100 text-center"
              :data-idx="n - 2"
              @focus="onMaskInputFocus"
              @blur="onMaskInputBlur"
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

    <div class="d-flex justify-space-between bg-light-green-lighten-5">
      <v-btn class="ma-1" :disable="hasPrevious" @click="viewNext(-1)">
        <v-icon start icon="mdi-arrow-left"></v-icon>
        上一个
      </v-btn>
      <v-btn class="ma-1" color="light-green" @click="queryPatterns">
        <v-icon center icon="mdi-magnify"></v-icon>
        查询
      </v-btn>
      <v-btn class="ma-1" :disable="hasNext" @click="viewNext(1)">
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
