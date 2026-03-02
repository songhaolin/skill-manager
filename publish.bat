@echo off
REM Skill Manager GitHub 发布脚本 (Windows版本)
REM 用于自动化创建GitHub仓库、打标签、创建Release

setlocal enabledelayedexpansion

echo ========================================
echo Skill Manager GitHub 发布脚本
echo ========================================
echo.

REM 配置
set SKILL_NAME=skill-manager
set REPO_NAME=skill-manager
if "%GITHUB_USERNAME%"=="" (
    set USERNAME=songhaolin
) else (
    set USERNAME=%GITHUB_USERNAME%
)

echo [步骤 1/6] 检查Git...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Git 未安装
    echo 请先安装Git: https://git-scm.com/
    pause
    exit /b 1
)
echo [成功] Git 已安装
echo.

echo [步骤 2/6] 检查目录...
if not exist "SKILL.md" (
    echo [错误] 请在 skill-manager 目录中运行此脚本
    pause
    exit /b 1
)
echo [成功] 找到 skill-manager
echo.

echo [步骤 3/6] 初始化Git仓库...
if exist ".git" (
    echo [警告] Git仓库已存在
) else (
    git init
    echo [成功] Git仓库初始化成功
)
echo.

echo [步骤 4/6] 添加文件...
git add .
echo [成功] 文件已添加
echo.

echo [步骤 5/6] 创建提交...
git rev-parse HEAD >nul 2>&1
if %errorlevel% equ 0 (
    echo [警告] 已存在提交，跳过
) else (
    git commit -m "Initial commit: skill-manager v1.0.0"
    echo [成功] 提交创建成功
)
echo.

echo [步骤 6/6] 准备推送到GitHub...
echo.
echo 请先在GitHub上创建仓库:
echo 1. 访问: https://github.com/new
echo 2. 仓库名: %REPO_NAME%
echo 3. 描述: 智能技能助手 - 说出需求，自动推荐安装技能
echo 4. 选择: Public
echo 5. 不要初始化 README
echo.
set /p CONTINUE=创建完成后按回车继续...

echo.
echo 关联远程仓库...
set REMOTE_URL=https://github.com/%USERNAME%/%REPO_NAME%.git

git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo [警告] 远程仓库已存在
    git remote set-url origin %REMOTE_URL%
) else (
    git remote add origin %REMOTE_URL%
    echo [成功] 远程仓库已关联
)
echo.

echo 推送到GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 发布成功！
    echo ========================================
    echo.
    echo 仓库地址: https://github.com/%USERNAME%/%REPO_NAME%
    echo.
    echo 下一步:
    echo 1. 访问仓库并设置描述
    echo 2. 添加Topics
    echo 3. 创建第一个Release
    echo.
) else (
    echo.
    echo [错误] 推送失败
    echo.
    echo 可能的原因:
    echo 1. GitHub仓库未创建
    echo 2. 用户名或仓库名错误
    echo 3. 认证问题
    echo.
    echo 请检查后重试
    echo.
)

pause
