# Personal Voice Polisher · 个人文风润色

**版本 0.1.2 · 中文 Agent Skill · MIT**

让 AI 从你的自然表达和过往文章中了解你，再把已有中文文案整理成更符合你习惯的版本。职业身份、发言场景和不愿公开／表达的边界分别记录，不靠头衔猜文风。

适合希望把 AI 初稿、口述内容或已有文章整理成自己表达方式的人。每位使用者建立自己的档案，公开包不预装作者或其他人的个人文风。

这里的个人风格主要指**这个人怎么说话**：常用词、有表达作用的口头禅或口头表达、称呼、语气和句子节奏。会过滤停顿、卡顿和无意义语气助词；不同话题可以继续补充样本。文章逻辑、业务流程、分段套路和“先原因再结果”等组织方式不沉淀为个人讲话特征，按当次内容处理。

[下载 ZIP](https://github.com/yulindian/personal-voice-polisher/releases/latest) · [完整示例](examples/quickstart.md) · [更新记录](CHANGELOG.md) · [反馈问题](https://github.com/yulindian/personal-voice-polisher/issues)

## 三步上手

1. 把本文件夹安装到支持本地 Agent Skills 的工具中。
2. 说“帮我建立个人文风”，提供几段自己写的内容，或回答它提出的具体问题。已有文章时可以直接分析，不必做完整访谈。
3. 说“按我的风格润色下面这篇”，附文章和用途。以后可以提供新的片段、修改偏好或边界。

没有样本也能先按明确偏好试改；这时档案是待校准的，不能当作已准确学会你的风格。“学习”是维护档案并在写作时读取，不会训练模型。

## 安装：优先使用项目级目录

技能运行需要能读取 Markdown 指令的 AI 助手；文件工具用于跨会话保存档案。没有文件能力时，可以让助手输出档案文本，自行保存并在下次提供。不需要额外 API Key、数据库或 Python 依赖来润色。

### 不使用命令行：下载 ZIP

1. 打开 [Releases](https://github.com/yulindian/personal-voice-polisher/releases/latest)，下载 `personal-voice-polisher-0.1.2.zip` 附件。
2. 解压，得到 `personal-voice-polisher` 文件夹。
3. 按下表将整个文件夹放入准备写作的项目，不要只复制 SKILL.md。
4. 在该项目启动助手，使用对应调用方式。

| 工具 | 项目内的入口位置 | 开始调用 |
| --- | --- | --- |
| Codex | `.agents/skills/personal-voice-polisher/SKILL.md` | `$personal-voice-polisher 帮我建立个人文风` |
| Claude Code | `.claude/skills/personal-voice-polisher/SKILL.md` | `/personal-voice-polisher 帮我建立个人文风` |

例如 Codex 的目录是 `你的写作项目/.agents/skills/personal-voice-polisher/SKILL.md`，不要多套一层同名文件夹。只保留一个同名启用版本；更新前保留自己的修改，勿复制或覆盖个人档案。

目录和调用方式依据 [OpenAI 官方文档](https://learn.chatgpt.com/docs/build-skills) 与 [Claude Code 官方文档](https://code.claude.com/docs/en/skills)。如果没有出现技能，重启助手并检查启动项目和入口路径。代理行为试用在当前开发环境完成；Claude Code 安装说明已对照官方文档，尚未在该客户端实际测试。

### 有 Git：可选的个人级安装

希望多个项目共用技能时，在 PowerShell 或 macOS／Linux 终端执行对应工具的一条命令。它安装到用户目录，作用于多个项目；只在一个项目使用时采用上面的 ZIP 方式。

Codex：

```sh
git clone https://github.com/yulindian/personal-voice-polisher.git "$HOME/.agents/skills/personal-voice-polisher"
```

Claude Code：

```sh
git clone https://github.com/yulindian/personal-voice-polisher.git "$HOME/.claude/skills/personal-voice-polisher"
```

目标目录已存在时不要覆盖，先检查是否已安装。个人级安装后，各项目的数据仍分别保存，不会自动混用档案。其他工具按其支持的 Skill 目录加载整个文件夹，不代表已在所有宿主中测试。本仓库是文件夹形式的本地 Skill，不是商店插件。

## 开始使用

新用户：

```text
请用 $personal-voice-polisher 帮我建立个人文风。
我写给第一次接触 AI 的朋友，分享自己的使用过程。
你可以先问我一个具体问题，让我按平时说话的方式回答。
不要公开我的单位和家人经历，也不要把我写成权威专家。
```

已有文章：

```text
请用 $personal-voice-polisher 从下面三段我自己写的文章中提取风格。
先存一份初步档案，再用它润色最后那段文案，不必重新访谈。
样本：[粘贴内容或提供可读取的文件]
待润色文案：[粘贴内容]
```

后续润色：

```text
请用 $personal-voice-polisher，读取我的已有档案。
把下面这篇整理成我的表达风格，用于公众号。
保留事实、观点和限定条件，不补个人经历。
[正文]
```

Claude Code 使用 `/personal-voice-polisher` 代替示例中的 `$personal-voice-polisher`，后面的要求相同。档案在其他位置时直接指定文件；多个档案时说明使用哪份；不会要求把职业、收入等信息全部填完。

纠正与边界：

```text
“颠覆认知”这几个字不像我，以后都不用。更新档案。
这一次把“先看看”改成“先确认”，只用于这篇，不更新长期规则。
我的职务可以帮助你理解背景，但不要出现在公开文章里。
```

## 你会得到什么

- 建档：有原句依据的讲话措辞、口头表达候选、语气与句子口语感，以及独立的身份背景、个人边界、适用范围和一次试改。
- 润色：默认一版完整稿；需要时再给前后对照或修改说明。
- 反馈：明确长期要求直接更新，单篇要求只处理当前文章；普通接受不会被当成新的本人原创证据。

访谈一次问一个具体问题。你说“先这样”，就结束当前访谈并保留已有档案；后续有新文章或修改时再继续。暂时未想到的边界可以补充；一段试改获接受，不会扩大成所有文章都已认可。

例如“我觉得、比较、不太、比如说”有具体表达作用时可以作为候选；“嗯、呃”、卡顿和重复起头不会被复制成个人特色。不会把所有“就是／其实／的话／嘛／吧”一律删除，而是根据本句作用处理。没有足够证据时会说明尚未识别到稳定口头禅，不为了凑风格给你贴标签。

职业、组织角色和社会身份是可选背景。负责人可以用普通使用者口吻，老师也可以用同行交流口吻；读者关系影响语气，不意味着固定“身份腔”。不会要求收入或社会地位排名，也不会自动在文中公开身份。

## 档案与文章放在哪里

默认在**使用者当前项目**保存 `.voice-polisher/profiles/<profile-id>/profile.md`。这是用户数据，不在公共技能安装目录内。首次默认保存时，助手应确保项目的忽略规则覆盖 `.voice-polisher/`，并告诉你实际位置。你也可以明确指定其他文件夹或直接提供现有档案。

保存档案不等于发布。档案不自动同步到云盘；忽略规则仅帮助防止误提交，不提供多人访问控制。真实文章默认保留原处，只记录必要引用与非敏感短摘录。禁止公开的原事不应为了当“风格证据”再次写入档案。

多个档案分别保存，润色时指定所用档案。不混用别人的经历、语气或边界。分享这个 Skill 时，只分享公共技能文件；不要附带自己的 `.voice-polisher/`、文章或聊天记录。

## 示例与验证

完整的虚构人物建档及改写示例见 [试用示例](examples/quickstart.md)。所有人物和材料均为虚构，不代表真实使用者已认可相似度。

可选结构检查需要 Python 3.10+，仅用标准库。执行目录为本 README 所在文件夹：

```powershell
python -X utf8 -B scripts/check_package.py .
```

它检查必需文件、入口元数据和随包本地链接，成功退出状态为 0；不检测 AI 率，不判断文章是否像本人。无效目录或缺文件时退出 1 并说明位置；参数用错退出 2。开发源中的辅助回归测试可执行：

```powershell
python -X utf8 -B -m unittest discover -s tests -p test_check_package.py -v
```

公开仓库和 ZIP 包含虚构场景与维护测试，不包含真实个人档案、完整聊天或本地过程记录。维护者可以重新生成只含公共文件的 ZIP：

```powershell
python -X utf8 -B scripts/build_release.py .
```

产物位于 `outputs/personal-voice-polisher-0.1.2.zip`。白名单脚本只打包列明的公共文件，不执行上传；相同输入生成相同 ZIP。维护说明见 [CONTRIBUTING](CONTRIBUTING.md)。

## 常见问题与边界

- **每次都重新采访？** 提供已有档案，或从同一项目使用，先确认助手读到了档案。不要承诺在没有文件或上下文的情况下自动记住。
- **找不到文件？** 给出工具实际可读取的路径，或粘贴正文；读取失败不能凭标题生成样本分析。
- **稿子还是不像我？** 指出具体一句并写出自己会怎么说，通常比只说“再自然一点”更容易校准。
- **别人的文章能改吗？** 可以整理表达；其中经历、数据和观点保留归因，不改成自己的亲测和认可。
- **适用范围？** 第一版主要面向中文文章、社交文案和口播。不是独立软件、事实核查器、内容发布器或多人在线服务。相似度需要本人反馈，不能由模型自评分证明。

设计参考见 [方法来源](references/sources.md)。公共技能文件采用 [MIT 许可](LICENSE)；这不会改变使用者原始文章和个人档案的权属。
