# Skill Manager - 智能技能助手

[![Stars](https://img.shields.io/github/stars/songhaolin/skill-manager?style=social)](https://github.com/songhaolin/skill-manager/stargazers)
[![Version](https://img.shields.io/github/v/release/songhaolin/skill-manager)](https://github.com/songhaolin/skill-manager/releases)
[![License](https://img.shields.io/github/license/songhaolin/skill-manager)](LICENSE)
[![Claude Skills](https://img.shields.io/badge/Claude-Skills-blue)](https://github.com/songhaolin/skill-manager)

**让技能管理变得简单：说出需求，其余的交给我** ⭐

---

## 🚀 快速开始

### 安装

```bash
# 使用 npx（推荐）
npx skills add songhaolin/skill-manager

# 或手动安装
git clone https://github.com/songhaolin/skill-manager.git ~/.claude/skills/skill-manager
```

### 使用

```bash
# 重启 Codex，然后：
/skill skill-manager
```

---

## ✨ 核心功能

- 🤖 **自然语言理解**
  - 说"我想写小说"即可，无需记住技能名
  - 智能识别中文需求描述

- 🔍 **智能搜索**
  - 自动调用 find-skills 搜索相关技能
  - 多关键词搜索，找到最合适的

- 💡 **智能推荐**
  - 单结果：强烈推荐，说明功能特色
  - 多结果：列表展示，让用户选择
  - 无结果：建议创建新技能

- 🚀 **一键安装**
  - 确认后自动调用 skill-installer
  - 安装成功后提供使用说明

---

## 💡 使用示例

### 示例1：描述需求（最简单）

```
你: "我想写小说"

我: 🔍 搜索中...
    ✅ 找到 literary-story（小说创作专用工具）

    literary-story ⭐⭐⭐⭐⭐
    基于目录的小说创作工作流
    • 智能意图路由
    • 自动进度管理
    • 防写错保护

    这正是小说创作的利器！要安装吗？(y/n)

你: y

我: 🚀 安装中...
    ✅ 安装成功！

    使用: /skill literary-story
    然后: 继续写《你的小说名》
```

### 示例2：直接安装

```
你: "install pdf"

我: 🚀 安装 pdf 技能...
    ✅ 安装成功！

    使用: /skill pdf
```

### 示例3：搜索技能

```
你: "有什么任务管理工具"

我: 🔍 搜索中...
    ✅ 找到 planning-with-files

    planning-with-files ⭐⭐⭐⭐⭐
    Manus风格的文件规划系统
    • Meta 20亿美元收购的技术
    • 50+工具调用不迷失目标
    • 会话恢复支持

    要安装吗？(y/n)
```

---

## 🎯 支持的需求类型

| 你说 | 我理解 | 推荐技能 |
|------|--------|----------|
| "我想写小说" | 小说创作 | literary-story |
| "需要处理PDF" | PDF处理 | pdf |
| "有任务管理工具吗" | 任务管理 | planning-with-files |
| "小红书内容生成" | 社交媒体 | xiaohongshu-generator |
| "自动化测试" | 测试工具 | playwright |
| "一键部署" | 部署工具 | vercel-deploy |

---

## 🛠️ 技术实现

### 意图分析
- 识别：install/create/search 意图
- 提取：技能名称、关键词
- 映射：中文需求 → 英文搜索词

### 智能搜索
- 调用：`npx skills find`
- 解析：搜索结果
- 去重：多个结果

### 智能推荐
- 单结果：显示详细信息和功能
- 多结果：列表展示供选择
- 无结果：建议创建新技能

### 一键安装
- 调用：skill-installer
- 备用：`npx skills add`
- 验证：安装成功

---

## 📊 项目结构

```
skill-manager/
├── SKILL.md                    # 技能定义
├── agents/
│   └── openai.yaml            # UI元数据
├── scripts/
│   ├── intent_analyzer.py     # 意图分析器
│   ├── skill_searcher.py      # 技能搜索器
│   └── skill_installer.py     # 技能安装器
├── README.md                  # 本文件
├── publish.sh                 # Linux发布脚本
├── publish.bat                # Windows发布脚本
├── RELEASE_NOTES.md           # Release说明
└── PUBLISH_GUIDE.md           # 发布指南
```

---

## 🚀 发布计划

- [x] v1.0.0 - 核心功能
  - 意图识别
  - 智能搜索
  - 智能推荐
  - 一键安装

- [ ] v1.1.0 - 增强功能
  - 技能评分系统
  - 使用统计
  - 批量操作

- [ ] v2.0.0 - 高级功能
  - 个性化推荐
  - 可视化界面
  - Web Dashboard

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发

```bash
# 1. Fork 仓库
git clone https://github.com/YOUR_USERNAME/skill-manager.git

# 2. 创建分支
git checkout -b feature/your-feature

# 3. 提交更改
git commit -m "Add your feature"

# 4. 推送分支
git push origin feature/your-feature

# 5. 创建 Pull Request
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## ⭐ 如果这个工具有用

请给个 Star 支持一下！
[Star History](https://star-history.com/#YOUR_USERNAME/skill-manager&Date)

---

## 🔗 链接

- **GitHub**: https://github.com/songhaolin/skill-manager
- **Issues**: https://github.com/songhaolin/skill-manager/issues
- **发布**: https://github.com/songhaolin/skill-manager/releases

---

**让技能管理变得简单！** 🚀

*Made with ❤️ by Claude Code*
