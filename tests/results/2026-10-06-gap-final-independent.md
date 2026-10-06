# gap-skills 独立全仓审查（冻结 f62ba40）

审查对象：`f62ba401eedaad65ed80afece8ebf1ab00f262ed`，170 个 tracked 文件。审查中仓库只读；全部新增报告、归档副本、测试产物保存在本目录。主线程随后做的清理修复不自动继承本结论。

结论：单 skill 包自包含、本地运行入口与现有 57 项回归通过；没有发现当前有效输入路径上的阻断运行缺陷。存在需要修正的测试/示例一致性问题、一个低风险错误处理缺陷及两处文档歧义。没有证明自然激活、浏览器交互、人类理解或总体效率。

## Findings（不混淆产品运行与测试契约）

1. **P2，Intent/spec，阻断声明的 Quick L2 场景复跑**：`tests/cases/workflows.json:6` 要求改 CLI invalid-port 提示及已有测试，指定的 `tests/fixtures/quick-project` 只有 README 拼写错误 `seperate`、邀请邮箱归一函数和身份测试，没有 CLI、端口或 approved wording。现有测试只检查 fixture 的 tests 通过，没有执行该 prompt。最小修复是把 case 对齐现有 README typo 及历史 Quick 场景；不需要新建 CLI。
2. **P2，Intent/spec，非阻断文档错误**：`EXAMPLES.md:29` 左右示例称是否允许再次邀请 accepted identity 尚未指定并向用户提问，但 `tests/fixtures/standard-invitation/AGENTS.md:8` 已明确必须报 already-accepted 错误。与“facts from repository”的宣称冲突。应在示例中展示读取既定规则，或明确这是另一个尚未指定政策的独立假设例；当前文档将其作为可执行 fixture 演示容易误导。
3. **P3，Engineering，非阻断有效输入运行**：`skills/gap/scripts/checkpoint.py:97` 的 state 容器和 revisions 没有结构校验；`state=[]` 抛 AttributeError，`revisions=[]` 抛 IndexError，两者 stderr traceback、退出 1，stdout 为空。`delivery.md` 把无效输入定义为退出 2；当前 caller 可能把损坏 checkpoint 误作普通待补证据，并无法解析 JSON。`probes.json` 保存复现。建议显式验证顶层对象和非空 revision 列表；不建议广泛吞掉所有异常。
4. **P3，Intent/spec，非阻断说明歧义**：`README.md:102` 写 separate regression/forward validation，实际 `experience.py:109–145` 要求两任务且至少一个 forward，允许两个 forward；`retrospective.md:67` 与实现一致。`probes.json` 的两个 forward 控制被接受为 evidence_recorded（仍 unverified outcome）。建议 README 使用精确下限，不凭简写新增门槛。
5. **P3，导航**：`README.md:126` 把 2026-08-27 0.4.0 结果称 current evidence，而同页已有 0.7.0；应标 historical baseline，保留历史结果本身。

对意图轴：实现的单入口、按需参考、事实先行、状态/回执、离线反馈边界基本一致；上述例子/用例需要修正。对工程轴：有效输入冒烟与回归通过；异常输入处理需要小修。独立性：这是主实现上下文外的只读审查，但为同一平台模型环境；没有伪称另一个模型或真实人类验收。

## 目录覆盖及保留/清理判断

逐文件路径/字节/哈希见 `inventory.json`；所有 JSON、JSONL 和 Python 文件解析检查见 `static-checks.json`。

| 类别 | 覆盖 | 判断 |
|---|---|---|
| 顶层文档/授权 | AGENTS、README、EXAMPLES、CHANGELOG、NOTICE、LICENSE | 读入口、来源、版本和限制；保留，修正文档不一致 |
| 平台/CI | `.claude-plugin`、`.codex-plugin`、`.claude/settings.json`、`.github/workflows`、`.gitignore` | 两 manifest 0.7.0、同一skill；Claude settings只作用开发仓，不随单folder安装；CI与AGENTS verify一致 |
| `skills/gap`（22文件） | 1入口、9参考、7assets、1metadata、4 Python helper | 全部读代码/文本，21个本地链接在复制folder内部存在；无外部repo imports；保留 |
| `scripts`（1） | validator | 校验包装、链接及关键措辞；措辞测试不是行为证明；保留 |
| `tests/cases`（2） | 20 activation、9 workflow | positive/negative矩阵有定义；未运行当前模型自然激活；Quick prompt/fixture不一致 |
| `tests/fixtures`（27） | Quick/Standard/review/collaboration | 静态读约束/API；现有测试实际跑fixture；保留 |
| `tests/evaluators`（3）、patch（1）、reference（7） | 已植入失败与known-green | 隐藏判据红绿能力实际由suite运行；只是本地结果检查，不是模型行为实验 |
| `tests/test_*.py`（5） | 57回归 | 全部实际通过；包含CLI、文件身份、symlink、反馈、经验、brief和非浏览器JS模拟 |
| `tests/results`（44 tracked） | 多轮计划、失败、独立审查、限定、回执 | 属于证据，不按冗余删除；绝对旧路径保持历史意义 |
| `examples/evidence-review`（46 tracked） | builder、旧mvp、usage acceptance、当前gap07展示 | 当前/历史混陈可整理；旧产物不是垃圾，需归档与恢复导航后才移出活跃展示 |
| ignored本地产物 | pycache、5个证据tar.gz | cache可重建；5个证据包不能删除，Git并不保存它们 |

