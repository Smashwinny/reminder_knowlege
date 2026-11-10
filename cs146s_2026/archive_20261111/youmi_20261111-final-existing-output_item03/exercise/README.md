# 原始课程函数的离线实验
Python3.13标准库，先运行fetch_source.py（公开下载，固定SHA256，不导入源码）以恢复未授权再分发的课程示例。全体练习脚本为本worker自写。
```bash
python3 exercise/fetch_source.py
python3 exercise/course_lab.py manifest
python3 exercise/course_lab.py inspect_source
python3 exercise/course_lab.py parsing
python3 exercise/course_lab.py file_tools
python3 exercise/course_lab.py replay
python3 exercise/course_lab.py test
```
manifest需本项公开证据文件，因此exercise.zip包含相应证据；原源码不打包。工具操作限本项scratch。不要直接运行下载示例顶层，它会初始化付费提供方并要求用户密钥。
