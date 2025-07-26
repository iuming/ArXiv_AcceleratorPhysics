@echo off
REM 推送到GitLab的Windows批处理脚本
REM 作者：Ming Liu
REM 创建日期：2025-07-26

echo === 推送代码到 GitLab (code.ihep.ac.cn) ===

REM 检查是否有GitLab远程仓库
git remote | findstr "gitlab" >nul
if %errorlevel% neq 0 (
    echo 添加GitLab远程仓库...
    git remote add gitlab git@code.ihep.ac.cn:mliu/ArXiv_AcceleratorPhysics.git
) else (
    echo GitLab远程仓库已存在
)

REM 显示远程仓库
echo 当前远程仓库：
git remote -v

echo.
echo 开始推送到GitLab...

REM 推送主分支
git push gitlab main

echo.
echo ✅ 推送完成！
echo.
echo 接下来的步骤：
echo 1. 访问 https://code.ihep.ac.cn/mliu/ArXiv_AcceleratorPhysics
echo 2. 前往 Settings ^> CI/CD ^> Variables 配置API密钥
echo 3. 前往 CI/CD ^> Schedules 配置每日定时任务
echo 4. 在 CI/CD ^> Pipelines 查看管道运行状态
echo.
echo 需要配置的环境变量：
echo - OPENAI_API_KEY
echo - DEEPSEEK_API_KEY
echo - HAI_API_KEY
echo - ANTHROPIC_API_KEY

pause
