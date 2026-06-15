#!/usr/bin/env python3
"""
经验萃取Skill自动更新系统
功能：自动联网检索最新行业动态，智能更新Skill内容，同步GitHub
"""

import os
import json
import datetime
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# 配置区 - 根据实际情况修改
# ============================================================

CONFIG = {
    "github_repo": "",  # GitHub仓库地址，如 "username/repo"
    "github_token": "",  # GitHub Personal Access Token
    "update_interval_days": 7,  # 更新检查间隔（天）
    "max_results_per_search": 5,  # 每次搜索返回的最大结果数
    "skills_dir": "/workspace/.minimax/skills",
    "backup_dir": "/workspace/.minimax/skills/_update_system/backups",
    "log_dir": "/workspace/.minimax/skills/_update_system/logs",
}

# 行业搜索关键词配置
INDUSTRY_KEYWORDS = {
    "tech-exp-distill": {
        "name": "信息技术行业",
        "search_queries": [
            "agile development best practices 2024",
            "DevOps trends 2024",
            "software architecture patterns",
            "site reliability engineering SRE",
            "continuous integration deployment tools",
        ],
        "sources": ["techcrunch", "infoworld", "martinfowler.com", "dev.to"],
    },
    "finance-exp-distill": {
        "name": "金融行业",
        "search_queries": [
            "digital transformation banking 2024",
            "fintech innovation trends",
            "risk management best practices",
            "financial technology regulation",
            "insurtech developments 2024",
        ],
        "sources": ["mckinsey.com", "bcg.com", "financialtimes.com", "bankingtech.com"],
    },
    "mfg-exp-distill": {
        "name": "制造业",
        "search_queries": [
            "smart manufacturing industry 4.0 2024",
            "lean production best practices",
            "supply chain management trends",
            "predictive maintenance manufacturing",
            "TPM total productive maintenance",
        ],
        "sources": ["mckinsey.com", "forbes.com/manufacturing", "industryweek.com"],
    },
    "industry-exp-distill": {
        "name": "行业经验元框架",
        "search_queries": [
            "knowledge management best practices 2024",
            "industry experience distillation",
            "cross-industry best practices",
            "ISIC industry classification updates",
            "professional knowledge management",
        ],
        "sources": ["hbr.org", "mckinsey.com", "forbes.com/business"],
    },
    "jing-yan-cui-qu": {
        "name": "个人经验萃取",
        "search_queries": [
            "personal knowledge management 2024",
            "experience distillation methods",
            "career growth learning strategies",
            "skill development methodologies",
            "reflection practices professional development",
        ],
        "sources": ["hbr.org", "fastcompany.com", "medium.com"],
    },
}

# ============================================================
# 版本控制类
# ============================================================

