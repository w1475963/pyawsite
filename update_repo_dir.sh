#!/bin/bash

# 解析参数
repo_configs=()
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --repo-url)
            repo_url="$2"
            shift 2
            ;;
        --branch)
            branch="$2"
            shift 2
            ;;
        --target-folder)
            target_folder="$2"
            shift 2
            ;;
        --local-dir)
            local_dir="$2"
            shift 2
            ;;
        *)
            # 新仓库参数组开始（无关键字，直接按顺序传递参数）
            # 支持简化格式：bash script.sh url branch folder dir
            repo_url="$1"
            branch="${2:-main}"  # 默认分支为 main
            target_folder="$3"
            local_dir="$4"
            shift 4
            ;;
    esac

    # 当四个核心参数齐全时，保存配置并重置临时变量
    if [[ -n "$repo_url" && -n "$target_folder" && -n "$local_dir" ]]; then
        repo_configs+=("repo_url=$repo_url branch=${branch:-main} target_folder=$target_folder local_dir=$local_dir")
        unset repo_url branch target_folder local_dir
    fi
done

# 验证参数是否合法
if [[ ${#repo_configs[@]} -eq 0 ]]; then
    echo "错误：未提供任何仓库配置参数"
    echo "用法："
    echo "bash $0 --repo-url URL --branch BRANCH --target-folder FOLDER --local-dir PATH"
    echo "或（简化格式）：bash $0 URL [BRANCH] FOLDER PATH"
    exit 1
fi

# 处理每个仓库
for config in "${repo_configs[@]}"; do
    # 解析配置
    eval "$config"
    echo "==== 处理仓库：$repo_url ===="

    # 初始化或进入本地仓库
    if [ ! -d "$local_dir" ]; then
        mkdir -p "$local_dir"
        cd "$local_dir"
        git init
        git remote add origin "$repo_url"
        git fetch --depth 1 origin "$branch"
        git checkout FETCH_HEAD
        git sparse-checkout init --cone
        git sparse-checkout set "$target_folder"
        echo "首次克隆完成：$local_dir"
    else
        cd "$local_dir"
    fi

    # 检查并拉取更新
    local_hash=$(git rev-parse HEAD 2>/dev/null)
    remote_hash=$(git rev-parse origin/"$branch" 2>/dev/null)

    if [ "$local_hash" != "$remote_hash" ] && [ -n "$remote_hash" ]; then
        echo "发现更新，开始拉取..."
        git fetch --depth 1 origin "$branch"
        git reset --hard FETCH_HEAD
        echo "更新完成：$local_dir"
    else
        echo "已是最新版本：$local_dir"
    fi

    # 清理缓存
    git gc --prune=now --quiet
    echo "==== 处理完成 ===="
    echo ""
done

