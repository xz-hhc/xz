const app = getApp();

Page({
  data: {
    uploadStatus: "",
    uploadHistory: [],
  },

  chooseFile() {
    wx.chooseMessageFile({
      count: 1,
      type: "file",
      extension: ["txt", "md", "csv", "pdf", "docx", "json"],
      success: (res) => {
        const file = res.tempFiles[0];
        this.uploadFile(file);
      }
    });
  },

  uploadFile(file) {
    this.setData({ uploadStatus: `正在上传: ${file.name}...` });

    wx.uploadFile({
      url: app.globalData.apiBaseUrl + "/api/upload",
      filePath: file.path,
      name: "file",
      success: (res) => {
        const data = JSON.parse(res.data);
        if (res.statusCode === 200) {
          this.setData({
            uploadStatus: `✅ ${data.message}`,
            uploadHistory: [
              { id: data.id, filename: data.filename },
              ...this.data.uploadHistory.slice(0, 19),
            ],
          });
        } else {
          this.setData({ uploadStatus: `❌ 上传失败: ${data.detail || "未知错误"}` });
        }
      },
      fail: (err) => {
        this.setData({ uploadStatus: "❌ 上传失败，请检查网络" });
      }
    });
  }
});
