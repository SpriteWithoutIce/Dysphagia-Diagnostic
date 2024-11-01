// pages/blue/blue.js
function inArray(arr, key, val) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i][key] === val) {
      return i;
    }
  }
  return -1;
}

// 将字符串转为 ArrayBuffer
function str2ab(str) {
  let buf = new ArrayBuffer(str.length);
  let bufView = new Uint8Array(buf);
  for (var i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}
Page({

  /**
   * 页面的初始数据
   */
  // bluetooth-comp/index.js
  data:{
    devices: [],
    connected: false,
    chs: []
  },
  /* 初始化蓝牙模块 */
  openBluetoothAdapter() {
    // 先关闭蓝牙模块再开启 防止断开后点连接连接不上
    this.closeBluetoothAdapter();

    wx.openBluetoothAdapter({
      success: response => {
        console.log("初始化蓝牙模块成功：openBluetoothAdapter", response);
        this.startBluetoothDevicesDiscovery();
      },
      fail: err => {
        if (err.errCode === 10001) {
          /* 监听蓝牙适配器状态变化事件 */
          wx.onBluetoothAdapterStateChange(res => {
            console.log("监听蓝牙适配器状态变化事件：onBluetoothAdapterStateChange", res);
            res.available && this.startBluetoothDevicesDiscovery();
          });
        }
      },
    });
  },
  /* 获取本机蓝牙适配器状态 */
  getBluetoothAdapterState() {
    wx.getBluetoothAdapterState({
      success: res => {
        console.log("getBluetoothAdapterState", res);
        if (res.discovering) {
          // 是否正在搜索设备
          this.onBluetoothDeviceFound();
        } else if (res.available) {
          // 蓝牙适配器是否可用
          this.startBluetoothDevicesDiscovery();
        }
      },
    });
  },
  /* 开始搜寻附近的蓝牙外围设备 */
  startBluetoothDevicesDiscovery() {
    // 开始扫描参数
    if (this._discoveryStarted) return;

    this._discoveryStarted = true;
    wx.startBluetoothDevicesDiscovery({
      allowDuplicatesKey: true,
      success: response => {
        console.log("开始搜寻附近的蓝牙外围设备：startBluetoothDevicesDiscovery", response);
        this.onBluetoothDeviceFound();
      },
      fail: err => {
        console.log("搜索设备失败", err);
        wx.showToast({ title: "搜索设备失败", icon: "none" });
      },
    });
  },
  /* 停止搜寻附近的蓝牙外围设备。*/
  stopBluetoothDevicesDiscovery() {
    console.log("停止搜寻附近的蓝牙外围设备");
    wx.stopBluetoothDevicesDiscovery();
  },
  /* 监听搜索到新设备的事件 */
  onBluetoothDeviceFound() {
    wx.onBluetoothDeviceFound(res => {
      res.devices.forEach(device => {
        if (!device.name && !device.localName) {
          return;
        }

        const foundDevices = this.data.devices;
        const idx = inArray(foundDevices, "deviceId", device.deviceId);
        const data = {};
        if (idx === -1) {
          data[`devices[${foundDevices.length}]`] = device;
        } else {
          data[`devices[${idx}]`] = device;
        }
        this.setData(data);
      });
    });
  },
  /* 连接蓝牙低功耗设备。*/
  createBLEConnection() {
    const deviceId = "EC:64:C9:AB:2B:52";
    const name = "ESP32BLE";
    wx.createBLEConnection({
      deviceId,
      success: () => {
        this.setData({ connected: true, name, deviceId });
        wx.showToast({ title: "连接蓝牙设备成功", icon: "none" });
        this.getBLEDeviceServices(deviceId);
      },
      fail: () => {
        console.log("连接失败");
        wx.showToast({ title: "连接失败", icon: "none" });
      },
    });
    // 停止搜寻蓝牙设备
    this.stopBluetoothDevicesDiscovery();
  },
  /* 断开与蓝牙低功耗设备的连接。 */
  closeBLEConnection() {
    console.log("断开与蓝牙低功耗设备的连接");
    wx.showToast({ title: "已断开和蓝牙设备的连接", icon: "none" });
    wx.closeBLEConnection({ deviceId: this.data.deviceId });
    this.setData({ connected: false, chs: [], canWrite: false });
  },
  /* 获取蓝牙低功耗设备所有服务 (service) */
  getBLEDeviceServices(deviceId) {
    wx.getBLEDeviceServices({
      deviceId,
      success: res => {
        for (let i = 0; i < res.services.length; i++) {
          if (res.services[i].isPrimary) {
            this.getBLEDeviceCharacteristics(deviceId, res.services[i].uuid);
            return;
          }
        }
      },
    });
  },
  /* 获取蓝牙低功耗设备某个服务中所有特征 (characteristic)。 */
  getBLEDeviceCharacteristics(deviceId, serviceId) {
    wx.getBLEDeviceCharacteristics({
      deviceId,
      serviceId,
      success: res => {
        console.log("获取蓝牙低功耗设备某个服务中所有特征：getBLEDeviceCharacteristics");

        for (let i = 0; i < res.characteristics.length; i++) {
          let item = res.characteristics[i];
          if (item.properties.read) {
            wx.readBLECharacteristicValue({ deviceId, serviceId, characteristicId: item.uuid });
          }
          if (item.properties.write) {
            this.setData({ canWrite: true });
            this._deviceId = deviceId;
            this._serviceId = serviceId;
            this._characteristicId = item.uuid;
            //   this.writeBLECharacteristicValue();
          }
          if (item.properties.notify || item.properties.indicate) {
            wx.notifyBLECharacteristicValueChange({
              deviceId,
              serviceId,
              characteristicId: item.uuid,
              state: true,
              success(res) {
                console.log("notifyBLECharacteristicValueChange success", res);
              },
            });
          }
        }
      },
      fail(res) {
        console.error("getBLEDeviceCharacteristics", res);
      },
    });

    // 操作之前先监听，保证第一时间获取数据
    wx.onBLECharacteristicValueChange(characteristic => {
      // console.log("收到原始的数据", characteristic, characteristic.value);
      const buffer = characteristic.value;
      
      const int8Array = new Int8Array(buffer);
      // for (let i = 0; i < int8Array.length; i++) {
      //   console.log(int8Array[i]);
      // }

      let asciiString = '';
      for (let i = 0; i < int8Array.length; i++) {
        asciiString += String.fromCharCode(int8Array[i]);
      }

      // 将字符串分割成单独的数字字符串
      const numberStrings = asciiString.match(/(\d+\.\d+)/g);

      // 将数字字符串转换为小数
      const numbers = numberStrings.map(numString => parseFloat(numString));

      // 输出转换后的小数数组
      console.log(numbers);
      
    });
  },
  /* 向蓝牙低功耗设备特征值中写入二进制数据 */
  writeBLECharacteristicValue(jsonStr) {
    let arrayBufferValue = str2ab(jsonStr);
    console.log("发送数据给蓝牙", "原始字符串", jsonStr, "转换arrayBuffer", arrayBufferValue);

    wx.writeBLECharacteristicValue({
      deviceId: this._deviceId,
      serviceId: this._serviceId, // 微信文档上是错误的
      characteristicId: this._characteristicId,
      value: arrayBufferValue, // 只能发送arrayBuffer类型数据
      success(res) {
        console.log("消息发送成功", res.errMsg);
        wx.showToast({ title: "消息发送成功", icon: "none" });
      },
      fail(e) {
        console.log("发送消息失败", e);
        wx.showToast({ title: "发送消息失败,错误信息: " + e.errMsg, icon: "none" });
      },
    });
  },
  closeBluetoothAdapter() {
    console.log("关闭蓝牙模块");
    wx.closeBluetoothAdapter();
    this._discoveryStarted = false;
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },
  // bluetooth-comp/index.js
})
