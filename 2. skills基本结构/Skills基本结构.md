# Skills 基本结构

## 一、Skills 的核心本质与特性

### 1.1 核心本质

Skills 的核心本质是为 AI 提供标准化执行流程的操作指引。一旦编写完成规则，这些规则就能像程序中的函数一样，被反复调用并直接复用。

### 1.2 存储与执行特性

Skills 以 Markdown 文本格式作为存储载体，其本身并不直接执行任何功能。Skills 具备按需加载和渐进式调用的特性，能够高效沉淀工作经验，实现能力的快速复用与精准传递。

## 二、Skill 的核心文件结构

### 2.1 基本组成

Skill 的核心结构可以概括为：一个文件夹加上一个 SKILL.md 文件。一个 Skill 本质上就是一个 Markdown 文件，且文件名必须固定为 SKILL.md。

目录结构示例：
```
my-skill/
└── SKILL.md   （唯一必需的文件）
```

### 2.2 SKILL.md 包含的内容

SKILL.md 文件需要包含两大部分：
- 元数据（至少包含名称和描述字段）
- 告诉 AI 如何完成某一特定任务的执行指令

## 三、SKILL.md 的基本模板与结构

### 3.1 基本模板格式

```markdown
---
name: your-skill-name
description: 一句话描述该 Skill 的功能和使用场景
---

# Skill 名称

## 使用指引
[给 AI 的分步骤行为指引]

## 示例
[该 Skill 的具体使用示例]
```

### 3.2 整体结构划分

整个 SKILL.md 文件分为上下两个部分：
- 上半部分：用 `---` 包裹的 YAML frontmatter（头部配置区域）
- 下半部分：Markdown 格式的正文（执行说明区域）

## 四、Frontmatter 元数据配置

### 4.1 必填字段概览

| 字段        | 必填 | 说明                                                         | 示例                              |
| ----------- | ---- | ------------------------------------------------------------ | --------------------------------- |
| name        | 是   | Skill 的唯一标识符，使用 kebab-case 命名格式，会被 `/` 命令引用，是系统识别 Skill 的关键字段 | web-design-guidelines             |
| description | 是   | 一句话描述功能与触发场景，内容越具体，触发越准确             | UI/UX design review for web pages |

### 4.2 name 字段的命名规范

name 字段最多支持 64 个字符，且只能包含小写字母、数字和连字符（-）。

正确示例：
```yaml
name: processing-pdfs        # 好：动名词形式，清晰描述功能
name: analyzing-spreadsheets # 好：一眼知道用途
name: my-brand-guidelines    # 好：组织专属知识
```

错误示例：
```yaml
name: helper      # 差：太模糊
name: MySkill     # 差：包含大写字母（不合规）
name: data files  # 差：包含空格（不合规）
```

命名建议：推荐使用动名词形式（动词 + -ing）来命名，如 `processing-pdfs`、`analyzing-spreadsheets`，这种方式能清晰描述 Skill 所提供的活动或能力。

命名对比参考：

| 推荐          | 不推荐               | 原因                                          |
| ------------- | -------------------- | --------------------------------------------- |
| code-reviewer | CodeReviewer         | 统一使用小写和连字符，避免跨平台兼容问题      |
| sql-optimizer | sql_optimizer        | kebab-case 是约定俗成的格式，与目录名保持一致 |
| deploy-check  | deploy-check-tool-v2 | 名称应简短，版本信息放在文件内部说明          |

### 4.3 description 字段的重要性与写法

description 是最重要的字段。在系统启动时，只会将所有 Skills 的 name 和 description 预加载进系统提示词。只有当 description 被 AI 判断为与当前任务相关时，系统才会进一步读取完整的 SKILL.md 内容。

description 字段应该同时包含两个信息：这个 Skill 做什么，以及 AI 应该在什么时候使用它。

正确示例：
```yaml
description: |
  Use when the user needs to create, read, edit, or generate Word
  documents (.docx). Triggers include: 'Word doc', 'word document',
  '.docx', 'report', 'letter', 'memo', or any request to produce
  a formatted document for sharing or printing.
```

description 写法对比：

| 推荐                                                | 不推荐           | 原因                                   |
| --------------------------------------------------- | ---------------- | -------------------------------------- |
| 「扫描 Python 代码中的 SQL 注入风险并给出修复建议」 | 「一个安全工具」 | 描述过于笼统，无法准确触发             |
| 「将 Markdown 转换为符合品牌规范的 HTML 邮件」      | 「转换文件格式」 | 缺少具体场景，可能在其他任务中被误触发 |

## 五、Markdown 正文的结构

### 5.1 正文的基本要求

Frontmatter 之后的部分是 Markdown 格式的正文，用于告诉 AI 具体应该怎么做。正文内容至少需要包含两个区块：使用指引和示例。

### 5.2 完整实例

以下是一个 SKILL.md 的完整实例：

```markdown
---
name: pdf-processing
description: 从 PDF 中提取文本和表格，填写表单，并合并文档
---

# PDF 处理

## 使用场景
当需要对 PDF 文件进行操作时使用，例如：

- 提取 PDF 文本或表格数据
- 填写 PDF 表单
- 合并多个 PDF 文件

## 提取文本
- 使用 `pdfplumber` 提取文本型 PDF 内容  
- 扫描版 PDF 需配合 OCR 工具  

## 填写表单
- 读取 PDF 表单字段  
- 按输入数据填充并生成新文件
```

### 5.3 最小必填示例

```markdown
---
name: skill-name
description: 说明该 Skill 的功能以及适用场景
---
```

### 5.4 含可选字段的完整示例

```markdown
---
name: pdf-processing
description: 从 PDF 中提取文本和表格，填写表单，并合并文档
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

## 六、SKILL.md 的完整字段说明

| 字段          | 必需 | 说明                                                         |
| ------------- | ---- | ------------------------------------------------------------ |
| name          | 是   | Skill 名称，最长 64 字符，只能使用小写字母、数字和 -，且不能以 - 开头或结尾 |
| description   | 是   | 功能与使用场景说明，最长 1024 字符，不能为空                 |
| license       | 否   | 许可证名称或指向随 Skill 附带的许可证文件                    |
| compatibility | 否   | 环境与依赖说明（产品、系统包、网络权限等），最长 500 字符    |
| metadata      | 否   | 自定义键值对，用于扩展元数据（如作者、版本号）               |
| allowed-tools | 否   | 允许使用的工具列表（空格分隔，实验性功能）                   |

## 七、Skill 的完整文件目录结构

### 7.1 目录组织原则

一个技能就是一个文件夹，其中至少包含一个 SKILL.md 文件。根据需要，还可以包含其他目录和文件。

为避免上下文膨胀，应遵循以下原则：
- 核心规则 → 放在 SKILL.md 中
- 详细资料 → 放在单独的文件中
- 实用逻辑 → 通过脚本执行（不加载到上下文）

### 7.2 推荐的目录结构

```
my-skill/
├── SKILL.md          # 必需：元数据 + 指令
├── scripts/          # 可选：可执行代码
      └── helper.py
├── references/       # 可选：参考文档
├── assets/           # 可选：模板、资源
└── ...               # 其他文件或目录
```

### 7.3 各目录的作用说明

| 目录        | 作用                                   |
| ----------- | -------------------------------------- |
| SKILL.md    | 必需文件，包含技能的元数据和执行指令   |
| scripts/    | 可选目录，包含代理可以执行的可执行代码 |
| references/ | 可选目录，包含详细的参考资料           |
| assets/     | 可选目录，包含静态资源如模板、图片等   |