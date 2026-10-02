---
tags: [概念]
领域: 前端工程 / 资产分发
别名: [jsDelivr 分发, npm as CDN, 包即CDN]
首次来源: "[[项目笔记/workout-guide]]"
---

# npm包即CDN源

**一句话定义**：npm 注册表本身可以被 jsDelivr 等公共 CDN 自动镜像，于是"发布一个 npm 包"就等于"获得了免费的全球边缘分发"，URL 里的版本号就是灰度开关。

**属于领域**：前端工程 / 静态资产分发（workout-guide 的 `getAssetUrl` 默认指向 `https://cdn.jsdelivr.net/npm/@bryllim/workout-guide@1.0.0/...`）

**通俗理解**（比喻/例子，讲完落回术语）：npm 像总仓库，jsDelivr 像自动帮你在全世界开的连锁便利店——货（包内容）一上架，便利店立刻免费铺货，你不用租店面不用配带宽。App 里 `<img src="https://cdn.jsdelivr.net/npm/包名@1.0.0/assets/...">` 直接能用；想升级就把 URL 里 `@1.0.0` 换成 `@1.1.0`（版本号即灰度），回滚就是把版本号改回去——不可变版本 URL 天然可缓存。

**实测要点**：
- `getAssetUrl(idOrSlug, frame, {baseUrl})` 支持自托管替换：但 frame.path 自带 `assets/` 前缀，baseUrl 要指向**包根**而不是 assets 目录，否则拼出 `assets/assets/` 双前缀（真实踩坑）
- 发布版 manifest 帧路径是 `.png`（npm 包只发 manifest 引用的 PNG），仓库内才有 `.svg` 矢量源——"仓库内容 ≠ 包内容"
- 同理可镜像 GitHub 仓库内容（jsDelivr 的 gh 前缀），适合小体量静态资产；大体量或高 SLA 再换自托管/对象存储

**与已有概念的关联**：
- 不可变版本 URL 与 [[快照契约与不可变只读]] 同一思想：发布即冻结
- [[提交即部署]] 的静态资产版：push 到 npm 即完成全球部署
- [[分层按需加载]]：包的 exports 把 manifest/assets 分路径暴露，消费端按需取

**首次接触于**：[[项目笔记/workout-guide]]