class VersionControl:
    """版本控制和变更追踪"""

    VERSION_PATTERN = re.compile(r'\*\*版本\*\*[:：]?\s*v?(\d+)\.(\d+)\.(\d+)')
    UPDATE_LOG_PATTERN = re.compile(r'\*\*更新日志\*\*.*?(?=\n##|\Z)', re.DOTALL | re.IGNORECASE)

    @staticmethod
    def parse_version(version_str: str) -> Tuple[int, int, int]:
        """解析版本号字符串"""
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', version_str)
        if match:
            return int(match.group(1)), int(match.group(2)), int(match.group(3))
        return 0, 0, 0

    @staticmethod
    def bump_version(current: str, level: str = "patch") -> str:
        """递增版本号"""
        major, minor, patch = VersionControl.parse_version(current)
        if level == "major":
            return f"{major + 1}.0.0"
        elif level == "minor":
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"

    @staticmethod
    def generate_changelog_entry(update_type: str, content_summary: str, date: str = None) -> str:
        """生成更新日志条目"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"- **{date}** [{update_type}]: {content_summary}"

    @staticmethod
    def update_version_in_file(file_path: str, new_version: str) -> bool:
        """更新文件中的版本号"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 更新版本号
            pattern = r'\*\*版本\*\*[:：]?\s*v?\d+\.\d+\.\d+'
            replacement = f"**版本**: v{new_version}"
            new_content = re.sub(pattern, replacement, content)

            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
            return False
        except Exception as e:
            print(f"更新版本号失败: {e}")
            return False

    @staticmethod
    def append_changelog(file_path: str, entry: str) -> bool:
        """追加更新日志"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 找到更新日志位置
            changelog_match = VersionControl.UPDATE_LOG_PATTERN.search(content)
            if changelog_match:
                old_log = changelog_match.group(0)
                # 在更新日志后追加新条目
                new_log = old_log.rstrip() + "\n" + entry + "\n"
                new_content = content.replace(old_log, new_log)
            else:
                # 如果没有更新日志，在版本信息后添加
                version_match = re.search(r'\*\*版本\*\*.*?(?=\n##|\n\n|\Z)', content, re.DOTALL)
                if version_match:
                    insert_pos = version_match.end()
                    new_content = content[:insert_pos] + "\n\n**更新日志**:\n" + entry + "\n" + content[insert_pos:]
                else:
                    new_content = content + "\n\n**更新日志**:\n" + entry + "\n"

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"追加更新日志失败: {e}")
            return False


# ============================================================
# 内容更新类
# ============================================================

class ContentUpdater:
    """智能内容更新"""

    @staticmethod
    def calculate_content_hash(file_path: str) -> str:
        """计算文件内容哈希"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    @staticmethod
    def find_insertion_point(content: str, section_name: str) -> int:
        """找到指定章节的插入位置"""
        pattern = rf'(##\s*{section_name}|###\s*{section_name})'
        match = re.search(pattern, content)
        if match:
            return match.end()
        return -1

    @staticmethod
    def generate_update_section(new_trends: List[Dict]) -> str:
        """生成更新内容章节"""
        if not new_trends:
            return ""

        section = "\n### 最新行业动态\n\n"

        for i, trend in enumerate(new_trends, 1):
            section += f"**{i}. {trend.get('title', '未命名趋势')[:60]}**\n"
            section += f"- 来源: {trend.get('source', '未知来源')}\n"
            section += f"- 摘要: {trend.get('snippet', '')[:150]}...\n"
            if trend.get('link'):
                section += f"- 链接: {trend.get('link')}\n"
            section += "\n"

        section += "---\n"
        return section

    @staticmethod
    def update_skill_file(file_path: str, new_trends: List[Dict], update_type: str) -> bool:
        """更新Skill文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 生成更新内容
            update_content = ContentUpdater.generate_update_section(new_trends)

            if not update_content.strip() or "最新行业动态" in content:
                # 已存在或无内容，跳过
                return False

            # 找到合适位置插入（通常在方法论或最佳实践章节后）
            insert_point = content.find("## 资源与学习路径")
            if insert_point == -1:
                insert_point = content.find("## 版本与更新")

            if insert_point == -1:
                insert_point = len(content)

            # 插入新内容
            new_content = content[:insert_point] + update_content + content[insert_point:]

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return True
        except Exception as e:
            print(f"更新Skill文件失败: {e}")
            return False


# ============================================================
# GitHub同步类
# ============================================================

class GitHubSync:
    """GitHub仓库同步"""

    def __init__(self, repo: str, token: str):
        self.repo = repo
        self.token = token
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def check_connection(self) -> bool:
        """检查GitHub连接"""
        import urllib.request
        try:
            req = urllib.request.Request(
                f"{self.api_base}/repos/{self.repo}",
                headers=self.headers
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200
        except Exception as e:
            print(f"GitHub连接检查失败: {e}")
            return False

    def commit_changes(self, file_path: str, message: str, content: str = None) -> bool:
        """提交文件变更"""
        import base64
        import urllib.request
        import json

        try:
            # 获取当前文件SHA
            repo_path = file_path.replace("/workspace/", "")
            url = f"{self.api_base}/repos/{self.repo}/contents/{repo_path}"

            req = urllib.request.Request(url, headers=self.headers)
            try:
                with urllib.request.urlopen(req) as response:
                    current = json.loads(response.read())
                    sha = current.get('sha')
            except Exception:
                sha = None

            # 准备提交数据
            if content:
                encoded_content = base64.b64encode(content.encode()).decode()
            else:
                with open(file_path, 'rb') as f:
                    encoded_content = base64.b64encode(f.read()).decode()

            data = {
                "message": message,
                "content": encoded_content,
            }
            if sha:
                data["sha"] = sha

            # 提交
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers=self.headers,
                method="PUT"
            )

            with urllib.request.urlopen(req) as response:
                return response.status in [200, 201]

        except Exception as e:
            print(f"GitHub提交失败: {e}")
            return False


# ============================================================
# 主更新器类
# ============================================================

class SkillAutoUpdater:
    """Skill自动更新器主类"""

    def __init__(self, config: Dict = None):
        self.config = config or CONFIG
        self.version_ctrl = VersionControl()
        self.content_updater = ContentUpdater()
        self.github_sync = None
        if self.config.get("github_repo") and self.config.get("github_token"):
            self.github_sync = GitHubSync(
                self.config["github_repo"],
                self.config["github_token"]
            )

    def check_needs_update(self, skill_id: str) -> bool:
        """检查是否需要更新"""
        skill_dir = Path(self.config["skills_dir"]) / skill_id
        meta_file = skill_dir / "_meta.json"

        if not meta_file.exists():
            return False

        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)

            last_update = meta.get("last_auto_update", "")
            if not last_update:
                return True

            last_date = datetime.datetime.fromisoformat(last_update)
            days_since = (datetime.datetime.now() - last_date).days

            return days_since >= self.config.get("update_interval_days", 7)

        except Exception:
            return True

    def get_skill_info(self, skill_id: str) -> Dict:
        """获取Skill信息"""
        skill_dir = Path(self.config["skills_dir"]) / skill_id
        meta_file = skill_dir / "_meta.json"

        if meta_file.exists():
            with open(meta_file, 'r') as f:
                return json.load(f)
        return {}

    def update_skill(self, skill_id: str, search_results: List[Dict]) -> bool:
        """更新单个Skill"""
        skill_dir = Path(self.config["skills_dir"]) / skill_id
        skill_file = skill_dir / "SKILL.md"

        if not skill_file.exists():
            print(f"Skill文件不存在: {skill_id}")
            return False

        # 备份原文件
        self._backup_file(skill_file)

        # 更新内容
        updated = self.content_updater.update_skill_file(
            str(skill_file),
            search_results,
            "auto-update"
        )

        if updated:
            # 更新版本号
            meta = self.get_skill_info(skill_id)
            current_version = meta.get("version", "1.0.0")
            new_version = self.version_ctrl.bump_version(current_version, "minor")
            self.version_ctrl.update_version_in_file(str(skill_file), new_version)

            # 更新元数据
            meta["version"] = new_version
            meta["last_auto_update"] = datetime.datetime.now().isoformat()

            with open(skill_dir / "_meta.json", 'w') as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)

            # 记录更新日志
            changelog_entry = self.version_ctrl.generate_changelog_entry(
                "auto-update",
                f"自动更新行业动态，发现 {len(search_results)} 条新趋势"
            )
            self.version_ctrl.append_changelog(str(skill_file), changelog_entry)

        return updated

    def _backup_file(self, file_path: Path):
        """备份文件"""
        backup_dir = Path(self.config.get("backup_dir", "./backups"))
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"{file_path.stem}_{timestamp}.md"

        import shutil
        shutil.copy2(file_path, backup_file)
        print(f"已备份: {backup_file}")

    def sync_to_github(self, file_path: str, message: str) -> bool:
        """同步到GitHub"""
        if not self.github_sync:
            print("GitHub未配置，跳过同步")
            return False

        if not self.github_sync.check_connection():
            print("GitHub连接失败，跳过同步")
            return False

        return self.github_sync.commit_changes(file_path, message)

    def run_update_cycle(self) -> Dict:
        """执行完整更新周期"""
        results = {
            "updated_skills": [],
            "failed_skills": [],
            "github_synced": [],
            "timestamp": datetime.datetime.now().isoformat()
        }

        for skill_id, keywords in INDUSTRY_KEYWORDS.items():
            try:
                if not self.check_needs_update(skill_id):
                    print(f"跳过 {skill_id}（无需更新）")
                    continue

                print(f"\n正在更新 {skill_id}...")

                # 模拟搜索结果（实际使用时会调用MCP工具）
                # search_results = self._fetch_latest_trends(keywords)
                search_results = []  # 实际使用时应填充

                # 更新Skill
                if self.update_skill(skill_id, search_results):
                    results["updated_skills"].append(skill_id)

                    # 同步到GitHub
                    skill_file = f"{self.config['skills_dir']}/{skill_id}/SKILL.md"
                    if self.sync_to_github(skill_file, f"Auto-update: {skill_id}"):
                        results["github_synced"].append(skill_id)

            except Exception as e:
                print(f"更新 {skill_id} 失败: {e}")
                results["failed_skills"].append(skill_id)

        # 记录更新日志
        self._log_update_cycle(results)

        return results

    def _log_update_cycle(self, results: Dict):
        """记录更新周期日志"""
        log_dir = Path(self.config.get("log_dir", "./logs"))
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"update_{datetime.datetime.now().strftime('%Y%m')}.log"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"更新周期: {results['timestamp']}\n")
            f.write(f"成功更新: {results['updated_skills']}\n")
            f.write(f"失败技能: {results['failed_skills']}\n")
            f.write(f"GitHub同步: {results['github_synced']}\n")


# ============================================================
# Skill集成接口 - 供MCP工具调用
# ============================================================

def skill_on_load_hook(skill_id: str) -> Dict:
    """
    Skill加载时自动调用的钩子函数
    功能：检查更新、返回最新状态
    """
    updater = SkillAutoUpdater()

    needs_update = updater.check_needs_update(skill_id)
    skill_info = updater.get_skill_info(skill_id)

    return {
        "skill_id": skill_id,
        "needs_update": needs_update,
        "version": skill_info.get("version", "unknown"),
        "last_update": skill_info.get("last_auto_update", "从未更新"),
        "message": "发现新版本可用，建议运行更新" if needs_update else "已是最新版本"
    }


def skill_manual_update(skill_id: str, search_results: List[Dict]) -> bool:
    """
    手动触发Skill更新
    供Agent在处理行业经验任务时调用
    """
    updater = SkillAutoUpdater()

    # 执行更新
    success = updater.update_skill(skill_id, search_results)

    if success:
        # 同步到GitHub
        skill_file = f"{CONFIG['skills_dir']}/{skill_id}/SKILL.md"
        updater.sync_to_github(skill_file, f"Manual update: {skill_id}")

    return success


def sync_all_skills_to_github() -> Dict:
    """
    同步所有Skill到GitHub
    """
    updater = SkillAutoUpdater()
    results = {"synced": [], "failed": []}

    for skill_id in INDUSTRY_KEYWORDS.keys():
        skill_file = f"{CONFIG['skills_dir']}/{skill_id}/SKILL.md"
        if updater.sync_to_github(skill_file, f"Skill sync: {skill_id}"):
            results["synced"].append(skill_id)
        else:
            results["failed"].append(skill_id)

    return results


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("经验萃取Skill自动更新系统")
    print("=" * 60)

    updater = SkillAutoUpdater()

    # 检查GitHub连接
    if updater.github_sync:
        if updater.github_sync.check_connection():
            print("✓ GitHub连接正常")
        else:
            print("✗ GitHub连接失败")

    # 执行更新
    print("\n开始检查更新...")
    results = updater.run_update_cycle()

    print("\n" + "=" * 60)
    print("更新结果:")
    print(f"  更新技能: {results['updated_skills']}")
    print(f"  失败技能: {results['failed_skills']}")
    print(f"  GitHub同步: {results['github_synced']}")
    print("=" * 60)