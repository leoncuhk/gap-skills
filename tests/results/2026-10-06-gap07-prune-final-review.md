# Prune4：最终格式修复独立复验

唯一源码差异为`review_view.py`详细text空回执行增加`.rstrip()`；已比对prune3副本，未变业务、校验、状态、经验或观测计算。

24项独立回归、两实际增强产物默认核心/完整证据/同观测/来源失效检查、105个Node引用定位模拟全部通过。开发与迁移默认text和HTML相对prune3逐字节不变；两个details各少1字节，仅移除human空`Evidence:`行尾空格，未删内容或限定。

开发details为14,274字节，三个模式总量47,214字节；迁移details为20,316字节，三模式总量60,047字节。其余比例与`independent-prune-review.md`相同，迁移三模式总量仍高于原两文件；不宣称人时、理解或总体成本收益。

原四臂证据包与prune3补充包SHA均保持不变，prune3文件和报告保留为历史。旧24验收仅在独立补充副本把原文断言切至显式details，另加默认核心检查；compact摘要版本ID缺失的修复记录继续保留于前份报告。

当前安装副本manifest SHA256：`aecc74723873a540a6c3fedddb976cd8f3cbb530ef93be2e9c17cc7e1183eda6`。结果见`prune4/comparison.json`、`compat24.log`、`node-disclosures.json`、`minimal-delta.json`。最终打包重放为独立新目录中的原包+补充包叠加验证，无新solver或浏览器。
