# MAXCLAW技能库上传指南

## 概述

本文档说明如何将经验萃取Skill上传到MAXCLAW技能库。

## Skill清单

本次创建的经验萃取Skill包括：

| Skill ID | 名称 | 描述 | 路径 |
|----------|------|------|------|
| `jing-yan-cui-qu` | 个人经验萃取 | 回顾工作、归纳逻辑、提取方法论 | `/workspace/.minimax/skills/jing-yan-cui-qu/` |
| `industry-exp-distill` | 行业经验萃取 | ISIC标准分类、行业最佳实践 | `/workspace/.minimax/skills/industry-exp-distill/` |
| `tech-exp-distill` | 信息技术行业 | 敏捷开发、DevOps、架构设计 | `/workspace/.minimax/skills/tech-exp-distill/` |
| `finance-exp-distill` | 金融行业 | 风险管理、客户服务、数字化 | `/workspace/.minimax/skills/finance-exp-distill/` |
| `mfg-exp-distill` | 制造业 | 精益生产、质量管理、供应链 | `/workspace/.minimax/skills/mfg-exp-distill/` |
| `_update_system` | 自动更新系统 | 联网检索、版本控制、GitHub同步 | `/workspace/.minimax/skills/_update_system/` |

## 上传前提条件

1. **MAXCLAW API Key**: 需要提供有效的API访问密钥
2. **MAXCLAW API URL**: API端点地址（可选，使用默认）

## Skill结构

每个Skill包含以下文件：

```
skill-name/
├── SKILL.md              # 核心框架文档（必需）
├── _meta.json            # 元数据（必需）
├── references/           # 参考资料（可选）
│   └── *.md
├── industry/            # 行业资料（可选）
│   └── */
└── configs/             # 配置文件（可选）
    └── *.json
```

## _meta.json格式

```json
{
  "id": <unique_id>,
  "name": "skill-name",
  "platform": "minimax",
  "updated_at": <timestamp>,
  "version": "1.0.0"
}
```

## 上传步骤

### 1. 获取API凭证

如果还没有MAXCLAW API Key，请联系管理员获取。

### 2. 调用上传接口

使用以下API端点上传Skill：

```
POST /api/skills/upload
Headers:
  - Authorization: Bearer <API_KEY>
  - Content-Type: multipart/form-data

Body:
  - skill_id: <skill-name>
  - skill_file: <SKILL.md file>
  - meta_file: <_meta.json file>
  - category: <行业分类>
```

### 3. 验证上传

上传成功后，可以使用以下API验证：

```
GET /api/skills/{skill_id}
```

## 批量上传

如需批量上传多个Skill，请逐个上传或使用批量接口。

## 常见问题

### Q: 上传失败怎么办？
A: 检查以下内容：
1. API Key是否有效
2. 文件格式是否正确
3. SKILL.md是否包含必需内容

### Q: 如何更新已上传的Skill？
A: 重新上传同名Skill，系统会自动更新版本号。

---

**生成时间**: 2024-01
**版本**: 1.0.0