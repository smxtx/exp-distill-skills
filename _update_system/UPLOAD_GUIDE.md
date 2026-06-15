# 经验萃取Skill - 上传配置指南

## 概述

本文档说明如何将创建的经验萃取Skill上传到GitHub和MAXCLAW技能库。

## 1. GitHub上传配置

### 方式一：使用GitHub CLI

```bash
# 安装GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
apt update && apt install gh

# 登录
gh auth login

# 创建仓库
gh repo create exp-distill-skills --public --source=. --push
```

### 方式二：使用Git Token

需要提供以下信息：
- `GITHUB_REPO`: 仓库名称（如 `username/exp-distill-skills`）
- `GITHUB_TOKEN`: Personal Access Token

### 获取GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制Token

## 2. MAXCLAW技能库上传

MAXCLAW技能库需要通过API上传。请提供：

- `MAXCLAW_API_KEY`: API访问密钥
- `MAXCLAW_API_URL`: API端点（可选，使用默认）

## 3. 经验萃取Skill清单

本次创建的经验萃取Skill包括：

| Skill ID | 名称 | 描述 |
|----------|------|------|
| `jing-yan-cui-qu` | 个人经验萃取 | 回顾工作、归纳逻辑、提取方法论 |
| `industry-exp-distill` | 行业经验萃取 | ISIC标准分类、行业最佳实践 |
| `tech-exp-distill` | 信息技术行业 | 敏捷开发、DevOps、架构设计 |
| `finance-exp-distill` | 金融行业 | 风险管理、客户服务、数字化 |
| `mfg-exp-distill` | 制造业 | 精益生产、质量管理、供应链 |
| `_update_system` | 自动更新系统 | 联网检索、版本控制、GitHub同步 |

## 4. 上传脚本

上传脚本位于：

```
/workspace/.minimax/skills/_update_system/scripts/update_skills.py
```

主要功能：
- 自动更新Skill内容
- 版本号管理
- GitHub同步
- 备份管理

## 5. 后续步骤

1. 配置GitHub凭证
2. 运行上传脚本
3. 验证上传结果

---

**版本**：1.0.0 | **创建日期**：2024-01