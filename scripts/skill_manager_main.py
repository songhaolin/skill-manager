#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Manager Main - 主程序入口
集成所有功能：意图分析、技能搜索、安装、文档管理、更新检查
"""

import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from intent_analyzer import IntentAnalyzer
from skill_searcher import SkillSearcher
from skill_installer import SkillInstaller
from document_manager import DocumentManager
from update_checker import UpdateChecker


class SkillManager:
    """技能管理器主类"""

    def __init__(self):
        self.intent_analyzer = IntentAnalyzer()
        self.skill_searcher = SkillSearcher()
        self.skill_installer = SkillInstaller()
        self.doc_manager = DocumentManager()
        self.update_checker = UpdateChecker()

    def handle_request(self, request: str) -> str:
        """处理用户请求"""
        print(f"🤖 处理请求: {request}")

        # 1. 检查更新
        if self.check_update_needed(request):
            return self.handle_update_request(request)

        # 2. 分析意图
        intent, skill_name = self.intent_analyzer.analyze(request)
        print(f"🎯 意图: {intent}, 技能: {skill_name}")

        # 3. 处理不同意图
        if intent == "info":
            return self.handle_info_request(skill_name, request)
        elif intent == "install":
            return self.handle_install_request(skill_name)
        elif intent == "search":
            return self.handle_search_request(skill_name)
        elif intent == "update":
            return self.handle_update_command(request)
        elif intent == "check":
            return self.handle_check_request(request)
        else:
            return "❓ 不太理解你的需求，试试说：\n- '我想写小说'\n- 'install pdf'\n- '说明 brainstorming'\n- 'check-update'"

    def handle_info_request(self, skill_name: str, request: str) -> str:
        """处理信息查看请求"""
        # 检查技能是否已安装
        if not self.doc_manager.find_skill_installation(skill_name):
            return f"❌ 技能 '{skill_name}' 尚未安装，请先安装"

        # 显示文档选择
        return self.doc_manager.show_skill_info(skill_name)

    def handle_install_request(self, skill_name: str) -> str:
        """处理安装请求"""
        # 检查是否已安装
        if self.doc_manager.find_skill_installation(skill_name):
            return f"✅ 技能 '{skill_name}' 已安装\n\n是否要查看文档？输入：说明 {skill_name}"

        # 搜索技能
        results = self.skill_searcher.search(skill_name)
        if not results:
            return f"❌ 未找到技能 '{skill_name}'\n\n我可以帮你创建这个技能，需要吗？"

        # 选择技能
        if len(results) == 1:
            # 单结果，直接安装
            return self.install_skill(results[0], skill_name)
        else:
            # 多结果，让用户选择
            response = "🔍 找到多个相关技能，请选择：\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. {result}\n"
            response += f"\n请输入数字（1-{len(results)}）或输入 'cancel' 取消"
            return response

    def install_skill(self, skill_name: str, user_query: str = "") -> str:
        """安装指定技能"""
        try:
            # 调用安装器
            result = self.skill_installer.install(skill_name)

            if "成功" in result:
                # 安装成功，生成文档
                self.doc_manager.check_and_install_skill(skill_name)

                # 添加到技能索引
                if skill_name not in self.doc_manager.skills_info:
                    self.doc_manager.skills_info[skill_name] = {
                        "repo": "待补充",
                        "verified": True,
                        "last_updated": self.doc_manager.get_current_time()
                    }
                    self.doc_manager.save_skills_index()

                response = f"🎉 {skill_name} 安装成功！\n\n"
                response += f"💡 快速开始：\n"
                response += f"- /skill {skill_name}\n"
                response += f"- 说明 {skill_name}\n"

                if user_query:
                    response += f"\n📝 因为你说：'{user_query}'"

                return response
            else:
                return f"❌ 安装失败：{result}"

        except Exception as e:
            return f"❌ 安装过程中出错：{str(e)}"

    def handle_search_request(self, skill_name: str) -> str:
        """处理搜索请求"""
        results = self.skill_searcher.search(skill_name)

        if not results:
            return f"❌ 未找到技能 '{skill_name}'"

        response = f"🔍 找到 {len(results)} 个相关技能：\n\n"
        for i, result in enumerate(results, 1):
            response += f"{i}. {result}\n"

        response += f"\n输入数字查看详情（1-{len(results)}），或输入 'install' 全部安装"
        return response

    def handle_update_request(self, request: str) -> str:
        """处理更新请求"""
        if "update" in request.lower():
            return self.update_checker.update_skill_manager()
        elif "check" in request.lower() or "update" in request:
            return self.handle_check_request(request)
        else:
            return "请使用：\n- check-update\n- update"

    def handle_update_command(self, request: str) -> str:
        """处理更新命令"""
        if "update" in request.lower():
            return self.update_checker.update_skill_manager()
        return "请使用：/skill skill-manager update"

    def handle_check_request(self, request: str) -> str:
        """处理检查请求"""
        if "check" in request.lower() and "update" in request.lower():
            return self.update_checker.get_update_notification()
        return "请使用：/skill skill-manager check-update"

    def check_update_needed(self, request: str) -> bool:
        """检查是否需要更新"""
        if "update" in request.lower() or "check" in request.lower():
            return True
        return False


def main():
    """主函数"""
    # 初始化管理器
    manager = SkillManager()

    # 从命令行参数获取请求
    if len(sys.argv) > 1:
        request = ' '.join(sys.argv[1:])
    else:
        # 交互式输入
        print("🎯 Skill Manager v1.1.0")
        print("输入 'exit' 退出")
        print("-" * 40)

        while True:
            try:
                request = input("\n请输入你的需求：").strip()
                if request.lower() == 'exit':
                    break

                if request:
                    response = manager.handle_request(request)
                    print(f"\n{response}\n")
                    print("-" * 40)
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误：{str(e)}")


if __name__ == "__main__":
    # 启动时检查更新
    print_update = False
    if len(sys.argv) > 1 and sys.argv[1] != "check-update":
        update_checker = UpdateChecker()
        notification = update_checker.get_update_notification()
        if notification:
            print(notification)
            print("继续使用 skill-manager...\n")

    main()