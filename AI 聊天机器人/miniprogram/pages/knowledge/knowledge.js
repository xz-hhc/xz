const app = getApp();

Page({
  data: {
    documents: [],
    stats: { docCount: 0, chunkCount: 0, vectorDim: 0 },
    loading: false,
  },

  onShow() {
    this.loadData();
  },

  onPullDownRefresh() {
    this.loadData(() => wx.stopPullDownRefresh());
  },

  loadData(callback) {
    this.setData({ loading: true });
    const apiBase = app.globalData.apiBaseUrl;

    Promise.all([
      new Promise((resolve) => {
        wx.request({
          url: apiBase + "/api/knowledge/list",
          success: (res) => {
            const docs = res.data.documents || [];
            this.setData({ documents: docs });
            resolve(docs);
          },
          fail: () => { this.setData({ documents: [] }); resolve([]); }
        });
      }),
      new Promise((resolve) => {
        wx.request({
          url: apiBase + "/api/knowledge/stats",
          success: (res) => {
            const s = res.data;
            this.setData({
              stats: {
                docCount: s.total_docs || 0,
                chunkCount: s.total_chunks || 0,
                vectorDim: s.vector_dim || 0,
              }
            });
            resolve();
          },
          fail: () => resolve()
        });
      })
    ]).then(() => {
      this.setData({ loading: false });
      if (callback) callback();
    });
  },

  deleteDoc(e) {
    const docId = e.currentTarget.dataset.id;
    wx.showModal({
      title: "确认删除",
      content: "确定要删除此文档吗？AI将丢失对应的知识。",
      success: (res) => {
        if (res.confirm) {
          wx.request({
            url: app.globalData.apiBaseUrl + "/api/knowledge/" + docId,
            method: "DELETE",
            success: () => {
              wx.showToast({ title: "删除成功", icon: "success" });
              this.loadData();
            },
            fail: () => {
              wx.showToast({ title: "删除失败", icon: "none" });
            }
          });
        }
      }
    });
  }
});
