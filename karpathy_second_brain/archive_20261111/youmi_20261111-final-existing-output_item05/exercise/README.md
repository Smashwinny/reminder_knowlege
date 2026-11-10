# 三角色合成实验
Python3.13标准库，无密钥无网络；程序由worker自写。解压到任意目录，进入item05：
```bash
python3 exercise/brain_lab.py setup
python3 exercise/brain_lab.py collect
python3 exercise/brain_lab.py compile
python3 exercise/brain_lab.py check
python3 exercise/brain_lab.py boundaries
python3 exercise/brain_lab.py test
```
仅写当前项目scratch/results。输入是3份合成材料，不是HTTP缓存事实或个人资料。重跑collect会保留已存在文件；其余派生页可重建。程序按角色字符串检查，不是OS沙箱；没有网络/外发执行器。没有实现自由文本矛盾检测、并发、崩溃恢复或真正多Bot协同。
