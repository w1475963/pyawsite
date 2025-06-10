from django.urls import path, include, re_path
from django.conf.urls.static import static
from pathlib import Path
from typing import TypedDict
import os.path
import sys
from django.views.static import serve

from .repo_git_operate import manage_git_repo


class RepoAppInfo(TypedDict):
    show_name: str
    repo_name: str
    base_url: str
    base_file: str
    files: list[str] | dict[str, str]
    base_files_path:list[str]
    base_static_url: str
    base_static_dir: list[str]


apps: dict[str, RepoAppInfo] = {
    "pyawsite_front": {
        "show_name": "站点",
        "repo_name": "",
        "base_url": "wap/",
        "base_file": "index.html",
        "files": ["favicon.ico"],
        "base_files_path":["dist"],
        "base_static_url": "wap/assets/",
        "base_static_dir": ["dist", "assets"],
    },
    "daily_todos": {
        "show_name": "站点",
        "repo_name": "",
        "base_url": "daily_todos/",
        "base_file": "index.html",
        "files": ["favicon.ico"],
        "base_files_path":["dist"],
        "base_static_url": "daily_todos/assets/",
        "base_static_dir": ["dist", "assets"],
    },
}


def update_repos():
    for app, app_info in apps.items():
        if app_info["repo_name"]:
            manage_git_repo(
                repo_url=f"https://github.com/{app_info['repo_name']}",
                target_folder="dist",
                local_dir=os.path.join(os.getenv("PROJECT_ROOT",os.getenv("HOME","")),"repos",app),
                branch="release",
            )



def get_app_urls(app: str):
    info = apps[app]
    if not isinstance(info["files"], dict):
        info["files"] = {s: s for s in info["files"]}
    return (
        *static(
            info["base_static_url"],
            document_root=f"repos/{app}/{'/'.join(info['base_static_dir'])}",
        ),
        *(
            path(
                info["base_url"] + u,
                serve,
                {"path": p, "document_root": f"repos/{app}/{'/'.join(info['base_files_path'])}"},
            )
            for u, p in info["files"].items()
        ),
        re_path(
            f"^{info['base_url']}.*$",
            serve,
            {
                "path": info["base_file"],
                "document_root": f"repos/{app}/{'/'.join(info['base_files_path'])}",
            },
        ),
    )

def get_urls():
    res = []
    for app in apps:
        res.extend(get_app_urls(app))
    return res



if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "update-repos":
                update_repos()
