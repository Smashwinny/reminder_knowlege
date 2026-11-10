# 真实实验日志
2026-11-11 Asia/Shanghai；Python3.13 + Node；无账户、密钥、发布、消息和付费服务。

## 环境准备
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools/exercise/runtime
npm ci --ignore-scripts --no-audit --no-fund
cd ../..
ln -s exercise/runtime/node_modules node_modules
```
实际exit0；依赖固定package-lock.json，npm-ci-batch2.log保留。

## 1. 生成夹具
目的：冻结6条非真实新闻、关键词规则；没有获取用户资料。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools
python3 exercise/lab.py init
```
实际exit0，stdout：
```text
created RSS fixture: 6 items (synthetic); 1 duplicate; no external feed or private data
```
验证：fixture.xml中6个item，keywords.txt设全局排除广告。

## 2. 读取并去重
目的：验证XML输入契约，单Feed以GUID去重。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools
python3 exercise/lab.py collect
```
实际exit0，stdout：
```text
parsed RSS 6 -> deduplicated 5 (GUID scope=single feed; duplicate titles not globally merged)
```
验证：collected.json恰5条；不能推广到跨Feed同GUID。

## 3. 真实关键词组件
目的：按固定规则调用上游frequency.py并输出草稿。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools
python3 exercise/lab.py select
```
实际exit0，stdout：
```text
real TrendRadar frequency.py: 5 -> 2; IDs=1,5; require AI AND 开源; global exclude 广告
```
验证：selected.json IDs=1,5；5条→2条；article.md标明合成演示。

## 4. 真实净化与内联排版
目的：调用Doocs真实sanitizeHtml，再用marked和juice形成教学HTML。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools
exercise/runtime/node_modules/.bin/tsx exercise/render.ts
```
实际exit0，stdout：
```text
real Doocs sanitizeHtml: ordinary script+event removed; benign protected-marker content restored
marked + juice: HTML generated, inline style=true
scope: real sanitizer component, not full Doocs renderer or WeChat clipboard; marker trust boundary not a universal sanitizer proof
```
验证：普通script/onerror删除、无害保护标记往返，article-inline.html有style；不是完整Doocs渲染器。

## 5. 审计输出
目的：检查本地产物，记录固定模块哈希与RSSHub源码契约。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools
python3 exercise/lab.py audit
```
实际exit0，stdout：
```text
PASS local HTML 3 checks; RSSHub route static contract: PR entries excluded (not executed); SHA256 manifest saved
```
验证：3个本地HTML检查通过；RSSHub排除PR仅为静态检查，非真实路由运行。

## 附加上游测试（失败，未计入主实验PASS）
```bash
cd upstream/TrendRadar
python3 -m unittest tests/test_frequency.py
```
实际exit1：
```text
E
======================================================================
ERROR: test_frequency (unittest.loader._FailedTest.test_frequency)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_frequency
Traceback (most recent call last):
  File "/usr/lib/python3.13/unittest/loader.py", line 137, in loadTestsFromName
    module = __import__(module_name)
  File "/workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools/upstream/TrendRadar/tests/test_frequency.py", line 5, in <module>
    from trendradar.core.frequency import load_frequency_words, matches_word_groups
  File "/workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools/upstream/TrendRadar/trendradar/__init__.py", line 10, in <module>
    from trendradar.context import AppContext
  File "/workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools/upstream/TrendRadar/trendradar/context.py", line 12, in <module>
    from trendradar.utils.time import (
    ...<8 lines>...
    )
  File "/workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools/upstream/TrendRadar/trendradar/utils/__init__.py", line 6, in <module>
    from trendradar.utils.time import (
    ...<5 lines>...
    )
  File "/workspace/jingjing-duonaonao-batch2-20261111/05-wechat-tools/upstream/TrendRadar/trendradar/utils/time.py", line 11, in <module>
    import pytz
ModuleNotFoundError: No module named 'pytz'


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
```
包初始化级联依赖pytz缺失，未执行上游测试；主实验importlib只加载真实frequency.py本体，不能称为全应用通过。

## 在线RSSHub证据
旧批同日GET https://rsshub.app/github/issue/doocs/md 返回HTTP403，原始记录exercise/out/rsshub-public-result.json；没有用空结果顶替失败，也没有绕过访问限制。
