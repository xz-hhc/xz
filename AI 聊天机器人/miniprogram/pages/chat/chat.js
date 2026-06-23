const app = getApp();

Page({
  data: {
    messages: [
      {
        role: "bot",
        content: "你好！我是你的AI知识助手 👋\n\n你可以通过「上传」页面导入文档资料，上传后我能自动学习并基于你的资料回答问题。",
        sources: []
      }
    ],
    inputValue: "",
    isTyping: false,
  },

  onInput(e) {
    this.setData({ inputValue: e.detail.value });
  },

  sendMessage() {
    const msg = this.data.inputValue.trim();
    if (!msg) return;

    // Add user message
    const msgs = [...this.data.messages, { role: "user", content: msg, sources: [] }];
    this.setData({ messages: msgs, inputValue: "", isTyping: true });

    const apiBase = app.globalData.apiBaseUrl;
    wx.request({
      url: apiBase + "/api/chat",
      method: "POST",
      header: { "Content-Type": "application/json" },
      data: {
        message: msg,
        conversation_id: app.globalData.conversationId,
      },
      success: (res) => {
        const data = res.data;
        app.globalData.conversationId = data.conversation_id;
        const botMsg = {
          role: "bot",
          content: data.reply,
          sources: data.sources || [],
        };
        this.setData({
          messages: [...this.data.messages, botMsg],
          isTyping: false,
        });
      },
      fail: (err) => {
        this.setData({
          messages: [...this.data.messages, {
            role: "bot",
            content: "抱歉，请求失败，请检查网络连接。",
            sources: []
          }],
          isTyping: false,
        });
      }
    });
  },
});
