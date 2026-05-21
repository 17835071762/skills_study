# 第一个 Skill

## 一、从使用现成 Skill 开始

### 1.1 准备工作

本文的演示基于 Claude Code 工具。Skill 的存放位置有两个选择：`~/.claude/skills/` 目录用于个人全局级别的技能，项目目录下的 `.claude/skills/` 用于项目专用的技能。

本章节在项目目录下进行测试。首先创建一个名为 `claude-test` 的目录：

```bash
mkdir claude-test
```

进入该目录，然后创建 skills 的目录与对应的 Skill 文件：

```bash
mkdir -p .claude/skills/python-naming-standard
```

### 1.2 编写配置文件 SKILL.md

在创建的目录下需要编写 SKILL.md 文件，这个文件相当于 Skill 的大脑，用来告诉 Claude 在什么时候应该使用这个技能。

以下是 SKILL.md 的示例内容：

```markdown
---
name: Python 内部命名规范技能
description: 当用户要求重构、审查或编写 Python 代码时，请参考此规范。
---

## 指令
1. 所有的内部辅助函数必须以 `_internal_` 前缀命名。
2. 如果发现不符合此规则的代码，请自动提出修改建议。
3. 在执行 `claude commit` 前，必须检查此规范。

## 参考示例
- 正确：`def _internal_calculate_risk():`
- 错误：`def _calculate_risk():`
```

字段要求说明：
- `name`：必须仅使用小写字母、数字和连字符组成，最长不超过 64 个字符
- `description`：Skill 的简要描述及其使用时机，最长不超过 1024 个字符

### 1.3 创建完成后的文件结构

创建完成后，项目的目录结构如下所示：

```
my-project/
├─ src/
│  └─ test.py              # 项目源码
├─ .claude/
│  ├─ skills/
│  │  └─ hello-world/
│  │     ├─ skill.md       # Skill 定义（YAML + Instructions，机器可执行）
│  │     └─ README.md      # Skill 说明（人类阅读，可选）
│  └─ config.yml           # Claude 项目级配置（可选）
├─ .gitignore
└─ README.md               # 项目整体说明
```

### 1.4 在终端中启动 Claude Code 并测试

在终端中执行以下命令启动 Claude Code：

```bash
claude
```

然后输入以下任务请求：

```
帮我写一个计算用户折扣的函数
```

Claude 会扫描已安装的 Skills，发现用户的请求涉及“Python 代码编写”，从而匹配到之前创建的 `python-naming-standard` 技能。根据 SKILL.md 中的要求，Claude 会生成如下格式的代码：

```python
def _internal_get_discount(user_score):
    # 计算逻辑...
    return discount
```

## 二、添加资源文件（可选功能）

### 2.1 可添加的目录类型

在 `.claude/skills/` 目录下可以额外添加以下三个目录来扩展 Skill 的功能：

| 目录名称    | 用途                                          |
| ----------- | --------------------------------------------- |
| examples/   | 存放示例文件                                  |
| references/ | 存放参考文档                                  |
| scripts/    | 存放可执行脚本（例如 Python 处理 PDF 的脚本） |

### 2.2 在 SKILL.md 中引用资源文件

添加上述目录后，可以在 SKILL.md 中通过以下方式进行引用：

- 查看示例 commit：`./examples/good-commit.txt`
- 运行脚本：使用工具执行 `./scripts/process.py`

## 三、官方市场

### 3.1 开放标准与官方仓库

除了自己编写 Skill 之外，还可以利用 2025 年末发布的 Agent Skills 开放标准。官方市场仓库地址为：https://github.com/anthropics/skills

从这个仓库可以下载预设的技能，例如 React 优化器、SQL 调优工具等。另外还有一个 Skill Creator 功能：可以对 Claude 说“帮我把我刚才教你的关于 Docker 的配置逻辑总结成一个 Skill”，Claude 会自动在相应目录中生成 Skill 文件。

### 3.2 注册插件市场

可以将 Anthropic 的 skills 仓库注册为 Claude Code 的插件市场。在 Claude Code 中执行以下命令：

```
/plugin marketplace add anthropics/skills
```

注册完成后，可以使用 `/plugin` 命令查看已注册的插件市场。

### 3.3 安装指定技能集的步骤

安装技能集的步骤如下：

1. 在 Claude Code 中输入命令浏览并安装插件：`Browse and install plugins`
2. 选择 `anthropic-agent-skills` 插件源
3. 选择 `document-skills`（文档技能）或 `example-skills`（示例技能）
4. 点击 `Install now`（立即安装）

### 3.4 通过命令直接安装插件

也可以通过以下命令直接安装上述两类插件：

```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

需要注意：使用插件方式安装的 skills，其目录位置在 `～/claude/plugins/marketplaces/` 下。插件安装完成后，需要重启一下 Claude Code 才能生效。

### 3.5 使用已安装的插件技能

使用的时候只需在指令中提及技能名称即可调用。例如安装 `document-skills` 插件后，可以向 Claude Code 下达以下指令：

```
使用 PDF 技能提取 path/to/some-file.pdf 文件中的表单字段
```

或者创建一个 PPT：

```
创建一个 Agent Skill 的演示文稿
```

可以看到系统调用了 `/document-skills:pptx` 技能开始生成，完成后会告知生成文件的存放位置。