# Canonical teacher feedback input

This is both the normal lesson report and the AI input. The teacher writes it once. Do not request mastery scores, error tags, JSON, a rubric, psychometric data, interests, or a second AI form.

```text
【课程】
[考试局/课程 + 科目 + syllabus code + level]
例：Cambridge IGCSE International Mathematics 0607 Extended

【日期 / 时间】
[YYYY.MM.DD｜北京时间 HH:MM–HH:MM]

【课程内容】
Topic：[本节章节]
本节练习/学习：[具体知识点或技能1]；[技能2]；[技能3]；[技能4]；至少四条

【课堂表现】
独立完成哪些技能：[学生无需提示可以完成的具体知识点；没有则写“无”]
提示后完成哪些技能：[需要提示才能完成的具体知识点；没有则写“无”]
提示类型：[概念 / 公式 / 步骤 / 符号 / 单位 / 图像 / 审题 / 其他；没有则写“无”]
尚不稳定/未完成：[仍然会错或不能完成的具体知识点；没有则写“无”]

【存在问题与建议】
具体问题：[写清楚“在哪一步、怎么错”，不要只写“粗心”“基础不好”；没有则写“无明显问题”]
下一步重点：[最多3项，按优先级写：1.___；2.___；3.___]

【课后作业】
[已有作业内容]

根据本次课后反馈自动生成个性化练习。
```

Minimum useful content is course identity, topic/lesson content, and observable performance. Accept ordinary wording variation and fewer than four skills when the scope is still clear. Use `无` for an empty skill/prompt field and `无明显问题` when no concrete error was observed; both parse as empty evidence, not literal skills. `下一步重点：由系统判断` is valid and triggers inference. The final sentence above is a valid generation trigger.

Bad classroom evidence: `课堂表现：表现不错。` Good evidence: `独立完成哪些技能：midpoint；distance` / `提示后完成哪些技能：gradient；equation of a straight line` / `提示类型：符号；步骤` / `尚不稳定/未完成：perpendicular gradient`.

Bad problem evidence: `比较粗心。` Good evidence: `坐标出现负数时，把 7-(-2) 写成 7-2；求直线方程时需要提醒先求 gradient。` If only vague wording is present, record the cause as unknown and use concrete performance evidence elsewhere.
