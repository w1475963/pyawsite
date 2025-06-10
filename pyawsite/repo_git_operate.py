import os
import subprocess
from typing import Optional


def manage_git_repo(
    repo_url: str,
    target_folder: str,
    local_dir: str,
    branch: str = "main",
    quiet: bool = False,
) -> bool:
    """管理Git仓库克隆与更新（支持稀疏检出）"""
    if not all([repo_url, target_folder, local_dir]):
        _log("错误：缺少必要参数", quiet)
        return False

    _log(f"处理仓库: {repo_url}", quiet)
    _log(f"本地目录: {local_dir}, 目标文件夹: {target_folder}", quiet)

    try:
        os.makedirs(local_dir, exist_ok=True)
        is_git = os.path.exists(f"{local_dir}/.git")

        if not is_git:
            _log("开始克隆", quiet)
            _git(["init"], local_dir, quiet)
            _git(["remote", "add", "origin", repo_url], local_dir, quiet)
            _git(["sparse-checkout", "init", "--cone"], local_dir, quiet)
            _git(["sparse-checkout", "set", target_folder], local_dir, quiet)
            _git(["fetch", "--depth=1", "origin", branch], local_dir, quiet)
            _git(["checkout", "FETCH_HEAD"], local_dir, quiet)
            _log("克隆完成", quiet)

        os.chdir(local_dir)
        _git(["fetch", "--depth=0", "origin", branch], quiet=quiet)
        local_hash = _git_hash("HEAD", quiet)
        remote_hash = _git_hash(f"origin/{branch}", quiet)

        if local_hash != remote_hash and remote_hash:
            _log("拉取更新", quiet)
            _git(["fetch", "--depth=1", "origin", branch], quiet=quiet)
            _git(["reset", "--hard", "FETCH_HEAD"], quiet=quiet)
            _log("更新完成", quiet)
        else:
            _log("已是最新", quiet)

        _git(["gc", "--prune=now", "--quiet"], quiet=quiet)
        _log("处理完成", quiet)
        return True

    except Exception as e:
        _log(f"操作失败: {str(e)}", quiet)
        return False


def _git(
    cmd: list[str], cwd: Optional[str] = None, check: bool = True, quiet: bool = False
) -> None:
    """执行Git命令"""
    try:
        subprocess.run(
            ["git"] + cmd,
            cwd=cwd,
            check=check,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None,
        )
    except subprocess.CalledProcessError:
        if not quiet:
            raise RuntimeError(f"命令失败: {'git ' + ' '.join(cmd)}")


def _git_hash(ref: str, quiet: bool = False) -> str:
    """获取Git哈希值"""
    result = subprocess.run(["git", "rev-parse", ref], capture_output=True, text=True)
    if result.returncode != 0 and not quiet:
        print(f"哈希获取失败: {ref}")
    return result.stdout.strip()


def _log(msg: str, quiet: bool) -> None:
    """条件日志输出"""
    if not quiet:
        print(msg)



