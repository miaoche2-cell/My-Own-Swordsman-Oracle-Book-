# CLAUDE.md — 全局规则

## 核心规则

### 磁盘清理规则

1. **清理前必须解释**：每个文件/目录在操作前，必须告诉用户这是什么文件/数据、删除后有什么影响、是否可以安全删除。
2. **不自行编写清理代码**：优先使用 Windows 内置工具（`cleanmgr`、`DISM`、`powercfg`、`mklink`）和 GitHub 上已有的开源工程（BleachBit、Sifty 等），不自己写脚本/程序。
3. **游戏数据优先迁移而非删除**：大体积游戏存档/Mod 优先用 `mklink /J` 迁移到其他盘。
4. **不碰系统核心文件**：`C:\Windows\System32` 绝对不碰，`WinSxS` 只用 DISM 命令。
5. **管理员权限操作前告知用户**：`mklink /J`、`DISM`、`powercfg` 等需管理员权限的命令，执行前告知用户。

### C 盘清理工具链

| 工具 | 用途 | 来源 |
|------|------|------|
| `cleanmgr` | Windows 磁盘清理 | 系统内置 |
| `DISM` | WinSxS 组件存储清理 | 系统内置 |
| `mklink /J` | 目录联结，迁移大文件 | 系统内置 |
| BleachBit | CLI 自动化系统清理 | GitHub (GPLv3) |
| Sifty | 安全优先清理（试运行+回收站） | GitHub (MIT) |

### 通用规则

- 操作前告诉用户你在做什么，不要自作主张
- 优先复用已有代码/工具，不重新造轮子
- 需要用户确认的操作，明确列出选项和后果

### 视觉识别规则 👁️

本模型（DeepSeek）不具备原生识图能力。当用户发送图片时，自动调用 vision skill：

- **触发条件**：用户消息中出现图片附件、图片路径（本地/URL）、"Saved attachments:" 等
- **执行方式**：
  ```bash
  node C:\Users\1\.claude\skills\vision\vision.js "图片路径" "用中文描述这张图片"
  ```
- **注意**：不要对图片使用 Read 工具，始终用 vision.js 处理
- 识图模型：`qwen3-vl-flash`（阿里云百炼，OpenAI 兼容格式）
- API 配置：`C:\Users\1\.claude\skills\vision\.env`
- 获取 Key：https://bailian.console.aliyun.com/

---

## Skills & 插件完整清单

> **所有 Skills 统一存放于 `C:\Users\1\.claude\skills\`（33 个），启动时自动发现，随时可调用。**
> **插件由 `C:\Users\1\.claude\plugins\` 管理，自动更新。**

### 🏠 本地 Skills（C:\Users\1\.claude\skills\，33 个）

#### 开发工具类
| Skill | 用途 |
|-------|------|
| caveman | 超压缩模式，省 ~75% token |
| code-review | 代码审查 |
| code-simplifier | 代码简化重构 |
| diagnose | 纪律化 Bug 诊断 loop |
| git-guardrails-claude-code | Git 危险操作护栏 |
| improve-codebase-architecture | 改进代码架构 |
| migrate-to-shoehorn | 迁移到 shoohorn 类型断言 |
| prototype | 快速原型（TUI 或 UI 变体） |
| qa | 交互式 QA → GitHub Issues |
| request-refactor-plan | 重构计划 + tiny commits |
| review | 代码审查 |
| scaffold-exercises | 搭建练习框架 |
| setup-pre-commit | 设置 Husky pre-commit |
| tdd | 测试驱动开发（red-green-refactor） |
| triage | Issue 分诊状态机 |

#### 设计与架构
| Skill | 用途 |
|-------|------|
| design-an-interface | 并行生成多个 API 设计方案 |
| ui-ux-pro-max | UI/UX 设计增强 |
| frontend-design | 前端设计 |

#### 文档与写作
| Skill | 用途 |
|-------|------|
| edit-article | 编辑改进文章 |
| documentation-generator | 文档生成 |
| document-skills | 文档处理 |
| to-issues | 计划 → Issues 拆分 |
| to-prd | 对话 → PRD |
| write-a-skill | 创建新 Skill |
| writing-beats | 叙事节奏写作 |
| writing-fragments | 写作素材挖掘 |
| writing-shape | 草稿塑形为文章 |

#### 思考与审查
| Skill | 用途 |
|-------|------|
| superpowers 🛡️ | 反谄媚、批判性思维 |
| grill-me | 持续追问直到理解一致 |
| grill-with-docs | 对照文档审查方案 |
| handoff | 对话压缩交接 |
| teach | 教学解释 |
| zoom-out | 视角放大/总结 |
| ubiquitous-language | DDD 统一语言 |

#### 平台与工具
| Skill | 用途 |
|-------|------|
| agent-reach | 13 平台互联网调研 |
| anysearch | 统一实时搜索 |
| hookify | Hooks 管理 |
| obsidian-vault | Obsidian 笔记操作 |
| setup-matt-pocock-skills | Matt Pocock TS 技能 |
| example-skills | 示例技能集 |

---

## 历史记录

### C 盘清理 (2026-07-03)

从 142G/3.5G (98%) → 98G/49G (67%)，释放 44 GB。

详见：`D:\桌面\光栅\C盘清理记录.md`

主要操作：
- NVIDIA 缓存 / pip / npm / Temp 等安全缓存 → 5.2 GB
- WPS 数据 / NVIDIA 安装包 / Razer 日志 → 15.1 GB
- BG3 存档 + Mods 迁移到 D 盘 → 26.6 GB
