# 经验萃取Skill自动更新系统

> **核心功能**：让Skill具备自动学习、即时更新、GitHub同步能力

---

## 系统概览

```
┌─────────────────────────────────────────────────────────────┐
│                   自动更新系统架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │ Skill加载   │───▶│ 更新检查   │───▶│ 联网检索    │      │
│  │ 触发钩子   │    │  (7天周期)  │    │ 最新动态    │      │
│  └─────────────┘    └─────────────┘    └──────┬──────┘      │
│                                               │             │
│                                               ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │ GitHub同步  │◀───│ 内容更新   │◀───│ 智能分析   │      │
│  │ 版本控制   │    │ 版本递增   │    │ 趋势提炼   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心功能

### 1. 自动更新机制

**触发条件**：

| 触发方式 | 说明 | 自动/手动 |
|----------|------|-----------|
| 加载检查 | 每次加载Skill时检查更新状态 | 自动 |
| 周期检查 | 距离上次更新超过7天 | 自动 |
| 手动触发 | 用户或Agent主动调用更新 | 手动 |

**更新内容**：

- 最新行业趋势和最佳实践
- 新兴方法论和工具
- 案例和参考资料更新
- 版本号递增

### 2. GitHub同步

**功能特性**：

- 自动提交更新内容
- 版本历史追踪
- 变更记录自动生成
- 支持分支管理

**配置要求**：

```json
{
  "github": {
    "repo": "username/skill-repo",
    "token": "ghp_xxxxxxxxxxxx"
  }
}
```

### 3. 版本控制

**版本规则**：

| 更新类型 | 版本递增 | 示例 |
|----------|----------|------|
| 补丁更新 | patch | 1.0.0 → 1.0.1 |
| 功能更新 | minor | 1.0.0 → 1.1.0 |
| 重大更新 | major | 1.0.0 → 2.0.0 |

**变更日志**：

每次更新自动追加变更记录到SKILL.md文件末尾。

---

## 使用方法

### 方法一：自动更新（推荐）

当您调用任何经验萃取Skill时，系统会自动检查更新状态：

```
用户：调用 tech-exp-distill
系统：检查更新 → 发现新版本 → 自动检索最新动态 → 更新内容
```

### 方法二：手动触发更新

在需要时手动触发更新：

```python
# 调用手动更新接口
skill_manual_update("tech-exp-distill", search_results)
```

### 方法三：批量同步

将所有Skill同步到GitHub：

```python
# 同步所有更新到GitHub
sync_all_skills_to_github()
```

---

## 配置说明

### 配置文件位置

```
/workspace/.minimax/skills/_update_system/configs/update_config.json
```

### 关键配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `update_interval_days` | 更新检查间隔 | 7天 |
| `max_trends_per_skill` | 每Skill最多趋势数 | 5条 |
| `backup_before_update` | 更新前备份 | true |
| `auto_sync_to_github` | 自动同步到GitHub | false |

### GitHub配置

```json
{
  "github": {
    "repo": "your-username/your-repo",
    "token": "ghp_your_personal_access_token"
  }
}
```

**获取GitHub Token**：

1. 登录GitHub → Settings → Developer settings
2. Personal access tokens → Generate new token
3. 勾选 `repo` 权限
4. 复制生成的token到配置中

---

## 文件结构

```
/workspace/.minimax/skills/
├── _update_system/
│   ├── configs/
│   │   └── update_config.json      # 更新配置
│   ├── scripts/
│   │   └── update_skills.py        # 更新脚本
│   ├── logs/                       # 更新日志
│   │   └── update_202401.log
│   └── backups/                    # 备份文件
│       └── SKILL_20240115_143000.md
│
├── jing-yan-cui-qu/               # 个人经验萃取
│   ├── SKILL.md
│   └── _meta.json
│
├── industry-exp-distill/           # 行业经验元框架
│   ├── SKILL.md
│   └── _meta.json
│
├── tech-exp-distill/               # 科技行业
│   ├── SKILL.md
│   └── _meta.json
│
├── finance-exp-distill/            # 金融行业
│   ├── SKILL.md
│   └── _meta.json
│
└── mfg-exp-distill/               # 制造业
    ├── SKILL.md
    └── _meta.json
```

---

## 更新日志格式

每次更新会在SKILL.md末尾追加以下格式的日志：

```markdown
### 最新行业动态

**1. [趋势标题]**
- 来源: [来源网站]
- 摘要: [内容摘要]...
- 链接: [链接地址]

---

**更新日志**:
- **2024-01-15** [auto-update]: 自动更新行业动态，发现 5 条新趋势
- **2024-01-10** [minor]: 新增DevOps实践案例
- **2024-01-01** [major]: 初始版本发布
```

---

## 故障排除

### 问题1：GitHub连接失败

**症状**：更新成功但同步GitHub失败

**解决方案**：

1. 检查 `update_config.json` 中的token是否正确
2. 确认token有repo权限
3. 确认repo名称格式正确（username/repo）

### 问题2：更新间隔过短

**症状**：频繁触发更新

**解决方案**：修改配置中 `update_interval_days` 为更大值（如14或30）

### 问题3：备份占用空间

**症状**：backups目录过大

**解决方案**：

1. 手动清理旧备份
2. 设置 `keep_last_n_backups` 自动保留数量

---

## API接口

### skill_on_load_hook(skill_id)

Skill加载时的钩子函数，检查更新状态。

**返回**：

```json
{
  "skill_id": "tech-exp-distill",
  "needs_update": true,
  "version": "1.0.0",
  "last_update": "2024-01-08T10:00:00",
  "message": "发现新版本可用"
}
```

### skill_manual_update(skill_id, search_results)

手动触发更新。

**参数**：

- `skill_id`: Skill标识符
- `search_results`: 搜索结果列表

**返回**：更新是否成功

### sync_all_skills_to_github()

同步所有Skill到GitHub。

**返回**：同步结果统计

---

## 安全建议

1. **Token安全**：不要将GitHub token提交到公开仓库
2. **备份意识**：重要更新前会创建本地备份
3. **版本控制**：所有变更都有版本记录，可回滚

---

## 扩展开发

### 添加新的Skill到更新系统

1. 在 `update_config.json` 的 `search_config` 中添加配置
2. 同步到 `INDUSTRY_KEYWORDS` 字典
3. 创建对应的SKILL.md文件

### 自定义更新源

修改 `update_config.json` 中的 `sources` 列表，添加行业特定的信息源。

---

## 版本信息

**当前版本**：1.0.0

**最后更新**：2024年1月

**维护者**：MiniMax Agent

---

**核心理念**：让Skill像生物一样具备学习和进化的能力，持续为用户提供最新、最有价值的行业智慧。