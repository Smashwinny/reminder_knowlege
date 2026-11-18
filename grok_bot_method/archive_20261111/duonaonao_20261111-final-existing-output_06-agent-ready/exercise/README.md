# 本地Agent-ready门禁练习
零依赖Python3+Git。解压到全新目录，依次运行 python3 lab.py 1 / 2 / 3 / 4 / 5。
lab.py会生成runs-v2/；故意不打包运行目录，避免字节码和覆盖旧证据。
源代码中的所有审批是合成夹具，绝不代表真实独立审阅。程序只判eligible，不merge/push/deploy。
实际执行日志见experiment-log.md；首轮失败也保留。
CI YAML仅提供待验证模板，未上传执行；GitHub Actions的v4/v5标签不等于固定action commit，生产接入应另行固定且审查。
本地脚本在候选仓库外控制验证，本实验不提供恶意代码沙箱。
