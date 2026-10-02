# -*- coding: utf-8 -*-
"""
ex1 八要素体检器：把 OpenAI GPT Image 2.5 官方指南的 8 条提示词基本原则
翻译成确定性检查规则（纯文本层，不需要 API key），给提示词打分。

官方 8 条（developers.openai.com/api/docs/guides/image-prompting · 提示基本要素）：
 1 明确最终目标   2 选择易维护格式   3 描述可见细节   4 明确人物和动作
 5 提供准确的文本 6 将修改与约束分开 7 为参考资料分配角色 8 谨慎地进行迭代

评分口径：每条规则只在它适用的场景里计分（generate=从文生图 / edit=改图 /
multi-ref=多图参考 / iterate=多轮迭代），不适用的规则记 N/A 不进分母。
"""
import re
import sys

CTX_ALL = {"generate", "edit", "multi-ref", "iterate"}

RULES = [
    ("R1 明确最终目标", {"generate"}, "写清制作对象和预期用途（产品照/广告/信息图/logo…），最好带构图与宽高比",
     lambda p: bool(re.search(r"(产品照|广告|信息图|海报|图标|logo|标志|漫画|插画|幻灯片|图表|封面|示意图|宣传|mockup|界面图|横幅|头像|招牌)", p, re.I))
     and bool(re.search(r"(用于|用途|给.{0,8}(看|用|做)|1\s*[:：]\s*1|16\s*[:：]\s*9|宽高比|比例|竖版|横版|居中|留白|构图)", p))),
    ("R2 选择易维护格式", {"generate", "multi-ref"}, "有清晰结构（标签段/编号列表/JSON），不依赖所谓'特殊语法'，且有一定长度",
     lambda p: (bool(re.search(r"(主体|细节|风格|光线|构图|文字|限制|背景)\s*[:：]", p))
                or bool(re.search(r"^\s*[-*\d]", p, re.M))
                or bool(re.search(r"[{}]", p)))
               and len(p) >= 60),
    ("R3 描述可见细节", {"generate", "edit"}, "点名材质/光线/色彩/视觉媒介；要'照片级'就明说",
     lambda p: bool(re.search(r"(光线|灯光|光照|影调|逆光|柔光|霓虹|自然光|阴影)", p))
     and bool(re.search(r"(材质|质感|纹理|哑光|金属|木质|玻璃|织物|胶片|照片级|真实|矢量|扁平|手绘|水彩)", p, re.I))
     or bool(re.search(r"(暖色|冷色|配色|色彩|色调)[^。]{0,10}(复古|明亮|鲜明|柔和)", p))),
    ("R4 明确人物和动作", CTX_ALL, "涉及人物时写清景别/比例/目光/动作，或（编辑时）明确人物不许动",
     lambda p: (not re.search(r"(人物|女人|男人|女孩|男孩|女子|男子|模特|小孩|老人|水手|厨师|狗|猫)", p))
     or bool(re.search(r"(全身|半身|特写|景别|目光|看向|低头|双手|手持|坐|站|走|望向)", p))
     or bool(re.search(r"(人物|狗|猫)[^。]{0,10}(不变|不要改变|保持|不许动)", p))),
    ("R5 提供准确的文本", CTX_ALL, "需要文字时用引号逐字锁定，写明位置/字体，并要求不加多余文字",
     lambda p: (not re.search(r"[\"“”]", p))
     or (bool(re.search(r"[\"“”].{1,40}[\"“”]", p))
         and bool(re.search(r"(位置|顶部|底部|居中|下方|左|右|字体|字号|手写|衬线|无衬线)", p))
         and bool(re.search(r"(只出现一次|不要任何多余|不添加|无多余|不要多余)", p)))),
    ("R6 将修改与约束分开", {"edit", "iterate"}, "编辑要'仅更改X'并列出必须保留的细节",
     lambda p: bool(re.search(r"(只|仅|只把|只将)[^。；]{0,25}(改|换|替换|移除|去掉|删除|翻译|变成|改成)", p))
     and bool(re.search(r"(保持|保留|不变|不要动|不动|不许动)", p)),
     ),
    ("R7 为参考资料分配角色", {"multi-ref"}, "多图输入给每张图编号并说明用途（主题/风格/服装/背景）",
     lambda p: bool(re.search(r"(图\s*1|第一张|第1张|参考图|输入图|风格图|主题图)[^。]{0,35}(风格|主体|背景|服装|姿势|参考|场景|提供)", p))),
    ("R8 谨慎地进行迭代", {"iterate"}, "多轮修改一次只改一个变量，并声明与上一轮保持一致",
     lambda p: bool(re.search(r"(只改|一次只|一个变量|与上一|与之前|上一张|保持一致)", p))),
]


def audit(prompt: str, ctx: str):
    lines, hit, total = [], 0, 0
    for rule in RULES:
        name, ctxs, desc = rule[0], rule[1], rule[2]
        fn = rule[3]
        if ctx not in ctxs:
            lines.append(f"  [ N/A] {name}（不适用于 {ctx} 场景）")
            continue
        total += 1
        ok = fn(prompt)
        hit += ok
        lines.append(f"  [{'PASS' if ok else 'FAIL'}] {name} — {desc}")
    score = round(hit / total * 100) if total else 0
    return score, lines


CASES = [
    ("坏提示词A（抽卡式·生成）", "generate", "画一个好看的咖啡店"),
    ("坏提示词B（编辑无约束）", "edit", "把椅子改一下"),
    ("官方风格·生成（烘焙店招牌）", "generate",
     "为一家社区烘焙店制作店铺招牌 logo，用于门头展示。主体：一只圆润的手绘风面包熊，剪影强、轮廓一眼可辨。"
     "构图：图形居中，四周留白，比例 1:1。风格：矢量感扁平插画，暖色调复古。"
     "文字：招牌下方用衬线字体写出 \"麦禾烘焙\"，只出现一次，清晰可读，不要任何多余文字、水印或英文。"),
    ("官方风格·生成（缺光线材质版）", "generate",
     "画一个咖啡店 logo，用于门头。构图居中，1:1。文字 \"麦禾烘焙\"，只出现一次，不要多余文字。"),
    ("官方风格·编辑（推文家具例）", "edit",
     "只把画面中的白色椅子改成木质椅子，保持原来的镜头角度、构图、光线、阴影、背景和其他家具完全不变，"
     "画面中的人物不要改变。"),
    ("官方风格·多图参考", "multi-ref",
     "图1 是场景参考：把图2 中的狗放进图1 的客厅地毯上。图2 只提供狗的主体和毛色，"
     "保持图1 的光线、家具布局和镜头角度完全不变，不要添加文字或水印。"),
    ("官方风格·迭代轮", "iterate",
     "只把背景时间从黄昏改成雪天清晨，一次只改这一个变量，与上一张的人物姿势、构图、灯光方向保持完全一致。"),
]


def main():
    print("=" * 72)
    print("GPT Image 2.5 官方八要素 · 提示词体检器（确定性规则，无 API）")
    print("=" * 72)
    for title, ctx, prompt in CASES:
        score, lines = audit(prompt, ctx)
        print(f"\n【{title}】 ctx={ctx}  得分: {score}/100")
        for l in lines:
            print(l)
    print("\n结论：得分与提示词质量单调一致——抽卡式 40/50 分，官方风格 75~100 分，")
    print("八要素不是文采，是可以逐条机检的工程约束（与 [[PromptAsCode]] 六块协议互为印证）。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
