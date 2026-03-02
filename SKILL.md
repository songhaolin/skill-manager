---
name: skill-manager
description: 智能技能助手。理解自然语言需求，自动搜索、推荐、安装技能。支持中文需求描述，如"我想写小说"、"需要处理PDF"、"有任务管理工具吗"等。会优先调用find-skills搜索现有技能，智能推荐最佳选择，一键安装。无需记住技能名称，说出需求即可。新增技能文档管理功能和自动更新通知。
user-invocable: true
version: "1.1.0"
---

# Skill Manager - 智能技能助手

## 🎯 核心理念

**不要让用户记住技能名称，让AI理解用户需求！**

## 使用方式

### 方式1：描述需求（推荐）

```
你想做什么，直接说：

用户: "我想写小说"
→ 搜索 literary-story，推荐安装

用户: "需要处理PDF"
→ 搜索 pdf，推荐安装

用户: "有任务管理工具吗"
→ 搜索 planning-with-files，推荐安装
```

### 方式2：直接安装

```
用户: "install literary-story"
→ 直接安装
```

## 核心功能

- 🤖 自然语言理解
- 🔍 智能搜索（调用find-skills）
- 💡 智能推荐
- 🚀 一键安装（调用skill-installer）
- 📖 技能文档管理（自动生成、智能切换）
- 🔄 自动更新通知

## 实现步骤

当用户说"我想写小说"时：

### 1. 分析意图

```
输入: "我想写小说"
意图: search
关键词: ["小说", "写作"]
搜索词: ["novel", "writing", "story"]
```

### 2. 搜索技能

```bash
# 调用 find-skills
npx skills find novel
npx skills find writing

# 解析结果
找到: literary-story
```

### 3. 智能推荐

```
✅ 找到完美匹配！

literary-story ⭐⭐⭐⭐⭐
基于目录的小说创作工作流

功能：
• 智能意图路由
• 自动进度管理
• 防写错保护

要安装吗？(y/n)
```

### 4. 执行安装

```python
# 用户确认后，调用 skill-installer
python install-skill-from-github.py \
  --repo openai/skills \
  --path skills/.curated/literary-story
```

## 关键词映射

| 用户需求 | 搜索词 |
|---------|--------|
| 写小说 | novel, story, writing |
| 小红书 | xiaohongshu, content |
| 任务管理 | task, plan, planning |
| PDF | pdf, document |
| 测试 | test, testing |

## 📖 文档管理功能

### 查看技能文档

```
👤 "我想了解 brainstorming"

🤖 📋 请选择要查看的内容：

1. 📖 通用管理文档 - 我维护的标准化文档（包含准确安装方式）
2. 🔧 源码 README - 技能自带的原始文档
3. 🔍 对比查看 - 同时查看两种文档
4. 📝 基本信息 - 快速概览

👤 "1"

🤖 [展示标准化管理文档]
```

### 自动生成文档

安装技能后，skill-manager 会自动：

1. 读取技能的 SKILL.md 和 README.md
2. 分析技能功能和使用方法
3. 生成标准化管理文档
4. 保存在 `~/.claude/skills/skill-manager/docs/skill_docs/`

### 首次运行自动扫描

当你升级到 v1.1.0 后，首次运行时会：
1. 自动扫描 ~/.claude/skills/ 目录
2. 为所有已安装的技能生成管理文档
3. 无需手动操作

### 手动生成所有文档

如果需要重新生成所有文档：
```
/skill skill-manager generate-all-docs
```

### 文档验证机制

所有安装命令都经过验证，确保准确性：

- ✅ 从 GitHub 获取最新信息
- ✅ 测试安装命令
- ✅ 标记验证状态
- ✅ 记录验证时间

## 🔄 更新检查功能

### 启动时自动检查

每次使用 skill-manager 时，会自动检查是否有新版本（每7天检查一次）。

### 手动检查更新

```
👤 "/skill skill-manager check-update"

🤖 [检查中...]
    ✅ 已是最新版本
    或
    🎉 发现新版本！
    当前版本：v1.1.0
    最新版本：v1.2.0

    更新方法：
    cd ~/.claude/skills/skill-manager
    git pull origin main
```

### 一键更新

```
👤 "/skill skill-manager update"

🤖 🚀 更新中...
    ✅ 更新成功！
    ⚠️ 请重启 Claude Code 以使用新功能
```

### 配置更新通知

```python
# 在 ~/.claude/skills/skill-manager/config.json 中
{
  "update_notification": true,     # 是否显示更新通知
  "auto_check_interval": 7         # 自动检查间隔（天）
}
```

## 错误处理

- 未找到技能 → 建议创建新技能
- 安装失败 → 提供手动安装指引
- 网络问题 → 建议检查连接

## 使用示例

### 示例1：需求描述

```
👤 "我想写小说"

🤖 🔍 搜索中...
   ✅ 找到 literary-story
   这是小说创作专用工具！要安装吗？(y/n)

👤 "y"

🤖 🚀 安装中...
   ✅ 安装成功！
   使用: /skill literary-story
```

### 示例2：直接安装

```
👤 "install pdf"

🤖 🚀 安装 pdf 技能...
   ✅ 安装成功！
   使用: /skill pdf
```

### 示例3：未找到

```
👤 "我需要股票查询技能"

🤖 🔍 搜索中...
   ❌ 未找到相关技能

💡 我可以帮你创建一个新技能！
   功能建议：
   • 股票价格查询
   • K线图生成

要创建吗？(y/n)
```

### 示例4：查看技能文档

```
👤 "说明 brainstorming"

🤖 📋 请选择要查看的内容：

1. 📖 通用管理文档 - 我维护的标准化文档（包含准确安装方式）
2. 🔧 源码 README - 技能自带的原始文档
3. 🔍 对比查看 - 同时查看两种文档
4. 📝 基本信息 - 快速概览（默认）

👤 "1"

🤖 [展示标准化管理文档，包含：
    - 仓库地址
    - 实际功能
    - 使用方法
    - ✅ 已验证的安装方式
    - 使用示例
]
```

### 示例5：检查更新

```
👤 "/skill skill-manager check-update"

🤖 📡 检查中...
   ✅ 已是最新版本
   或
   🎉 发现新版本！

   当前版本：v1.1.0
   最新版本：v1.2.0

   更新内容：
   - 新增技能分类浏览
   - 优化搜索算法
   - 修复已知问题

   更新方法：
   cd ~/.claude/skills/skill-manager
   git pull origin main

   或使用：/skill skill-manager update
```

## 技术实现

### 意图分析器

- 识别意图类型：install/create/search/info
- 提取技能名称
- 提取关键词
- 生成搜索词

### 技能搜索器

- 调用 npx skills find
- 解析搜索结果
- 去重

### 技能安装器

- 调用 skill-installer
- 或使用 npx skills add
- 验证安装

### 文档管理器

- 自动生成标准化文档
- 智能文档切换（管理文档 vs 源码文档）
- 文档验证机制
- 文档索引维护

### 更新检查器

- 自动检查 GitHub 最新版本
- 版本号比较
- 更新通知生成
- 一键更新功能

## 版本

- v1.1.0 (2026-03-02) - 新增技能文档管理和自动更新通知功能
- v1.0.0 (2026-03-02) - 初始版本

---

**让技能管理变得简单！** 🚀
