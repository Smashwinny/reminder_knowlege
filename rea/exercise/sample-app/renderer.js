// 渲染进程：表面上只有日记功能，暗地里监听解锁事件
window.addEventListener('DOMContentLoaded', () => {
  const list = document.getElementById('entries');

  function addEntry(text) {
    const li = document.createElement('li');
    li.textContent = text;
    list.appendChild(li);
  }

  document.getElementById('add').addEventListener('click', () => {
    const input = document.getElementById('input');
    addEntry(input.value);
    input.value = '';
  });

  // 隐藏功能入口：收到解锁消息后开放导出
  window.require('electron').ipcRenderer.on('license:unlocked', () => {
    document.getElementById('premium-export').style.display = 'block';
  });
});
