<template>
  <div class="container">
    <div class="title-box">
      <h1 class="title">In Situ Fully Integrated Dysphagia Assisted Diagnostic Platform</h1>
    </div>
    
    <div class="columns">
      <div class="column">
        <h2 class="subtitle">Physiological Signals</h2>
        <div class="blocks">
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==0? '#c9e7e3' : '#fff' }">
            <img class="block-image" src="../assets/ditou.png" alt="Block Image" />
            <div class="block-text">Bow</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==1? '#c9e7e3' : '#fff' }">
            <img class="block-image" src="../assets/jujiao.png" alt="Block Image" />
            <div class="block-text">Chew</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==2? '#c9e7e3' : '#fff' }">
            <img class="block-image" src="../assets/kesou.png" alt="Block Image" />
            <div class="block-text">Cough</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==3? '#c9e7e3' : '#fff' }">
            <img class="block-image" src="../assets/ertongerbihou-tunyankunnan.png" alt="Block Image" />
            <div class="block-text">Swallow</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==4? '#c9e7e3' : '#fff' }">
            <img class="block-image" src="../assets/tanpeiyang.png" alt="Block Image" />
            <div class="block-text">Belch</div>
          </div>
        </div>
      </div>
      <div class="column">
        <h2 class="subtitle">Pronunciation</h2>
        <div class="blocks">
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==5? '#c9e7e3' : '#fff' }">
            <img class="block-image2" src="../assets/A.png" alt="Block Image" />
            <div class="block-text">A</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==6? '#c9e7e3' : '#fff' }">
            <img class="block-image2" src="../assets/e.png" alt="Block Image" />
            <div class="block-text">E</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==7? '#c9e7e3' : '#fff' }">
            <img class="block-image2" src="../assets/i.png" alt="Block Image" />
            <div class="block-text">I</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==8? '#c9e7e3' : '#fff' }">
            <img class="block-image2" src="../assets/o.png" alt="Block Image" />
            <div class="block-text">O</div>
          </div>
          <div class="block" v-bind:style="{ backgroundColor: isOpen == 1 && currentIndex==9? '#c9e7e3' : '#fff' }">
            <img class="block-image2" src="../assets/u.png" alt="Block Image" />
            <div class="block-text">U</div>
          </div>
        </div>
      </div>
      <div class="column">
        <h2 class="subtitle">Signal</h2>
        <div class="button-box">
          <button @click="predict" class="green-button">Start</button>
          <button @click="predict" class="green-button" style="background-color: indianred;">Stop</button>
        </div>
        
        <div class="image-block" style="width: 500px;">
          <img v-if="currentIndex===0" src="../assets/低头.gif" alt="Current Image" />
          <img v-if="currentIndex===1" src="../assets/咀嚼.gif" alt="Current Image" />
          <img v-if="currentIndex===2" src="../assets/咳嗽.gif" alt="Current Image" />
          <img v-if="currentIndex===3" src="../assets/干咽.gif" alt="Current Image" />
          <img v-if="currentIndex===4" src="../assets/打嗝.gif" alt="Current Image" />
          <img v-if="currentIndex===5" src="../assets/a.gif" alt="Current Image" />
          <img v-if="currentIndex===6" src="../assets/e.gif" alt="Current Image" />
          <img v-if="currentIndex===7" src="../assets/i.gif" alt="Current Image" />
          <img v-if="currentIndex===8" src="../assets/o.gif" alt="Current Image" />
          <img v-if="currentIndex===9" src="../assets/u.gif" alt="Current Image" />
        </div>
      </div>
      <div class="column">
        <h2 class="subtitle">Answer</h2>
        <button @click="predict1">Predict</button>
        <div class="block" style="justify-content: center; align-items: center;text-align: center;" v-if="isOpen==0">
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==0" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/ditou.png" alt="Block Image" />
          <div class="block-text">Bow</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==1" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/jujiao.png" alt="Block Image" />
          <div class="block-text">Chew</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==2" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/kesou.png" alt="Block Image" />
          <div class="block-text">Cough</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==3" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/ertongerbihou-tunyankunnan.png" alt="Block Image" />
          <div class="block-text">Swallow</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==4" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/tanpeiyang.png" alt="Block Image" />
          <div class="block-text">Belch</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==5" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/A.png" alt="Block Image" />
          <div class="block-text">A</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==6" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/e.png" alt="Block Image" />
          <div class="block-text">E</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==7" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/i.png" alt="Block Image" />
          <div class="block-text">I</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==8" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/o.png" alt="Block Image" />
          <div class="block-text">O</div>
        </div>
        <div class="block" v-if="isOpen==1 && currentIndex==9" style="background-color: #66cdaa;">
          <img class="block-image" src="../assets/u.png" alt="Block Image" />
          <div class="block-text">U</div>
        </div>
        <img src="../assets/model_structure.png" alt="Model Structure" style="width: 220px;margin-bottom: 10px;">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HealthMonitoringSystem',
  data() {
    return {
      numbers: ["Bow", "Chew", "Cough", "Swallow", "Belch", "A", "E", "I", "O", "U"],
      currentIndex: -1,
      isOpen:0,
      images: [
        "../assets/0-0.png",
        "../assets/0-1.png",
        "../assets/0-2.png",
        "../assets/0-3.png",
        "../assets/0-4.png",
        "../assets/1-A.png",
        "../assets/1-E.png",
        "../assets/1-I.png",
        "../assets/1-O.png",
        "../assets/1-U.png",
      ]
    }
  },
  computed: {
    currentNumber() {
      return this.numbers[this.currentIndex]; // 返回当前数字
    }
  },
  methods: {
    predict() {
      if (this.currentIndex < this.numbers.length - 1) {
        this.currentIndex++; // 移动到下一个数字
      } else {
        this.currentIndex = 0; // 如果是最后一个数字，重置为第一个数字
      }
      this.isOpen=0;
    },
    predict1() {
      this.isOpen=1;
    },
  }
}
</script>

