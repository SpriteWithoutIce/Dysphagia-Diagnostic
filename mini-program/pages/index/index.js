function inArray(arr, key, val) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i][key] === val) {
      return i;
    }
  }
  return -1;
}
// ArrayBuffer转16进度字符串示例
function ab2hex(buffer) {
  var hexArr = Array.prototype.map.call(
    new Uint8Array(buffer),
    function (bit) {
      return ('00' + bit.toString(16)).slice(-2)
    }
  )
  return hexArr.join('');
}
Page({
  onReady: function () {
    const points=[10, 30, 50, 40, 30, 20, 30]
    this.setData({
      points:points
    })
    this.drawSmoothLineChart();
    console.log(this.data.points);
  },
  data: function() {
    return{
      points: [10, 30, 50, 40, 30, 20, 30],
      count: 0,
      draw_points: [],
    };
  },
  onLoad: function(options) {
    console.log(this.data.points); // 应该打印出数组
  },
  start: function(){
    this.drawSmoothLineChart();
  },
  drawSmoothLineChart: function () {
    wx.createSelectorQuery()
    .select('#smoothLineCanvas') // 在 WXML 中填入的 id
    .fields({ node: true, size: true })
    .exec((res) => {
        // Canvas 对象
        const canvas = res[0].node
        // 渲染上下文
        const ctx = canvas.getContext('2d')
        ctx.fillStyle = '#9cd2b4';
        ctx.fillRect(0, 0, 250, 150);
        const data = this.data.points; // 你的数据数组
        console.log(data)
        // console.log(data.length)
        const points = this.calculatePoints(data); // 计算绘制点
        this.drawPinkBackground(ctx);
        // 绘制背景格子
        this.drawGrid(ctx);
        // 绘制折线图
        this.drawSmoothLine(ctx, points);
    })
    
  },
  calculatePoints: function (data) {
    const points = [];
    let x = 10; // 起始x坐标
    let y = 150; // 起始y坐标，假设canvas高度为200
    const minY = 0; // 数据的最小值
    const maxY = 400; // 数据的最大值
    const range = maxY - minY; // 数据的范围
    for (let i = 0; i < data.length; i++) {
      const value = (data[i] - minY) / range * 100;
      points.push({ x: x, y: y - value }); // 根据数据值计算y坐标
      x += 20; // x坐标间隔
    }
    console.log(points);
    return points;
  },
  drawPinkBackground: function (ctx) {
    ctx.fillStyle='#FFC0CB'; // 粉色背景
    ctx.fillRect(0, 0, 250, 75); // 填充上半部分粉色背景
  },
  drawGrid: function (ctx) {
    ctx.beginPath();
    ctx.lineWidth =1;
    ctx.strokeStyle='#f0f0f0'; // 白色格子线
    for (let i = 0; i <= 250; i += 40) {
      ctx.moveTo(i, 0);
      ctx.lineTo(i, 150);
    }
    for (let i = 0; i <= 150; i += 20) {
      ctx.moveTo(0, i);
      ctx.lineTo(250, i);
    }
    ctx.stroke();
  },
  drawSmoothLine: function (ctx, points) {
    ctx.beginPath();
    ctx.strokeStyle='#000000'; // 折线颜色
    ctx.lineWidth=2;
    ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
      // 二次贝塞尔曲线绘制圆滑折线
      ctx.bezierCurveTo(
        points[i - 1].x + (points[i].x - points[i - 1].x) / 3,
        points[i - 1].y,
        points[i].x - (points[i].x - points[i - 1].x) / 3,
        points[i].y,
        points[i].x,
        points[i].y
      );
    }
    ctx.stroke();
  },
  data: {
    devices: [],
    connected: false,
    chs: [],
    healthy: 1,
    tmp_data: [],
  },
  onLoad() {
   
  },
  openBluetoothAdapter() {
    wx.openBluetoothAdapter({
      success: (res) => {
        console.log('openBluetoothAdapter success', res)
        this.startBluetoothDevicesDiscovery()
      },
      fail: (res) => {
        if (res.errCode === 10001) {
          wx.onBluetoothAdapterStateChange(function (res) {
            console.log('onBluetoothAdapterStateChange', res)
            if (res.available) {
              this.startBluetoothDevicesDiscovery()
            }
          })
        }
      }
    })
  },
  startBluetoothDevicesDiscovery() {
    if (this._discoveryStarted) {
      return
    }
    this._discoveryStarted = true
    wx.startBluetoothDevicesDiscovery({
      allowDuplicatesKey: true,
      success: (res) => {
        console.log('startBluetoothDevicesDiscovery success', res)
        this.onBluetoothDeviceFound()
      },
    })
  },
  onBluetoothDeviceFound() {
    wx.onBluetoothDeviceFound((res) => {
      res.devices.forEach(device => {
        if (!device.name && !device.localName) {
          return
        }
        const foundDevices = this.data.devices
        const idx = inArray(foundDevices, 'deviceId', device.deviceId)
        const data = {}
        if (idx === -1) {
          data[`devices[${foundDevices.length}]`] = device
        } else {
          data[`devices[${idx}]`] = device
        }
        this.setData(data)
      })
    })
  },
  createBLEConnection() {
    const deviceId = "EC:64:C9:AB:2B:52"
    const name = "ESP32BLE"
    wx.createBLEConnection({
      deviceId,
      success: (res) => {
        this.setData({
          connected: true,
          name,
          deviceId,
        })
        this.getBLEDeviceServices(deviceId)
      }
    })
    this.stopBluetoothDevicesDiscovery()
  },
  getBLEDeviceServices(deviceId) {
    wx.getBLEDeviceServices({
      deviceId,
      success: (res) => {
        for (let i = 0; i < res.services.length; i++) {
          if (res.services[i].isPrimary) {
            this.getBLEDeviceCharacteristics(deviceId, res.services[i].uuid)
            return
          }
        }
      }
    })
  },
  getBLEDeviceCharacteristics(deviceId, serviceId) {
    wx.getBLEDeviceCharacteristics({
      deviceId,
      serviceId,
      success: (res) => {
        console.log('getBLEDeviceCharacteristics success', res.characteristics)
        for (let i = 0; i < res.characteristics.length; i++) {
          let item = res.characteristics[i]
          if (item.properties.read) {
            wx.readBLECharacteristicValue({
              deviceId,
              serviceId,
              characteristicId: item.uuid,
            })
          }
          if (item.properties.write) {
            this.setData({
              canWrite: true
            })
            this._deviceId = deviceId
            this._serviceId = serviceId
            this._characteristicId = item.uuid
            this.writeBLECharacteristicValue()
          }
          if (item.properties.notify || item.properties.indicate) {
            wx.notifyBLECharacteristicValueChange({
              deviceId,
              serviceId,
              characteristicId: item.uuid,
              state: true,
            })
          }
        }
      },
      fail(res) {
        console.error('getBLEDeviceCharacteristics', res)
      }
    })
    // 操作之前先监听，保证第一时间获取数据
    wx.onBLECharacteristicValueChange((characteristic) => {
      const idx = inArray(this.data.chs, 'uuid', characteristic.characteristicId)
      const data = {}
      const buffer = characteristic.value;
      const int8Array = new Int8Array(buffer);
      let asciiString = '';
      for (let i = 0; i < int8Array.length; i++) {
        asciiString += String.fromCharCode(int8Array[i]);
      }

      // 将字符串分割成单独的数字字符串
      const numberStrings = asciiString.match(/(\d+\.\d+)/g);

      // 将数字字符串转换为小数
      const numbers = numberStrings.map(numString => parseFloat(numString));

      // 输出转换后的小数数组
      console.log(numbers[0]*100);
      const new_number=this.data.points;
      // new_number.push(numbers[0]*100);
      
      // 加点
      // 降采样，20点
      const new_tmp=this.data.tmp_data;
      new_tmp.push(500-numbers[0]*100);
      if(new_tmp.length==10){
        const sum = new_tmp.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
        const average = sum / new_tmp.length;
        new_number.push(average);
        console.log(new_tmp);
        console.log(new_number);
        // 更新画图点
        if (new_number.length==16){
          this.setData({
            points: new_number
          })
          console.log(new_number);
          let hasThreeConsecutive = false;
          for (let i = 0; i < new_number.length - 3; i++) {
            if (new_number[i] > 300 && new_number[i + 1] > 300 && new_number[i + 2] > 300 && new_number[i + 3] > 300) {
              hasThreeConsecutive = true;
              break;
            }
          }
          // 输出结果
          if (hasThreeConsecutive) {
            console.log("Oh! This is bigger than 600.")
            this.setData({
              healthy:0
            })
          } else {
            this.setData({
              healthy:1
            })
          }
          this.drawSmoothLineChart();
          const new1=new_number.slice(-12);
          this.setData({
            points: new1
          })
        }
        else{
          this.setData({
            points: new_number
          })
        }
        this.setData({
          tmp_data:[],
        })
      }
      else{
        this.setData({
          tmp_data:new_tmp,
        })
      }
      

      if (idx === -1) {
        data[`chs[${this.data.chs.length}]`] = {
          uuid: characteristic.characteristicId,
          value: ab2hex(characteristic.value)
        }
      } else {
        data[`chs[${idx}]`] = {
          uuid: characteristic.characteristicId,
          value: ab2hex(characteristic.value)
        }
      }
      this.setData(data)
    })
  },
  stopBluetoothDevicesDiscovery() {
    wx.stopBluetoothDevicesDiscovery()
  },
  closeBluetoothAdapter() {
    wx.closeBluetoothAdapter()
    this._discoveryStarted = false
  },
});

