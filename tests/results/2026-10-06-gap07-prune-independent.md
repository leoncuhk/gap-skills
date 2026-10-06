# 默认阅读面删减：独立复验

结论：本次最小删减保留了原验收要求的证据可取得性与观测绑定，默认阅读面明显缩小。独立24项兼容回归、两组实际增强产物的核心/完整证据检查，以及105个实际引用链接的Node模拟均通过。该结果只是文本量和定位机制证据，不是人时、费用或理解提升证据。

这是四臂实验之后的确定性renderer修订验证，不是新增solver对照实验。没有改变原brief/state、公式、schema、经验规则或既有四臂产物；原321,627字节证据归档SHA仍为`8123942cae5006a796d090857f1e8900d5b695486d2ac52c691b85a568205806`。

## 保留了什么

默认text/HTML完整呈现实际summary、逐项impact与不变对象、claim类型、判据claim/status/note、独立验收边界、全部owner/question/option/consequence/tradeoff/deferral和limits。独立检查覆盖开发23项核心字段、迁移32项；没有只剩判据ID。

完整text通过`view --details`取得；HTML同一文档内将原文、diff、hash与回执折叠。完整text仍包含所有原文及差异、引用path/line/full SHA/target和回执关系，重复证据集中一次。开发5个、迁移15个唯一引用逐项核对通过。compact/details/HTML与原冻结视图的observation完全相同；反馈仍不改state、不授权，引用来源的未引用行变化仍拒绝旧反馈。

本次审查发现并修复一项小但实质的回归风险：初版compact text完全省略observation，只让人重新生成details，独立摘要无法辨认其版本。现默认底部保留完整Observation和Brief path，并要求详情与摘要观测一致，否则重查。未为减少文字移除关键限定。

## 实测大小

| 指标 | 开发冻结版 → 删减版 | 迁移冻结版 → 删减版 |
|---|---:|---:|
| 默认text字节 | 19,721 → 4,585（-76.8%） | 20,737 → 6,293（-69.7%） |
| HTML初始展开文本字符代理 | 8,793 → 4,537（-48.4%） | 12,562 → 5,888（-53.1%） |
| HTML文件字节 | 36,295 → 28,355 | 37,835 → 33,438 |
| 默认text+HTML，均2文件 | 56,016 → 32,940字节 | 58,572 → 39,731字节 |
| 额外生成完整details后，3文件总量 | 47,215字节 | 60,048字节 |

迁移案例若同时保存三个模式，总字节略高于原两文件，不能宣称总存储或总体工作成本下降。HTML代理排除script/style/head/noscript，按details的open属性推算初始展开文本，并非浏览器实际排版、屏幕面积或阅读时间。

## 定位与验证证据

Node根据两个真实生成HTML的DOM树模拟点击：开发5个source链接+46个receipt链接，迁移22+32，合计105。全部打开正确的details祖先（最深两层），设置目标焦点并滚动到目标；同一页面反馈payload仍带正确观测。标准anchor保留手动可追查路径，无JS有手动展开提示。未使用浏览器，没有实际键盘驱动、布局/视觉或人类理解试验；直接带fragment初次打开的自动展开不是本次验证对象，当前保证为页面内引用激活。

24项旧独立验收只在本补充副本把原文检查明确切换至`details=True`，保留全部原文、失效与反馈判据，再增加默认核心可见检查；旧验收脚本与原归档未改写。源码AST比对显示brief校验不变，experience.py逐字节不变，checkpoint仅新增view参数与render_text传参；变更范围为renderer和相关communication说明。

## 产物

- `prune3/comparison.json`：指标与核心/原文/绑定结果。
- `prune3/compat24.log`：24/24兼容验收。
- `prune3/node-disclosures.json`：105次引用定位与反馈绑定模拟。
- `prune3/scope-review.json`、`reviewed.diff`：范围审查。
- `prune3/dev/compact.txt`、`details.txt`、`review.html`：可查看开发样例；迁移同目录结构。
- `prune3/skill-manifest.json` SHA256：`5fb72224795cb7e6dda88016a78210f10cf1f1e84a76577cd61db836365ed811`。

没有新阻断发现。这里的“通过”限于上述冻结语义、证据保全、默认可见性和本地机制检查，不扩展为总体目标达成。
