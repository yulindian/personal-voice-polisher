# 维护与改进

此 Skill 的公共方法与使用者的个人档案分离。请使用虚构或可公开的最小样本报告问题，不在 Issue、Pull Request 或提交中附带真实档案、私人文章、单位／客户信息或完整聊天记录。

## 本地验证

运行时是纯 Markdown，不需要 Python。以下命令用于维护和打包，要求 Python 3.10+，无第三方依赖。执行目录为仓库根：

```text
python -X utf8 -B scripts/check_package.py .
python -X utf8 -B -m unittest discover -s tests -p "test_*.py" -v
python -X utf8 -B scripts/build_release.py .
```

最后一条在 `outputs/` 生成按版本命名的 ZIP，不会上传或发布。脚本只复制明确列出的公共文件；缺文件、非法版本或输入链接越界时失败。相同字节的输入生成相同 ZIP；不会把整个工作目录打包。新增公共文件时同步修改 `scripts/build_release.py` 中的 `PUBLIC_FILES`。

`.tmp/` 用于测试临时项目，`outputs/` 为可重建的交付物；二者都不应提交。不得仅凭忽略规则认定已跟踪的文件不会被提交。个人运行数据不得写进技能安装目录。

## 修改 Skill 时验证什么

结构检查只证明入口、必需文件和本地引用有效，不证明文风像本人。行为改动至少用 [虚构场景](tests/scenarios.md) 做实际试改，重点核对：

- 事实、数字、限定、否定和外部作者归因是否保留。
- 没有把风格样本中的经历、观点或建议移进目标文章。
- 只沉淀讲话语言，不把文章逻辑、先后步骤或业务流程归为个人风格；有作用的口头表达与转写填充词应分开。
- 身份背景不替代本人表达证据，角色变化不混用个人档案。
- 个人边界与核心内容冲突时只询问必要取舍，不默认公开或解除边界。
- “先这样”结束访谈，单段接受不扩为所有文章都已认可。

变更时同步 `SKILL.md` 的 `metadata.version`、README 和 [更新记录](CHANGELOG.md)。GitHub Actions 会执行结构、单测和打包检查；真人风格相似度仍依赖实际使用者的具体反馈。

## 提交反馈

请说明使用的宿主、Skill 版本、预期行为、实际行为，以及一小段虚构复现材料。可通过仓库的 [Issues](https://github.com/yulindian/personal-voice-polisher/issues) 提交。安装兼容性和模型表现可能不同，请勿仅用检测器分数判断改动是否有效。
