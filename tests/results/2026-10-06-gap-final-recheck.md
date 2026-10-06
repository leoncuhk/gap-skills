# 0.7.1 具体修复与清理：独立复核第1轮

判定：**本轮修复范围通过，无未解决的阻断发现。** 本轮只审 f62ba40 后已经指出的问题、清理恢复与最终安装内容，没有扩大为新一轮模型效果实验。旧审查、旧失败探针、初次审查脚本的路径归一错误记录均原样保留在父目录。

审查对象是未提交的实际工作树复制品，不是 `git archive HEAD`。复制时142文件，逐文件清单在 `working-tree-manifest.json`；验证结束后这些文件与仓库仍逐字节相同。文档后续补本回执、提交hash不自动改变已验证代码身份。

## 修复复核

- Quick prompt 现在明确改 `README.md` 的 `seperate`。复制 fixture 后实际改这一处并执行声明的 unittest：通过，仅 README 字节变化，无新文件、无流程产物。此为确定性执行冒烟，不是自然激活或新模型行为试验。
- Standard 示例读取 AGENTS 已定 accepted-identity 等规则，不再重复提问；示例标为 illustrative，去掉固定9/9冒充本次运行。
- `load_state` 显式验证顶层对象和非空对象revision列表；原失败 `[]` 与空revisions已修复，另测null/string/null-revisions/[null]，六种均JSON error、退出2、stderr空、输入字节未变。
- README 将经验条件精确为两个不同验证任务含至少一个forward；历史0.4结果改称historical baseline。两manifest均0.7.1。
- README正确区分单入口、四Python helper、离线HTML反馈、按任务由Agent编写的一般图示和宿主runtime；无Karpathy整套映射、无Thariq全量套件、无自动回传/浏览器验证的过度承诺。明确本地未发布版本和远端installer可能不同。

## 实际运行

从复制工作树运行 `python3 scripts/validate.py` 通过；`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` **58/58通过，4.028秒**。`claude plugin validate <copy>` 通过；Codex manifest路径与metadata静态核对通过。单独复制22文件skill到 `.agents/skills/gap`，21个内部链接都在folder内存在。

共24条命令满足各自预期退出码：repo validator、58回归、Claude manifest validator、Quick fixture、demo builder、installed helper init/check/record/text+HTML/feedback/use/use-result/revise/end，以及stale和六种无效输入控制。完整命令、stdout、stderr见 `result.json`，精简凭据见 `receipt.json`，可复现脚本为 `recheck.py`。

## 清理与证据链

历史归档 `tests/results/2026-10-06-legacy-examples-evidence.tar.gz`：14755 bytes，SHA256 `5c69c15ac74ed9f89ac21ef8202dbc76188db7977d6ccfed871c1270b0641886`。本轮另解到全新 `restored/`，40文件、68043源bytes均同时匹配manifest和 `git show f62ba401eedaad65ed80afece8ebf1ab00f262ed:<path>`。旧活跃目录已移除，当前MVP保留；4处文档导航改为恢复说明，validator无断链。

5个既有ignored evidence包SHA与初审完全相同。19个既有结果JSON/JSONL及5个结果txt共24文件逐字节未改。历史状态引用旧路径没有被改写为假通过；恢复说明明确完整旧树/匹配helper与ignored包的不同用途。未把“只有Git备份”说成完整运行包都在Git中。

## 固定身份及报告一致性

- installed checkpoint.py SHA256：`8755b729f5bc60137003ad98517b58326be49a6496716f6f674eb295cbcfeaeb`。
- 22文件skill manifest SHA256：`e55efefe3118f5e83b9e5bd19d8dd79ce545ed8872692dfb955096cf97ada856`。算法为对按path排序的 `{path,sha256,bytes}` 行列表以 `json.dumps(...,sort_keys=True,separators=(',',':'))` 编码后SHA256。
- `working-tree-manifest.json` 文件SHA256：`b8ec49077fab35a0aa83e38ab1fcf7a2257d2dd9bd72f4ddc34a210b897c7226`。
- `result.json` 文件SHA256：`0a04c50f3cdaa37d62f89dac17690230d0f580b162a5f4ef05a1816e7f65d84b`。
- `receipt.json` 文件SHA256：`f48a2c84becc9a4c75ec78165e371506d54fdf867a5fda1a36e364d8cd9c0d47`。

阅读 `tests/results/2026-10-06-gap-final.md` 及其新增独立报告：它明确冻结版审查与最终版待复核的区分，新forward仅支持一个范围内candidate trial，未宣称validated晋升、因果收益或模型优效；参考仓只读研究未伪称新增产品能力。本轮未跨仓复验上游clone身份，也未重跑新forward solver，其事实依据仍是链接的独立留存报告。本回执可以填入该报告的“最终复核”段；随后本地commit是否成功另需主线程验证。

边界保持：无网络、浏览器、headless、localhost、全局安装、外部模型或新agents；不能把本地包/DOM模拟通过写为自然激活、人类理解或节省工时已验证。意图轴与工程轴在本次具体差异内均通过，实际发布/外部动作不在本轮范围。
