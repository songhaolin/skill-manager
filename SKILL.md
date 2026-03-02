---
name: skill-manager
description: 智能技能助手。理解自然语言需求，自动搜索、推荐、安装技能。支持中文需求描述，如"我想写小说"、"需要处理PDF"、"有任务管理工具吗"等。会优先调用find-skills搜索现有技能，智能推荐最佳选择，一键安装。无需记住技能名称，说出需求即可。
user-invocable: true
version: "1.0.0"
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

## 技术实现

### 意图分析器

- 识别意图类型：install/create/search
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

## 版本

- v1.0.0 (2026-03-02) - 初始版本

---

**让技能管理变得简单！** 🚀
