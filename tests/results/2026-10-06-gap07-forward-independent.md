# 新任务正向试用：独立验收

本次只补了一个可执行缺口：把原候选JSON及其绑定失败来源逐字节带入一个此前未参与调试的新同范围任务，实际trial并以新结果闭合。没有新增baseline，没有重复运行求胜，没有改产品。

## 已补齐的证据

一个fresh solver（请求gpt-6-astra/high/fork none，上限12calls/8分钟）处理15条新的replacement snapshots。独立oracle在启动前冻结，未给solver或父线程。保留请求B22=4、C33=7、D44=9、E55=6、F66=5、G77=0，共31；取消A11。完整身份、整数revision先后、取消/重新批准、同team不同request、批准零数量均核对正确。旧候选中的Q1/Q2/Q4及17被明确解释为历史值，而非新任务目标。

独立机械检查22项通过：原task/input/candidate/incident/安装skill字节保持；新task ID及同task scope/use/result匹配；receipt引用当前真实产物；新副本删除旧results后运行solve.py仍生成完整正确结果。

独立阅读并重放`check.py --exercise`，正向31通过，last-row=25、lexical=49、先筛approved=39、team-collapse=11四种错误解释均以exit1被拒绝。随后在另一复制任务中实际执行init、use与use-result，闭合同一新use，候选仍candidate且validations为空。不是仅凭“读过经验”或命令字符串判通过。原历史solver调用的全平台身份仍未知，本审查实际重放是已执行的本地证据。

## 未被证明或未被执行

这证明限定范围经验能在一个新实例真正trial并留存可重放结果，不能证明经验导致更好结果：当前policy也直接给出选择规则，且没有baseline。没有相对效率估计、真实业务收益、validated apply或候选晋升。原candidate及validations=[]按任务要求不改，不能把这份报告自动写成晋升许可。浏览器、真人理解、backend、tokens、精确时间和费用均未验证；8calls仅solver自报。

## MVP核清

当前repo MVP只读静态语义21项通过：Mei、rush68积分/周一setup、standard17积分/周二after setup、51差价、17:00 deferral、明确无date/timezone以及未授权/反馈不授权都默认可见。详细原文及diff和原始5个来源的全文SHA/target一致，三模式沿用原Observation。这里只验证静态内容与引用一致性，没有浏览器或真人理解实验。凭据为`mvp-static-semantic-review.json`。

## 冻结与复跑

`frozen/acceptance-manifest.json`在启动前锁定criteria、expected、输入manifest、evaluator和prompt；独立验收器先通过1个已知可解正控与4个红控。`workspace/`为唯一实际solver原产物，未替其修补。`reports/actual-mechanical.json`、`actual-verifier-lifecycle-replay.json`和`independent-forward-result.json`为独立结果。运行`python3 replay_all.py`重放验收资格、完整结果和真实trial生命周期；不调用模型。
