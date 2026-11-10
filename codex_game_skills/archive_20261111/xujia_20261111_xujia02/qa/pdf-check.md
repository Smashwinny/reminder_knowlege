# PDF检查：未渲染

无头Chrome打印命令使用独立item02/qa/pdf-profile：
```bash
timeout 30s /usr/bin/google-chrome --headless=new --disable-dev-shm-usage --disable-gpu --disable-extensions --no-first-run --disable-search-engine-choice-screen --no-default-browser-check --user-data-dir=/workspace/xujia-batch/item02/qa/pdf-profile --print-to-pdf=/workspace/xujia-batch/item02/guide.pdf --no-pdf-header-footer file:///workspace/xujia-batch/item02/guide.html
```
30秒后仍无guide.pdf，随后仅终止本项专属profile进程。stderr仅见DBus连接错误/UPower警告，不足以确诊根因，未修改系统/代理/账户。

未生成PDF，所以没有pdftoppm逐页图像，也没有做或声称完成逐页视觉检查。HTML包含A4、卡片break-inside:avoid、print-color-adjust:exact；这些是静态样式，不代表打印已经通过。预计11个设计页，不能当作PDF实测页数。

保留轻量guide.html；PDF状态为“未渲染”。
