#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Checker - 技能更新检查模块
自动检查技能更新，通知用户更新
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict
import requests


class UpdateChecker:
    """技能更新检查器"""

    def __init__(self):
        # 当前版本
        self.current_version = "1.1.0"

        # 配置文件
        self.config_file = Path.home() / '.claude' / 'skills' / 'skill-manager' / 'config.json'
        self.update_info_file = Path.home() / '.claude' / 'skills' / 'skill-manager' / 'docs' / 'update_info.json'

        # 加载配置
        self.config = self.load_config()

        # GitHub API URL（用于检查更新）
        self.github_repo = "songhaolin/skill-manager"
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"

    def load_config(self) -> Dict:
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        # 默认配置
        return {
            "last_check": None,
            "last_version": self.current_version,
            "update_notification": True,
            "auto_check_interval": 7  # 天数
        }

    def save_config(self):
        """保存配置"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def check_for_updates(self, force: bool = False) -> Optional[Dict]:
        """检查更新"""
        # 检查是否需要检查（避免频繁请求）
        if not force and not self.should_check():
            return None

        try:
            # 使用 GitHub API 获取最新版本
            response = requests.get(self.github_api_url, timeout=5)
            response.raise_for_status()

            release_info = response.json()
            latest_version = release_info['tag_name'].lstrip('v')

            # 更新检查时间
            self.config['last_check'] = self.get_current_date()
            self.save_config()

            # 比较版本
            if self.is_newer_version(latest_version, self.current_version):
                # 保存更新信息
                self.save_update_info(release_info)

                return {
                    "has_update": True,
                    "current_version": self.current_version,
                    "latest_version": latest_version,
                    "release_url": release_info['html_url'],
                    "release_notes": release_info['body']
                }

            return {"has_update": False}

        except Exception as e:
            print(f"[警告] 检查更新失败：{e}")
            return None

    def should_check(self) -> bool:
        """判断是否应该检查"""
        if not self.config.get('update_notification', True):
            return False

        last_check = self.config.get('last_check')
        if not last_check:
            return True

        interval = self.config.get('auto_check_interval', 7)
        days_since_check = self.days_between(last_check, self.get_current_date())

        return days_since_check >= interval

    def is_newer_version(self, latest: str, current: str) -> bool:
        """比较版本号"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]

            for i in range(max(len(latest_parts), len(current_parts))):
                l = latest_parts[i] if i < len(latest_parts) else 0
                c = current_parts[i] if i < len(current_parts) else 0

                if l > c:
                    return True
                elif l < c:
                    return False

            return False
        except:
            return False

    def save_update_info(self, release_info: Dict):
        """保存更新信息"""
        self.update_info_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.update_info_file, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)

    def get_update_notification(self) -> str:
        """获取更新通知"""
        update_info = self.check_for_updates()

        if not update_info:
            return ""

        if not update_info.get('has_update'):
            return "[成功] skill-manager 已是最新版本"

        # 生成更新通知
        notification = f"""
[新版本发现]

当前版本：v{update_info['current_version']}
最新版本：v{update_info['latest_version']}

更新内容：
{update_info['release_notes'][:500]}...

更新方法：
```bash
cd ~/.claude/skills/skill-manager
git pull origin main
```

或者访问：
{update_info['release_url']}

---
[更新后请重启 Claude Code 以使用新功能！]
"""
        return notification

    def days_between(self, date1: str, date2: str) -> int:
        """计算两个日期之间的天数"""
        try:
            from datetime import datetime
            d1 = datetime.strptime(date1, '%Y-%m-%d')
            d2 = datetime.strptime(date2, '%Y-%m-%d')
            return abs((d2 - d1).days)
        except:
            return 0

    def get_current_date(self) -> str:
        """获取当前日期"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')

    def update_skill_manager(self) -> bool:
        """更新 skill-manager"""
        try:
            # 获取安装目录
            install_dir = Path.home() / '.claude' / 'skills' / 'skill-manager'

            if not install_dir.exists():
                print("[错误] skill-manager 未安装")
                return False

            # 拉取最新代码
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=install_dir,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("[成功] skill-manager 更新成功！")
                print("[注意] 请重启 Claude Code 以使用新功能")

                # 更新配置
                update_info = self.check_for_updates(force=True)
                if update_info:
                    self.config['last_version'] = update_info['latest_version']
                    self.save_config()

                return True
            else:
                print(f"[错误] 更新失败：{result.stderr}")
                return False

        except Exception as e:
            print(f"[错误] 更新失败：{e}")
            return False


def show_update_on_startup():
    """启动时显示更新通知"""
    checker = UpdateChecker()

    # 显示更新通知
    notification = checker.get_update_notification()
    if notification:
        print(notification)
        print("\n如需稍后更新，可以使用：/skill skill-manager update")
        print("或者：/skill skill-manager check-update")


if __name__ == "__main__":
    import sys

    # 命令行使用
    if len(sys.argv) > 1:
        if sys.argv[1] == 'check':
            checker = UpdateChecker()
            print(checker.get_update_notification())
        elif sys.argv[1] == 'update':
            checker = UpdateChecker()
            checker.update_skill_manager()
        elif sys.argv[1] == 'startup':
            show_update_on_startup()
        else:
            print("用法: python update_checker.py [check|update|startup]")
    else:
        # 默认检查更新
        checker = UpdateChecker()
        print(checker.get_update_notification())