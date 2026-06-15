# ClawHub 发布指南

## 概述

本文档说明如何将经验萃取 Skills 发布到 ClawHub 技能库。

## 方法一：使用 GitHub Actions（推荐）

### 步骤 1：创建 GitHub Secret

1. 进入 GitHub 仓库: https://github.com/smxtx/exp-distill-skills/settings/secrets/actions
2. 点击 **New repository secret**
3. 名称输入: `CLAWHUB_TOKEN`
4. 值输入您的 ClawHub API Token（格式: `clh_xxx`）
5. 点击 **Add secret**

### 步骤 2：创建 Workflow 文件

由于 GitHub API 限制，请手动创建以下文件：

**文件路径**: `.github/workflows/publish-to-clawhub.yml`

```yaml
name: Publish Skills to ClawHub

on:
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install ClawHub CLI
        run: npm install -g clawhub

      - name: Login to ClawHub
        run: clawhub login --token ${{ secrets.CLAWHUB_TOKEN }} --no-browser
        env:
          CLAWHUB_DISABLE_TELEMETRY: '1'

      - name: Publish all skills
        run: |
          for SKILL_DIR in jing-yan-cui-qu industry-exp-distill tech-exp-distill finance-exp-distill mfg-exp-distill; do
            if [ -d "$SKILL_DIR" ]; then
              echo "Publishing $SKILL_DIR..."
              clawhub publish "./$SKILL_DIR" \
                --slug "$SKILL_DIR" \
                --name "$SKILL_DIR" \
                --version "1.0.0" \
                --changelog "Initial release" \
                --tags "experience-distillation,minimax,openclaw"
              echo "✓ Published $SKILL_DIR"
            fi
          done
```

### 步骤 3：触发 Workflow

1. 进入仓库的 **Actions** 页面
2. 选择 **Publish Skills to ClawHub** workflow
3. 点击 **Run workflow** 按钮
4. Workflow 将自动发布所有 5 个技能到 ClawHub

## 方法二：使用 ClawHub CLI 直接发布

如果您在本地有 Git 环境和 Node.js：

```bash
# 1. 安装 ClawHub CLI
npm install -g clawhub

# 2. 登录 ClawHub
clawhub login --token YOUR_CLAWHUB_TOKEN

# 3. 克隆仓库
git clone https://github.com/smxtx/exp-distill-skills.git
cd exp-distill-skills

# 4. 发布每个技能
for skill in jing-yan-cui-qu industry-exp-distill tech-exp-distill finance-exp-distill mfg-exp-distill; do
  clawhub publish "./$skill" --slug "$skill" --name "$skill" --version "1.0.0"
done
```

## 获取 ClawHub Token

1. 访问 https://clawhub.ai
2. 使用 GitHub 账号登录
3. 进入 Settings → API Keys
4. 创建新的 CLI Token（格式: `clh_xxx`）

## 技能列表

| Skill | 描述 | Tags |
|-------|------|------|
| jing-yan-cui-qu | 个人经验萃取 | experience-distillation,minimax |
| industry-exp-distill | ISIC行业经验萃取 | industry,ISIC,minimax |
| tech-exp-distill | 信息技术行业经验 | tech,IT,minimax |
| finance-exp-distill | 金融行业经验 | finance,banking,minimax |
| mfg-exp-distill | 制造业经验 | manufacturing,minimax |

## 验证发布

发布后访问:
- https://clawhub.ai/skills/jing-yan-cui-qu
- https://clawhub.ai/skills/industry-exp-distill

---

**生成时间**: 2024-01