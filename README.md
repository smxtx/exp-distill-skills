# 经验萃取Skill库 (Experience Distillation Skills)

> **核心使命**：汇聚个人与行业智慧，萃取可复用的工作方法论

## 概述

这是一个经验萃取Skill集合，专注于帮助用户回顾工作经历、归纳工作逻辑、提取可复用方法论，并持续学习行业最新最佳实践。

## Skill清单

| Skill | 名称 | 描述 |
|-------|------|------|
| `jing-yan-cui-qu` | 个人经验萃取 | 回顾历史工作、归纳工作逻辑、提取可复用方法论 |
| `industry-exp-distill` | 行业经验萃取 | 基于ISIC国际标准行业分类，收集各行业最佳实践 |
| `tech-exp-distill` | 信息技术行业 | 敏捷开发、DevOps、架构设计、技术管理 |
| `finance-exp-distill` | 金融行业 | 风险管理、客户服务、合规管理、数字化转型 |
| `mfg-exp-distill` | 制造业 | 精益生产、质量管理、供应链优化、智能制造 |

## 核心功能

### 1. 个人经验萃取
- 会话记录存储（使用`/memories`目录）
- 工作思路分析方法论
- 经验模板生成
- 方法论提炼框架

### 2. 行业经验收集
- ISIC国际标准行业分类（21个门类）
- 六维度收集框架
- 最佳实践收集与验证
- 跨行业方法论提炼

### 3. 自动更新系统
- 联网检索最新行业动态
- 版本控制与变更追踪
- GitHub自动同步
- 增量更新与备份

## ISIC行业分类覆盖

基于联合国ISIC Rev.4标准，已覆盖以下高价值行业：

| 代码 | 行业 | 优先级 |
|------|------|--------|
| J | 信息和通信 | ⭐⭐⭐⭐⭐ |
| K | 金融和保险 | ⭐⭐⭐⭐⭐ |
| C | 制造业 | ⭐⭐⭐⭐⭐ |
| M | 专业和科技服务 | ⭐⭐⭐⭐ |
| P | 教育 | ⭐⭐⭐⭐ |
| Q | 人体健康 | ⭐⭐⭐⭐ |

## 方法论体系

### 个人层面
- PDCA循环
- 复盘四步法
- 五维分析法
- 经验价值评估

### 行业层面
- 全面质量管理（TQM）
- 敏捷开发（Scrum/SAFe）
- DevOps实践体系
- 精益生产（Lean/TPS）

## 使用方法

### 方式一：在MiniMax Agent中直接调用

```
用户：调用 jing-yan-cui-qu Skill
系统：加载个人经验萃取框架，开始记录和归纳工作
```

### 方式二：使用自动更新系统

每次调用Skill时，系统会自动检查更新状态，并可联网检索最新行业动态。

### 方式三：手动更新

运行更新脚本：
```bash
python _update_system/scripts/update_skills.py
```

## 文件结构

```
exp-distill-skills/
├── jing-yan-cui-qu/              # 个人经验萃取
│   ├── SKILL.md                  # 核心框架文档
│   ├── _meta.json                # 元数据
│   └── references/               # 参考资料
│       └── templates.md          # 模板库
│
├── industry-exp-distill/         # 行业经验元框架
│   ├── SKILL.md                  # ISIC分类+行业总览
│   ├── _meta.json                # 元数据
│   └── references/               # 参考资料
│       └── usage-guide.md        # 使用指南
│
├── tech-exp-distill/             # 信息技术行业
│   ├── SKILL.md                  # 敏捷/DevOps/架构
│   └── _meta.json
│
├── finance-exp-distill/          # 金融行业
│   ├── SKILL.md                  # 风控/服务/合规
│   └── _meta.json
│
├── mfg-exp-distill/              # 制造业
│   ├── SKILL.md                  # 精益/质量/供应链
│   └── _meta.json
│
└── _update_system/               # 自动更新系统
    ├── configs/                  # 配置文件
    ├── scripts/                  # 更新脚本
    ├── logs/                     # 更新日志
    ├── backups/                  # 文件备份
    └── README.md                 # 系统文档
```

## 版本与更新

**当前版本**：1.0.0

**更新机制**：
- 自动更新：每次调用时检查更新
- 手动更新：运行更新脚本
- GitHub同步：自动提交到仓库

**版本规则**：
- Patch：内容修正
- Minor：新增趋势和方法论
- Major：重大框架调整

## 贡献指南

欢迎提交新的行业经验或改进现有内容：

1. Fork本仓库
2. 创建新分支 (`git checkout -b feature/new-industry`)
3. 提交更改 (`git commit -am 'Add new industry experience'`)
4. 推送到分支 (`git push origin feature/new-industry`)
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue。

---

**核心理念**：让每一段工作经历都转化为可复用的智慧资产，让最佳实践成为每个人的能力。