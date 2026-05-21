#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报/月报自动生成器
从 Git 提交记录、任务系统、文档变更中提取工作成果，自动生成结构化周报/月报
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import re


@dataclass
class GitCommit:
    hash: str
    author: str
    date: str
    message: str
    files_changed: List[str] = field(default_factory=list)


@dataclass
class TaskItem:
    id: str
    title: str
    status: str
    priority: str = ""
    description: str = ""
    completed_date: Optional[str] = None


@dataclass
class DocumentChange:
    path: str
    change_type: str
    modified_date: str = ""


@dataclass
class GitAuthConfig:
    """Git 认证配置"""
    auth_type: str = "ssh"  # ssh, https, token
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    ssh_key_path: Optional[str] = None
    remote_url: Optional[str] = None


@dataclass
class ReportConfig:
    report_type: str = "weekly"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    git_repo_path: str = "."
    include_git: bool = True
    include_tasks: bool = True
    include_documents: bool = True
    author_name: str = ""
    team_name: str = ""
    highlights: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)
    plans: List[str] = field(default_factory=list)
    git_auth: Optional[GitAuthConfig] = None
    private_repo: bool = False


class GitExtractor:
    def __init__(self, repo_path: str = ".", auth_config: Optional[GitAuthConfig] = None):
        self.repo_path = repo_path
        self.auth_config = auth_config
        self._setup_auth()
    
    def _setup_auth(self):
        """配置 Git 认证"""
        if not self.auth_config:
            return
        
        try:
            if self.auth_config.auth_type == "ssh" and self.auth_config.ssh_key_path:
                self._setup_ssh_auth()
            elif self.auth_config.auth_type == "token" and self.auth_config.token:
                self._setup_token_auth()
            elif self.auth_config.auth_type == "https" and self.auth_config.username and self.auth_config.password:
                self._setup_https_auth()
        except Exception as e:
            print(f"⚠️  Git 认证配置失败：{e}")
    
    def _setup_ssh_auth(self):
        """配置 SSH 认证"""
        ssh_key = self.auth_config.ssh_key_path
        if ssh_key and os.path.exists(ssh_key):
            os.environ["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key} -o IdentitiesOnly=yes"
    
    def _setup_token_auth(self):
        """配置 Token 认证"""
        token = self.auth_config.token
        if token:
            os.environ["GIT_ASKPASS"] = "/bin/echo"
            if self.auth_config.remote_url:
                self._update_remote_url(token)
    
    def _setup_https_auth(self):
        """配置 HTTPS 认证"""
        username = self.auth_config.username
        password = self.auth_config.password
        if username and password:
            credential_helper = f"!f() {{ test \"$1\" = username && echo {username} || echo {password}; }}; f"
            os.environ["GIT_ASKPASS"] = "/bin/echo"
            if self.auth_config.remote_url:
                self._update_remote_url_with_auth(username, password)
    
    def _update_remote_url(self, token: str):
        """使用 token 更新远程仓库 URL"""
        try:
            if self.auth_config.remote_url:
                new_url = self.auth_config.remote_url.replace("https://", f"https://{token}@")
                subprocess.run(
                    ["git", "-C", self.repo_path, "remote", "set-url", "origin", new_url],
                    capture_output=True,
                    check=False
                )
        except Exception:
            pass
    
    def _update_remote_url_with_auth(self, username: str, password: str):
        """使用用户名密码更新远程仓库 URL"""
        try:
            if self.auth_config.remote_url:
                new_url = self.auth_config.remote_url.replace(
                    "https://", 
                    f"https://{username}:{password}@"
                )
                subprocess.run(
                    ["git", "-C", self.repo_path, "remote", "set-url", "origin", new_url],
                    capture_output=True,
                    check=False
                )
        except Exception:
            pass
    
    def get_commits(self, start_date: str, end_date: str) -> List[GitCommit]:
        try:
            if self.private_repo and self.auth_config:
                self._ensure_auth_setup()
            
            cmd = [
                "git", "-C", self.repo_path, "log",
                f"--since={start_date}",
                f"--until={end_date}",
                "--pretty=format:%H|%an|%ad|%s",
                "--date=iso",
                "--name-status"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return self._parse_git_log(result.stdout)
        except subprocess.CalledProcessError as e:
            error_msg = str(e.stderr) if e.stderr else str(e)
            if "authentication failed" in error_msg.lower() or "could not read username" in error_msg.lower():
                print(f"❌ Git 认证失败：请检查私有仓库认证配置")
                print(f"   错误信息：{error_msg}")
                print(f"   解决方案：")
                print(f"     1. 使用 SSH 方式：配置 SSH Key")
                print(f"     2. 使用 Token 方式：生成 Personal Access Token")
                print(f"     3. 使用 HTTPS 方式：确保用户名密码正确")
            elif "repository not found" in error_msg.lower():
                print(f"❌ 无法访问私有仓库：{self.repo_path}")
                print(f"   请确认仓库路径正确且有访问权限")
            else:
                print(f"Git 命令执行失败：{error_msg}")
            return []
        except Exception as e:
            print(f"Git 操作异常：{e}")
            return []
    
    def _ensure_auth_setup(self):
        """确保认证已配置"""
        if not self.auth_config:
            print("⚠️  访问私有仓库需要配置认证信息")
            print("   请在配置文件中添加 git_auth 配置")
    
    def _parse_git_log(self, log_output: str) -> List[GitCommit]:
        commits = []
        current_commit = None
        files = []
        
        for line in log_output.split("\n"):
            if not line.strip():
                if current_commit and files:
                    current_commit.files_changed = files
                    commits.append(current_commit)
                    current_commit = None
                    files = []
                continue
            
            if "|" in line and len(line.split("|")) >= 4:
                if current_commit:
                    current_commit.files_changed = files
                    commits.append(current_commit)
                
                parts = line.split("|", 3)
                current_commit = GitCommit(
                    hash=parts[0][:8],
                    author=parts[1],
                    date=parts[2],
                    message=parts[3]
                )
                files = []
            elif current_commit and line.startswith(("A\t", "M\t", "D\t")):
                files.append(line.split("\t", 1)[-1])
        
        if current_commit:
            current_commit.files_changed = files
            commits.append(current_commit)
        
        return commits
    
    def get_commit_stats(self, commits: List[GitCommit]) -> Dict[str, Any]:
        if not commits:
            return {}
        
        authors = {}
        daily_commits = {}
        file_types = {}
        
        for commit in commits:
            authors[commit.author] = authors.get(commit.author, 0) + 1
            date = commit.date.split()[0]
            daily_commits[date] = daily_commits.get(date, 0) + 1
            
            for file in commit.files_changed:
                ext = Path(file).suffix or "无扩展名"
                file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            "total_commits": len(commits),
            "authors": authors,
            "daily_commits": daily_commits,
            "file_types": file_types,
            "most_active_day": max(daily_commits.items(), key=lambda x: x[1])[0] if daily_commits else None
        }


class TaskExtractor:
    def extract_from_file(self, file_path: str) -> List[TaskItem]:
        if not os.path.exists(file_path):
            return []
        
        ext = Path(file_path).suffix.lower()
        if ext == ".json":
            return self._parse_json_tasks(file_path)
        elif ext in [".md", ".txt"]:
            return self._parse_markdown_tasks(file_path)
        return []
    
    def _parse_json_tasks(self, file_path: str) -> List[TaskItem]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            tasks = []
            for item in data.get("tasks", []):
                tasks.append(TaskItem(
                    id=item.get("id", ""),
                    title=item.get("title", ""),
                    status=item.get("status", ""),
                    priority=item.get("priority", ""),
                    description=item.get("description", ""),
                    completed_date=item.get("completed_date")
                ))
            return tasks
        except Exception as e:
            print(f"解析任务文件失败：{e}")
            return []
    
    def _parse_markdown_tasks(self, file_path: str) -> List[TaskItem]:
        tasks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            pattern = r"- \[([ x])\]\s+(.+?)(?:\s+\(([^)]+)\))?"
            matches = re.findall(pattern, content)
            
            for match in matches:
                status = "completed" if match[0] == "x" else "pending"
                tasks.append(TaskItem(
                    id=f"task-{len(tasks)+1}",
                    title=match[1].strip(),
                    status=status,
                    priority=match[2] if match[2] else ""
                ))
        except Exception as e:
            print(f"解析 Markdown 任务失败：{e}")
        
        return tasks


class DocumentChangeTracker:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
    
    def track_changes(self, start_date: str, end_date: str) -> List[DocumentChange]:
        changes = []
        doc_extensions = [".md", ".txt", ".rst", ".doc", ".docx", ".pdf"]
        
        try:
            cmd = [
                "git", "-C", self.repo_path, "log",
                f"--since={start_date}",
                f"--until={end_date}",
                "--name-only",
                "--pretty=format:%ad"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            current_date = None
            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue
                
                if re.match(r"\d{4}-\d{2}-\d{2}", line):
                    current_date = line
                elif any(line.endswith(ext) for ext in doc_extensions):
                    changes.append(DocumentChange(
                        path=line,
                        change_type="modified",
                        modified_date=current_date or ""
                    ))
        except Exception as e:
            print(f"追踪文档变更失败：{e}")
        
        return changes
    
    def categorize_documents(self, changes: List[DocumentChange]) -> Dict[str, List[DocumentChange]]:
        categories = {
            "documentation": [],
            "api": [],
            "readme": [],
            "changelog": [],
            "other": []
        }
        
        for change in changes:
            path_lower = change.path.lower()
            if "api" in path_lower or "swagger" in path_lower:
                categories["api"].append(change)
            elif "readme" in path_lower:
                categories["readme"].append(change)
            elif "changelog" in path_lower or "change" in path_lower:
                categories["changelog"].append(change)
            elif any(doc in path_lower for doc in ["doc", "wiki", "guide"]):
                categories["documentation"].append(change)
            else:
                categories["other"].append(change)
        
        return categories


class ReportGenerator:
    def __init__(self, config: ReportConfig):
        self.config = config
        self.git_extractor = GitExtractor(config.git_repo_path, config.git_auth)
        self.task_extractor = TaskExtractor()
        self.doc_tracker = DocumentChangeTracker(config.git_repo_path)
    
    def generate(self) -> str:
        start_date = self.config.start_date or self._get_default_start_date()
        end_date = self.config.end_date or datetime.now().strftime("%Y-%m-%d")
        
        sections = []
        
        if self.config.include_git:
            commits = self.git_extractor.get_commits(start_date, end_date)
            stats = self.git_extractor.get_commit_stats(commits)
            sections.append(self._generate_git_section(commits, stats))
        
        if self.config.include_tasks:
            tasks = self.task_extractor.extract_from_file("tasks.json")
            if not tasks:
                tasks = self.task_extractor.extract_from_file("TODO.md")
            sections.append(self._generate_task_section(tasks))
        
        if self.config.include_documents:
            doc_changes = self.doc_tracker.track_changes(start_date, end_date)
            sections.append(self._generate_document_section(doc_changes))
        
        sections.append(self._generate_highlights_section())
        sections.append(self._generate_challenges_section())
        sections.append(self._generate_plans_section())
        
        return self._assemble_report(sections, start_date, end_date)
    
    def _get_default_start_date(self) -> str:
        now = datetime.now()
        if self.config.report_type == "weekly":
            start = now - timedelta(days=now.weekday())
        else:
            start = now.replace(day=1)
        return start.strftime("%Y-%m-%d")
    
    def _generate_git_section(self, commits: List[GitCommit], stats: Dict) -> str:
        if not commits:
            return "## 代码提交\n\n本周暂无代码提交记录。\n"
        
        lines = ["## 代码提交\n"]
        lines.append(f"- **总提交数**: {stats.get('total_commits', 0)}\n")
        
        if stats.get('most_active_day'):
            lines.append(f"- **最活跃日期**: {stats['most_active_day']}\n")
        
        lines.append("\n### 主要提交\n")
        
        for commit in commits[:10]:
            lines.append(f"- `{commit.hash}` {commit.message} ({commit.author}, {commit.date.split()[0]})\n")
        
        if stats.get('file_types'):
            lines.append("\n### 文件类型分布\n")
            for ext, count in sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:5]:
                lines.append(f"- {ext}: {count} 次修改\n")
        
        return "".join(lines)
    
    def _generate_task_section(self, tasks: List[TaskItem]) -> str:
        lines = ["## 任务完成情况\n"]
        
        if not tasks:
            lines.append("本周暂无任务记录。\n")
            return "".join(lines)
        
        completed = [t for t in tasks if t.status == "completed"]
        pending = [t for t in tasks if t.status == "pending"]
        
        lines.append(f"- **完成任务数**: {len(completed)}\n")
        lines.append(f"- **进行中任务数**: {len(pending)}\n\n")
        
        if completed:
            lines.append("### 已完成任务\n")
            for task in completed:
                priority_tag = f" [{task.priority}]" if task.priority else ""
                lines.append(f"- ✅ [{task.id}]{priority_tag} {task.title}\n")
            lines.append("\n")
        
        if pending:
            lines.append("### 进行中任务\n")
            for task in pending:
                priority_tag = f" [{task.priority}]" if task.priority else ""
                lines.append(f"- 🔄 [{task.id}]{priority_tag} {task.title}\n")
        
        return "".join(lines)
    
    def _generate_document_section(self, changes: List[DocumentChange]) -> str:
        lines = ["## 文档更新\n"]
        
        if not changes:
            lines.append("本周暂无文档更新。\n")
            return "".join(lines)
        
        categorized = self.doc_tracker.categorize_documents(changes)
        
        for category, docs in categorized.items():
            if docs:
                category_names = {
                    "documentation": "技术文档",
                    "api": "API 文档",
                    "readme": "README",
                    "changelog": "变更日志",
                    "other": "其他文档"
                }
                lines.append(f"### {category_names.get(category, category)}\n")
                for doc in docs:
                    lines.append(f"- 📄 {doc.path} ({doc.modified_date})\n")
                lines.append("\n")
        
        return "".join(lines)
    
    def _generate_highlights_section(self) -> str:
        lines = ["## 工作亮点\n"]
        
        if self.config.highlights:
            for highlight in self.config.highlights:
                lines.append(f"- ✨ {highlight}\n")
        else:
            lines.append("请补充本周工作亮点...\n")
        
        lines.append("\n")
        return "".join(lines)
    
    def _generate_challenges_section(self) -> str:
        lines = ["## 遇到的问题与挑战\n"]
        
        if self.config.challenges:
            for challenge in self.config.challenges:
                lines.append(f"- ⚠️ {challenge}\n")
        else:
            lines.append("请补充遇到的问题和挑战...\n")
        
        lines.append("\n")
        return "".join(lines)
    
    def _generate_plans_section(self) -> str:
        lines = ["## 下周/下月计划\n"]
        
        if self.config.plans:
            for plan in self.config.plans:
                lines.append(f"- 📌 {plan}\n")
        else:
            lines.append("请补充下周/下月工作计划...\n")
        
        lines.append("\n")
        return "".join(lines)
    
    def _assemble_report(self, sections: List[str], start_date: str, end_date: str) -> str:
        report_type = "周报" if self.config.report_type == "weekly" else "月报"
        
        header = f"# {report_type} ({start_date} ~ {end_date})\n\n"
        
        if self.config.author_name:
            header += f"**汇报人**: {self.config.author_name}\n"
        if self.config.team_name:
            header += f"**团队**: {self.config.team_name}\n"
        
        header += "\n---\n\n"
        
        return header + "".join(sections)
