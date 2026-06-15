# 手动上传指南 - GitHub

## 问题说明

当前GitHub token缺少`repo`权限，无法自动创建仓库。请按以下步骤手动创建：

## 步骤1：在GitHub.com上创建仓库

1. 登录 GitHub: https://github.com (账号: smxtx)
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   - **Owner**: smxtx
   - **Repository name**: `exp-distill-skills`
   - **Description**: `经验萃取Skill库 - 汇聚个人与行业智慧，萃取可复用的工作方法论`
   - **Visibility**: Public
   - **勾选**: 不要勾选 "Add a README file" (我们已有)
   - **勾选**: 不要勾选 "Initialize this repository with a README"
4. 点击 **Create repository**

## 步骤2：推送本地代码

打开终端，运行以下命令：

```bash
cd /workspace/exp-distill-skills

# 更新远程仓库地址
git remote set-url origin https://github.com/smxtx/exp-distill-skills.git

# 推送到GitHub
git push -u origin main
```

## 验证上传成功

刷新 GitHub 仓库页面，应能看到以下文件结构：

```
exp-distill-skills/
├── README.md
├── .gitignore
├── jing-yan-cui-qu/
│   ├── SKILL.md
│   ├── _meta.json
│   └── references/
├── industry-exp-distill/
│   ├── SKILL.md
│   ├── _meta.json
│   └── references/
├── tech-exp-distill/
│   ├── SKILL.md
│   └── _meta.json
├── finance-exp-distill/
│   ├── SKILL.md
│   └── _meta.json
├── mfg-exp-distill/
│   ├── SKILL.md
│   └── _meta.json
└── _update_system/
    ├── configs/
    ├── scripts/
    ├── logs/
    ├── backups/
    └── README.md
```

---

**生成时间**: 2024-01
**仓库地址**: https://github.com/smxtx/exp-distill-skills