具体可清理候选：`scripts/__pycache__`、`skills/gap/scripts/__pycache__`、`tests/__pycache__`及fixture下同类缓存，均属于解释器可再生派生物，不需Git恢复；本轮没有删除。旧 `examples/evidence-review/mvp/` 与 `usage-acceptance-2026-10-06/` 可从活跃目录归档，但必须逐文件比对 `f62ba40`、归档SHA并异地解包核验，说明从Git或归档恢复的准确命令。`package.tar` 是本轮对整个固定commit执行 `git archive` 的副本，本地证据包另留原处。

不能当成临时文件：5个 ignored evidence tar.gz、历史失败/计划/独立结论、before/state/旧回执。`smoke.json` 列出5包字节数、sha256和tar成员数；4个正文已声明哈希均匹配，所有包可读且无tar链接。未对5包所有业务流程重新运行，避免把历史归档验证扩大为新行为实验。

移除旧示例后需更新当前README/EXAMPLES及 `tests/results/2026-10-06-batch2.md:25,27`、`2026-10-06-usage-acceptance.md:47,60` 的导航链接。`batch2-state.json` 绑定旧路径，应保留字节，明确历史checkpoint要恢复固定树/包再重放，不能说HEAD仍可直接check历史状态。

## 实际运行证据

- `validate.txt`：`PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate.py`，通过1 skill/9 references/7 assets/2 manifests。
- `tests.txt`：`python3 -m unittest discover -s tests -v`，57/57通过，3.841秒。本地测试含Standard/review/collaboration的失败基线和成功参考；没有外部模型。
- `audit.py` / `smoke.json`：从固定commit打包并解包，单独复制 `skills/gap` 到隔离 `.agents/skills/gap`，未依赖仓根；16条实际命令通过预期返回码，包括 `claude plugin validate <copied-package>`、独立副本validator、builder、installed helper的init/check/record/text+HTML/feedback/use/use-result/revise/end，及源变更后的check=1和feedback=2。
- `task/review.html`、`task/review.txt`：本次真实本地生成；反馈合成输入明确标记，不是用户批准。
- `probes.py` / `probes.json`：两种无效状态异常及两个forward验证控制。
- `static-checks.json`：170 tracked文件清单覆盖；JSON/JSONL解析和Python AST无语法错误。

本轮audit脚本初次把macOS `/tmp` 与解析后的 `/private/tmp` 直接比较，导致自包含assert误报；修正审查脚本为统一resolved path后通过。此为审查工具路径比较错误，不是gap缺陷。未重复或隐去任何产品失败。

## 只装 gap 到底包含什么

| 能力 | 当前包含程度 |
|---|---|
| 单一用户入口 | 是，`skills/gap/SKILL.md`，内部9参考由Agent按需读取 |
| Karpathy经验 | 当前固定仓全文没有Karpathy引用或机制映射；不能因为有小改动/验证/自主循环就声称装了整套Karpathy经验，也未捆绑其runtime |
| Thariq unknown discovery | NOTICE明确列出Finding Your Unknowns及机制；discovery内有事实/决策/品味/盲区、差异原型、来源作为行为规范。属于抽取方法，没有上游完整suite或全量覆盖证据 |
| Thariq HTML/沟通 | NOTICE与communication内有按阅读任务选择text/diagram/HTML的指导；已内置checkpoint离线HTML视图及JSON反馈导出/回读 |
| Diagram | 有何时选图、图作为同源视图的指导；一般Mermaid/SVG/图布局由Agent生成，没有内置通用diagram编辑器或自动图引擎 |
| HTML互动 | 内置折叠证据、来源跳转、筛选判据、反馈准备/下载，离线stdlib生成；无需服务器/CDN/其他skill；实际浏览器交互本轮未测 |
| 自主执行/记忆/批准 | helper只核声明的文件连续性及回执，不运行Agent、不认证reviewer、不发布、不授权、不自动学习晋升 |
| 安装位置/runtime | folder/manifest和本地helper已验证；真正注册、自然激活由Claude/Codex等宿主决定，未全局安装，未调用模型验证activation |
| demo builder | repository-only；不随单skill folder搬走，不妨碍installed view/feedback |

未验证：npx联网installer、远端CI、平台自然激活、跨模型有效性、生产或外部动作、完整上游经验映射、真人理解/节省工时。本轮没有调用浏览器、headless、localhost或替代工具绕过既有浏览器拒绝；HTML/JS是静态及现有Node模拟检查。

本报告完成的是冻结版本的独立审查与本地冒烟，不代表主任务的修复、清理、同步或所有目标已经完成。
