# 公开归档版依赖恢复说明

本次公开整理移除了第三方源码、模板及上游说明书副本；原始ZIP仍在本地归档，原创驱动、教学代码、测试和既有结果保留。许可证/NOTICE仅说明来源及条件，不代表源码仍随包提供。

**本轮没有下载依赖、重新执行实验或重新学习；不能宣称清理后的目录直接可运行或已通过复现。** 原HTML/PDF/实验日志及README中的命令描述的是当时完整实验包，公开版需先恢复下表依赖，并检查原README的运行环境和其他外部依赖。不要把历史成功记录当作新环境运行结果。

## 已记录的一手版本

仓库：[wheresryan22/anatomy](https://github.com/wheresryan22/anatomy)  
固定提交：`1482e8469b0a9e0d8cc18ea2740a01423d29ae80`（[固定树](https://github.com/wheresryan22/anatomy/tree/1482e8469b0a9e0d8cc18ea2740a01423d29ae80)）。

版本和路径来自已经保存的sources.md、实验清单/许可与原ZIP，不是本轮重新连接上游的结果。SHA256是从原交付包逐字节计算的预期内容哈希。

## 恢复方法（说明，未执行）

1. 将上述公开仓库的固定提交取回另一个隔离的依赖目录，不把完整上游或.git纳入学习仓库。
2. 以该提交的仓库根为起点读取下表“上游相对路径”；仅将必要文件恢复到本项目archive_20261111下的“练习相对路径”。保留原许可证、署名与第三方条件。
3. 对每个恢复文件计算SHA256并与表中比较。路径不可得或哈希不符时停止恢复、保留差异，不用最新main替代，也不覆盖原创练习。
4. 本说明只交代缺失依赖；没有执行这些步骤，没有确认网络可达/重新取回字节，也没有承诺跨系统或新环境的复现。

| 练习相对路径（恢复位置） | 固定仓库内相对路径 | 原交付字节SHA256 |
|---|---|---|
| `exercise/upstream/examples/dial-indicator/build.mjs` | `examples/dial-indicator/build.mjs` | `e4eaa2324af7f2630650ca72e52a78d56159213a786e14fba8321344789f990d` |
| `exercise/upstream/examples/dial-indicator/dial-indicator-light.html` | `examples/dial-indicator/dial-indicator-light.html` | `bc1810e340d916a25cc1749589b44096b7e41970f22fa7fce569bbefc0613093` |
| `exercise/upstream/kit/iso-kit.mjs` | `kit/iso-kit.mjs` | `6d3ecc725d30c3b0346da309cf61dfa5a65017c23620bbd4093009d4fb104018` |
| `exercise/upstream/kit/iso.css` | `kit/iso.css` | `ef19bac5a42ba9be42b56b2c1cf7fc7e21d332a8060765e9ca1d987b8ab23924` |
| `exercise/upstream/scripts/inline-kit.mjs` | `scripts/inline-kit.mjs` | `01e08df7c2556ce52a7e8ed9009a332036b209ab7e42389874af2a65fda6e9db` |

`examples/dial-indicator/dial-indicator-light.html`同时是官方示例的生成产物；本轮没有确认它是否直接存在于固定Git树。若上游只有build.mjs，不执行新构建来冒充已恢复，可先使用本地原包中哈希匹配的既有产物；需要另行重建时应明确记为后续工作。
