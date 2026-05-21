# 使用现有 Skills

## 前置准备：GitHub SSH 配置（首次使用需要）

在安装官方 Skills 之前，需要先配置 GitHub SSH 连接，否则可能会遇到“Host key verification failed”错误。

### 第一步：生成 SSH 密钥

打开 **CMD**（命令提示符），执行以下命令（将邮箱替换为你的 GitHub 注册邮箱）：

```bash
ssh-keygen -t ed25519 -C "你的QQ邮箱@qq.com"
```

系统会询问三个问题，**全部直接按回车**：
- 密钥保存位置：直接回车（使用默认路径）
- 输入密码：直接回车（不设置密码）
- 确认密码：直接回车

成功后会显示：
```
Your identification has been saved in C:\Users\用户名/.ssh/id_ed25519
Your public key has been saved in C:\Users\用户名/.ssh/id_ed25519.pub
```

### 第二步：查看并复制公钥

执行以下命令显示公钥内容：

```bash
type C:\Users\你的用户名\.ssh\id_ed25519.pub
```

会输出一串以 `ssh-ed25519` 开头的文本，**选中全部内容，按右键复制**。

### 第三步：添加公钥到 GitHub

1. 登录 GitHub（https://github.com）
2. 点击右上角**头像** → **Settings**
3. 左侧菜单点击 **SSH and GPG keys**
4. 点击绿色按钮 **New SSH key**
5. 填写信息：
   - **Title**：输入 `Claude Code`（便于识别）
   - **Key type**：保持默认 `Authentication Key`
   - **Key**：粘贴刚才复制的公钥内容
6. 点击 **Add SSH key** 保存

### 第四步：验证 SSH 连接

在 CMD 中执行：

```bash
ssh -T git@github.com
```

首次连接会提示确认指纹，输入 `yes` 回车。

如果看到以下信息，说明配置成功：

```
Hi 用户名! You've successfully authenticated, but GitHub does not provide shell access.
```

## 官方技能仓库

目前市场上已经有很多大家编写好的 Skills。其中最重要的是 Anthropic 官方提供的 Claude Skills 仓库。

**官方仓库地址**：https://github.com/anthropics/skills

该仓库是 Anthropic 官方 Claude 技能合集，配套 Agent Skills 开放标准，支持动态加载拓展 AI 专项能力。技能覆盖以下领域：

- 设计
- 开发
- 企业办公
- 全品类文档编辑

多数技能开源，文档底层能力可供源码参考。

## 安装官方插件市场

完成 GitHub SSH 配置后，在 Claude Code 中执行以下命令：

```
/plugin marketplace add anthropics/skills
```

如果遇到网络问题，也可以使用 HTTPS 方式：

```
/plugin marketplace add https://github.com/anthropics/skills
```

安装完成后，可以使用 `/plugin` 命令查看已安装的插件市场。

## 安装指定技能集

### 方式一：通过界面操作

1. 浏览并安装插件（Browse and install plugins）
2. 选择 `anthropic-agent-skills` 插件源
3. 选择以下技能包之一：
   - `document-skills`（文档技能）
   - `example-skills`（示例技能）
4. 点击「立即安装」（Install now）

### 方式二：通过命令直接安装

```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

### 插件安装位置

使用插件安装的 skills 位于 `~/claude/plugins/marketplaces/` 目录下。

### 重启生效

插件安装完成后，**需要重启 Claude Code** 才能生效。

## 使用已安装的 Skill

使用的时候只需在指令中提及技能名称即可调用。

### 示例一：使用 PDF 技能

安装 `document-skills` 插件后，可以向 Claude Code 下达指令：

```
使用 PDF 技能提取 path/to/some-file.pdf 文件中的表单字段
```

### 示例二：创建 PPT

```
创建一个 Agent Skill 的演示文稿
```

系统会调用 `/document-skills:pptx` 技能，然后开始生成，最后告诉你生成的文件位置。

## Agent Skills 相关资源

| 资源说明                                        | 链接                                                         |
| ----------------------------------------------- | ------------------------------------------------------------ |
| Skill 聚合入口                                  | https://skills.sh/                                           |
| Skills 市场（中文界面）                         | https://skillsmp.com/zh                                      |
| Agent Skills 官方标准站点                       | https://agentskills.io                                       |
| Anthropic 官方工程文章（Agent Skills 实战理念） | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills |
| VS Code Copilot Agent Skills 文档               | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| Anthropic 官方 Skills GitHub 仓库               | https://github.com/anthropics/skills                         |
| Claude 技能精选列表（Awesome 系列）             | https://github.com/ComposioHQ/awesome-claude-skills          |
| 软件开发自动化工作流 Skills 集合                | https://github.com/obra/superpowers                          |
| 自动生成 Skill 的 Skill（官方示例）             | https://github.com/anthropics/skills/tree/main/skills/skill-creator |

## 补充：VS Code 中的 Agent Skills

根据 VS Code 官方文档，Agent Skills 也可以在 VS Code 中使用，与 Claude Code 遵循相同的开放标准。

### VS Code 中的 Skill 存储位置

| Skill 类型                    | 存储位置                                                     |
| ----------------------------- | ------------------------------------------------------------ |
| 项目 Skills（存储在仓库中）   | `.github/skills/`、`.claude/skills/`、`.agents/skills/`      |
| 个人 Skills（存储在用户目录） | `~/.copilot/skills/`、`~/.claude/skills/`、`~/.agents/skills/` |

### SKILL.md 文件格式

`SKILL.md` 是 Markdown 文件，包含 YAML 前置元数据：

```markdown
---
name: skill-name
description: 技能描述
---

# 技能指令

详细说明...
```

**必需字段**：

| 字段          | 说明                                                 |
| ------------- | ---------------------------------------------------- |
| `name`        | 唯一标识符，仅允许小写字母、数字和连字符，最大64字符 |
| `description` | 技能描述，说明能力和使用场景，最大1024字符           |

**可选字段**：

| 字段                       | 说明                                          |
| -------------------------- | --------------------------------------------- |
| `argument-hint`            | 聊天输入框中显示的提示文本                    |
| `user-invocable`           | 是否显示为斜杠命令，默认 true                 |
| `disable-model-invocation` | 是否禁止 AI 自动调用，默认 false              |
| `context`                  | 加载方式：`inline`（默认）或 `fork`（实验性） |

### VS Code 中的技能加载方式

1. **发现**：读取 `name` 和 `description`
2. **指令加载**：加载 `SKILL.md` 正文
3. **资源访问**：按需访问技能目录中的附加文件（脚本、示例等）

这种三级加载系统确保可以安装许多技能而不会消耗上下文。