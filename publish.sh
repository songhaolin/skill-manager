#!/bin/bash
# Skill Manager GitHub 发布脚本
# 用于自动化创建GitHub仓库、打标签、创建Release

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SKILL_NAME="skill-manager"
REPO_NAME="skill-manager"
USERNAME="${GITHUB_USERNAME:-songhaolin}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Skill Manager GitHub 发布脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git 未安装${NC}"
    echo "请先安装Git: https://git-scm.com/"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "SKILL.md" ]; then
    echo -e "${RED}❌ 请在 skill-manager 目录中运行此脚本${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 找到 skill-manager${NC}"

# 步骤1：初始化Git仓库
echo ""
echo -e "${BLUE}[步骤 1/6] 初始化Git仓库${NC}"
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git仓库已存在${NC}"
else
    git init
    echo -e "${GREEN}✓ Git仓库初始化成功${NC}"
fi

# 步骤2：添加所有文件
echo ""
echo -e "${BLUE}[步骤 2/6] 添加文件到Git${NC}"
git add .
echo -e "${GREEN}✓ 文件已添加${NC}"

# 步骤3：创建初始提交
echo ""
echo -e "${BLUE}[步骤 3/6] 创建初始提交${NC}"
if git rev-parse HEAD > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  已存在提交，跳过${NC}"
else
    git commit -m "Initial commit: skill-manager v1.0.0

智能技能助手 - 说出需求，自动推荐安装技能

功能：
- 自然语言理解
- 智能搜索
- 智能推荐
- 一键安装

安装: npx skills add $USERNAME/$REPO_NAME"
    echo -e "${GREEN}✓ 提交创建成功${NC}"
fi

# 步骤4：创建GitHub仓库提示
echo ""
echo -e "${BLUE}[步骤 4/6] 创建GitHub仓库${NC}"
echo ""
echo -e "${YELLOW}请在GitHub上创建新仓库：${NC}"
echo "1. 访问: https://github.com/new"
echo "2. 仓库名: $REPO_NAME"
echo "3. 描述: 智能技能助手 - 说出需求，自动推荐安装技能"
echo "4. 选择: Public（公开）"
echo "5. ⚠️  不要初始化 README"
echo ""
echo "创建后仓库地址: https://github.com/$USERNAME/$REPO_NAME"

# 步骤5：关联远程仓库
echo ""
echo -e "${BLUE}[步骤 5/6] 关联远程仓库${NC}"
REMOTE_URL="https://github.com/$USERNAME/$REPO_NAME.git"

if git remote get-url origin &> /dev/null; then
    echo -e "${YELLOW}⚠️  远程仓库已存在${NC}"
    git remote set-url origin "$REMOTE_URL"
else
    git remote add origin "$REMOTE_URL"
    echo -e "${GREEN}✓ 远程仓库已关联${NC}"
fi

# 步骤6：推送到GitHub
echo ""
echo -e "${BLUE}[步骤 6/6] 推送到GitHub${NC}"
echo "推送代码到 main 分支..."

git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ 发布成功！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "🎉 恭喜！skill-manager 已成功发布到GitHub！"
    echo ""
    echo "📦 仓库地址: https://github.com/$USERNAME/$REPO_NAME"
    echo ""
    echo "下一步："
    echo "1. 访问仓库并设置描述"
    echo "2. 添加Topics: claude-skills, ai-assistant, skill-management"
    echo "3. 创建第一个Release"
    echo ""
    echo "📢 推广建议："
    echo "- 分享到 Reddit r/Claude"
    echo "- 发推文: @AnthropicAI"
    echo "- 发布到 Discord AI社区"
    echo ""
else
    echo ""
    echo -e "${RED}❌ 推送失败${NC}"
    echo ""
    echo "可能的原因："
    echo "1. GitHub仓库未创建"
    echo "2. 用户名或仓库名错误"
    echo "3. 认证问题"
    echo ""
    echo "请检查后重试："
    echo "git push -u origin main"
fi
