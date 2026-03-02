# 🎉 skill-manager v1.0.0

## 🚀 智能技能助手

让技能管理变得简单：**说出需求，其余的交给我**

## ✨ 核心功能

- 🤖 **自然语言理解**
  - 说"我想写小说"即可，无需记住技能名
  - 智能识别中文需求

- 🔍 **智能搜索**
  - 自动调用 find-skills 搜索相关技能
  - 多关键词搜索，找到最合适的

- 💡 **智能推荐**
  - 单结果：强烈推荐，说明功能
  - 多结果：列表展示，让用户选择
  - 无结果：建议创建新技能

- 🚀 **一键安装**
  - 确认后自动调用 skill-installer
  - 安装成功后提供使用说明

## 📦 安装

### 方法1：使用 npx（推荐）

```bash
npx skills add songhaolin/skill-manager
```

### 方法2：手动安装

```bash
git clone https://github.com/songhaolin/skill-manager.git ~/.claude/skills/skill-manager
```

## 📖 使用示例

### 示例1：描述需求

```
/skill skill-manager
我想写小说

→ 🔍 搜索中...
→ ✅ 找到 literary-story
→ 💡 这是小说创作专用工具！
→ 🚀 一键安装
```

### 示例2：直接安装

```
/skill skill-manager
install pdf

→ 🚀 直接安装，无需搜索
```

### 示例3：搜索

```
/skill skill-manager
有任务管理工具吗

→ 🔍 搜索中...
→ ✅ 找到 planning-with-files
→ 💡 Meta 20亿美元收购的技术
```

## 🎯 支持的需求类型

| 需求 | 推荐技能 |
|------|----------|
| "我想写小说" | literary-story |
| "需要处理PDF" | pdf |
| "有任务管理工具吗" | planning-with-files |
| "小红书内容生成" | xiaohongshu-generator |
| "自动化测试" | playwright |

## 🛠️ 技术实现

- **意图分析**: 正则表达式 + 关键词映射
- **技能搜索**: 调用 npx skills find
- **智能推荐**: 内置技能知识库
- **一键安装**: 调用 skill-installer

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
└── README.md                  # 项目说明
```

## 🔗 链接

- **GitHub**: https://github.com/songhaolin/skill-manager
- **Issues**: https://github.com/songhaolin/skill-manager/issues
- **文档**: README.md

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## ⭐ 如果这个工具有用

请给个 Star 支持一下！

---

**让技能管理变得简单！** 🚀
