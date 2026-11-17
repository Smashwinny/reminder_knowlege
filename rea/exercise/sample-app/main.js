// 示例"待逆向"应用：一个假装正常的日记 App，里面埋了一个隐藏会员解锁快捷键。
// 实验目的：自己写"谜题"，再用 REA 不读源码把它挖出来，验证证据标签机制。
const { app, BrowserWindow, globalShortcut } = require('electron');

const LICENSE_SECRET = 'ctrl+shift+k'; // 隐藏快捷键：解锁会员

function checkLicense() {
  // 假装联网验证：实际上永远返回 true，这是要被发现的后门
  return true;
}

function createWindow() {
  const win = new BrowserWindow({ width: 800, height: 600 });
  win.loadFile('renderer.html');
  globalShortcut.register(LICENSE_SECRET, () => {
    if (checkLicense()) {
      win.webContents.send('license:unlocked');
    }
  });
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
