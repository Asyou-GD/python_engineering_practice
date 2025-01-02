#!/bin/bash

# 配置 Git 用户名
git config --global user.name "GD"

# 配置 Git 用户邮箱
git config --global user.email "gd0818109@163.com"

echo "Git user.name 和 user.email 已成功配置！"

git init
echo "git 已初始化！"

git remote add origin git@github.com:Asyou-GD/python_engineering_practice.git
echo "git 已配置远程地址！"

echo "远程地址为"
git remote -vv

git branch -M master
echo "转换为master分支"

# 防止窗口秒退，等待用户按下 Enter
read -p "按下回车键退出..."