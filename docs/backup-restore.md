# 数据备份与恢复说明

## 备份文件清单

| 文件名 | 类型 | 大小 | 说明 |
|--------|------|------|------|
| ghost-local-backup-YYYYMMDD-HHMMSS.db | SQLite 数据库 | ~1.5MB | 完整数据库备份，包含所有文章、标签、会员、评论、设置 |
| ghost-content-export.json | JSON 导出 | ~109KB | 内容导出文件，包含文章、标签、会员数据，便于跨环境迁移 |

## 备份方法

### 方法一：SQLite 数据库文件备份（推荐）

1. 停止 Ghost 实例（确保数据一致性）：
   ```bash
   cd runtime
   ghost stop
   ```

2. 复制数据库文件：
   ```bash
   cp runtime/content/data/ghost-local.db backups/ghost-local-backup-$(date +%Y%m%d-%H%M%S).db
   ```

3. 重启 Ghost：
   ```bash
   ghost start --development
   ```

### 方法二：管理后台内容导出

1. 登录 Ghost 管理后台 http://localhost:2368/ghost
2. 进入 设置 → 高级 → 实验室 → 导出内容
3. 点击"导出"按钮，下载 JSON 文件
4. 将下载的文件保存到 backups/ 目录

### 方法三：API 自动化导出

运行项目提供的导出脚本：
```bash
node scripts/export-content.js
```

## 恢复方法

### 方法一：SQLite 数据库文件恢复

1. 停止 Ghost 实例：
   ```bash
   cd runtime
   ghost stop
   ```

2. 备份当前数据库（防止恢复失败）：
   ```bash
   cp content/data/ghost-local.db content/data/ghost-local.db.bak
   ```

3. 用备份文件替换当前数据库：
   ```bash
   cp ../../backups/ghost-local-backup-YYYYMMDD-HHMMSS.db content/data/ghost-local.db
   ```

4. 重启 Ghost：
   ```bash
   ghost start --development
   ```

5. 验证数据：
   - 访问 http://localhost:2368 检查文章是否正常显示
   - 登录管理后台检查文章、标签、会员数量

### 方法二：管理后台内容导入

1. 登录 Ghost 管理后台
2. 进入 设置 → 高级 → 实验室 → 导入内容
3. 选择 JSON 导出文件
4. 点击"导入"按钮
5. 等待导入完成，检查数据完整性

## 数据验证清单

恢复完成后，请验证以下数据：

- [ ] 文章数量正确（当前：9篇）
- [ ] 标签数量正确（当前：4个）
- [ ] 会员账号存在（当前：2个）
- [ ] 文章内容完整（标题、正文、标签关联）
- [ ] 评论数据保留
- [ ] 站点设置正确（标题、描述、主题）
- [ ] 自定义主题正常激活

## 注意事项

1. **数据库一致性**：进行数据库文件备份前，建议先停止 Ghost 实例，确保所有数据已写入磁盘。

2. **版本兼容性**：SQLite 数据库文件在不同 Ghost 版本之间可能不兼容。恢复时请确保 Ghost 版本一致（当前：v6.59.0）。

3. **敏感信息**：数据库文件包含管理员密码哈希和会员信息，请勿提交到公开 Git 仓库或分享给无关人员。

4. **定期备份**：建议在重要操作前（如主题修改、数据导入）进行备份，并定期（如每周）进行完整备份。

5. **存储位置**：备份文件存储在项目根目录的 backups/ 文件夹中，该目录已在 .gitignore 中排除，不会提交到版本控制。

## 自动化备份脚本

项目提供了自动化备份脚本 `scripts/backup.ps1`（Windows）或可自行创建 shell 脚本：

```powershell
# Windows PowerShell 备份脚本示例
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$source = "runtime\content\data\ghost-local.db"
$dest = "backups\ghost-local-backup-$timestamp.db"
Copy-Item $source $dest
Write-Output "Backup created: $dest"
```
