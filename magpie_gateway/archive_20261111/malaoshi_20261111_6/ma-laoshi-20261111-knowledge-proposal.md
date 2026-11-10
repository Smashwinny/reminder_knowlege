# 候选知识合入建议（仅建议，未写共享vault）
## 查重基线
reminder_knowlege main `a8674777e18302b8804b137212b1396cbfe5a747`；实读00-总览、BYOK模型网关与用量归因、Provider适配层与错误契约、接缝与桩实现StubSeam。未发现magpie/Kiro专项；旧笔记已有统一网关、计量分层、stub，因此不重复创建这些同义概念。
## 建议新增
- vault/项目笔记/magpie-网关与订阅边界.md：固定源码、原帖与作者回复的冲突、官方FAQ直接限制、官方替代路径。
- 追加到 vault/概念/BYOK模型网关与用量归因.md：asked/member/wire/served四层名称；网关计量有reported和estimate来源，cache_unknown不等于0%。
- 追加到 vault/概念/Provider适配层与错误契约.md：本次离线Messages文本→mock chat实验，6类拒绝不上游，503映射502。不要继承旧笔记的“永不throw”契约到本HTTP接口；契约要按调用边界设计。
- 追加到 vault/概念/接缝与桩实现StubSeam.md：不用任何订阅验证路由与计量；mock成功只证实接缝，不证实真实模型或合规。
## 本次确实执行
编译+4分组测试：text/routes/usage/errors，全部0退出；2请求计量4合成输入+4输出；错误注入与拒绝实际发生。详情看experiment-log。
## 不合入为事实
作者“不会封号”“效果相同”、具体性能/节省比例、历史缓存修复、真实模型与订阅额度、Desktop全功能兼容。产品实接入本次未授权执行。
## 交付方式
仅本独立云端目录候选成果；由总协调者决定合入路径与去重。没有独立第三方审核，不自称审核通过。