<style scoped>
.container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 10px;
}

.title {
  font-size: 26px;
  color: #333;
  text-align: center;
}
.title-box{
  width: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
  background-color: #cddced;
  margin: 0 auto;
}

.columns {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.column {
  display: flex;
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 水平居中对齐 */
  border: 3px solid #cddced; 
  padding: 10px;
}

.column:last-child {
  margin-right: 0;
}

.subtitle {
  font-size: 22px;
  color: #0074bd;
  margin-bottom: 10px;
}

.blocks {
  display: flex;
  flex-direction: column; /* 子元素垂直排列 */
  justify-content: center; /* 垂直居中对齐 */
  align-items: center; /* 水平居中对齐 */
}

.block {
  background-color: #fff; 
  border: 1px solid #ddd; 
  padding: 10px;
  text-align: center;
  width: 200px;
  height: 60px;
  margin-bottom: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.block-image {
  max-width: 20%;
  height: auto;
  display: block;
  margin: 0 auto 5px; /* 使图片水平居中 */
}
.block-image2 {
  max-width: 20%;
  height: auto;
  display: block;
  margin: 0 auto 5px; /* 使图片水平居中 */
}

.block-text {
  font-size: 16px;
  color: #555;
  font-weight: bold;
}
.image-block {
  text-align: center;
}

.image-block img {
  width: 500px;
  height: auto;
}

.button-box{
  display: flex;
  flex-direction: row; /* 子元素垂直排列 */
  justify-content: space-around;
  align-items: center; /* 水平居中对齐 */
}

button {
  padding: 15px 40px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  margin-bottom: 10px;
  font-weight: bold;
  font-size: 18px;
  margin: 10px 20px;
}

button:hover {
  background-color: #0056b3;
}

.green-button {
  padding: 15px 40px;
  background-color: #00cc33;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  margin-bottom: 30px;
  font-weight: bold;
  font-size: 18px;
}

.green-button:hover {
  background-color: #5c9f59;
}
</style>