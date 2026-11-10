# 零凭证网关练习
原创教学实现，不是magpie源码副本，不是Kiro接口模拟器或产品替代品。来源URL+SHA写在gateway.py头部。
仅Python3标准库；无安装步骤、模型、API key、账号读取。禁止用于公网生产。
运行（在此目录）：
```
python3 -m py_compile ma-laoshi-20261111-gateway.py ma-laoshi-20261111-test_gateway.py
python3 ma-laoshi-20261111-test_gateway.py text
python3 ma-laoshi-20261111-test_gateway.py routes
python3 ma-laoshi-20261111-test_gateway.py usage
python3 ma-laoshi-20261111-test_gateway.py errors
```
每条命令自行创建临时127.0.0.1 HTTP服务，验证后finally关闭。工具/SSE/图片显式拒绝，不是完整Anthropic协议实现。计数按空白分词并固定输出2，只为测试用量累加。
