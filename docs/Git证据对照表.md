# 个人开发过程与 Git 证据对照表

## 开发阶段与 Git 提交对照

| 阶段 | 开发内容 | 对应提交 | 提交哈希 | 提交类型 | 文件数 | 代码行数 |
|------|----------|----------|----------|----------|--------|----------|
| 阶段1：项目初始化 | 创建项目骨架、.gitignore、环境配置、基线文档 | chore: 初始化项目骨架与基线配置 | 900732e | chore | 7 | +4137 |
| 阶段2：主题定制 | 复制 Source 主题、修改导航/卡片/详情页、自定义CSS/JS | feat(theme): 基于 Source 主题开发自定义博客主题 | 8103140 | feat | 88 | +8024 |
| 阶段3：自主功能 | 相关文章推荐、搜索增强、启动脚本、演示数据脚本 | feat(enhancement): 实现相关文章推荐与搜索增强功能 | a94c800 | feat | 7 | +431 |
| 阶段4：测试 | 编写20项验收测试用例 | test: 编写20项验收测试用例并全部通过 | 86e693c | test | 1 | +328 |
| 阶段5：文档 | README、NOTICE、备份恢复文档 | docs: 完善README、NOTICE和备份恢复文档 | e55126a | docs | 3 | +627 |
| 阶段6：PR记录 | PR与Code Review记录文档 | docs: 添加PR与Code Review记录 | e77a7cf | docs | 1 | +160 |
| 阶段7：合并 | 合并 feature 分支到 main | merge: 合并自主扩展功能与测试文档到main | 882cd7b | merge | - | - |

**合计**：6个非合并提交 + 1个合并提交，107个跟踪文件，约13700行新增代码/文档。

---

## 功能需求与 Git 证据对照

| 功能需求 | 实现文件 | 对应提交 | 证据类型 |
|----------|----------|----------|----------|
| 前台可访问 | Ghost 核心 + 主题 | 900732e, 8103140 | 运行截图 01-homepage.png |
| 管理后台可访问 | Ghost 核心 | 900732e | 运行截图 04-admin-dashboard.png |
| 管理员账号 | Ghost 初始化 | 900732e | baseline.md 记录 |
| 会员账号 | create-demo-data.js | a94c800 | 管理后台截图 Members:2 |
| 文章创建/编辑 | Ghost 核心 + 演示脚本 | a94c800 | 运行截图 05-admin-posts.png (9篇) |
| 标签关联 | Ghost 核心 + 演示脚本 | a94c800 | 文章列表截图显示标签 |
| 标签浏览 | tag.hbs (上游) + 自定义样式 | 8103140 | 前台可访问标签页 |
| 评论功能 | Ghost 核心 + enable-features.js | a94c800 | 文章详情页评论区 |
| 搜索功能 | oss-search.js + oss-custom.css | a94c800, 8103140 | 测试用例 TC-007, TC-008 |
| 自定义导航 | navigation.hbs | 8103140 | 前台截图导航栏 |
| 自定义文章卡片 | post-card.hbs + oss-custom.css | 8103140 | 运行截图 02-post-list.png |
| 自定义详情页 | post.hbs | 8103140 | 运行截图 03-post-detail.png |
| 相关文章推荐 | post.hbs (第70-100行) | a94c800 | 测试用例 TC-019 |
| 搜索增强(高亮/建议) | oss-search.js (401行) | a94c800 | 测试用例 TC-020 |
| 响应式布局 | oss-custom.css | 8103140 | 测试用例 TC-014 |
| 键盘可访问 | oss-search.js | a94c800 | 测试用例 TC-015 |
| 重启数据保留 | SQLite 持久化 | 900732e | 测试用例 TC-017 |
| 数据导出/备份 | export-content.js + backups/ | a94c800 | 测试用例 TC-018 |
| README | README.md | e55126a | 文件存在，8666字节 |
| NOTICE | NOTICE.md | e55126a | 文件存在，1488字节 |
| .env.example | .env.example | 900732e | 文件存在 |
| 启动脚本 | 启动博客.bat + start.ps1 | a94c800 | 文件存在 |
| 主题压缩包 | theme/oss-blog-theme.zip | (构建产物) | 327KB |
| Git 分支 | feature/theme-customization, feature/blog-enhancement | git branch | 2个功能分支 |
| Pull Request | docs/pr-review.md | e77a7cf | 2次PR记录 |
| Code Review | docs/pr-review.md | e77a7cf | 2次Review记录 |
| 版本标签 | v1.0-lab | git tag | annotated tag |

---

## 测试用例与 Git 证据对照

| 测试编号 | 测试名称 | 对应功能 | 实现提交 | 测试结果 |
|----------|----------|----------|----------|----------|
| TC-001 | 管理员登录成功 | 认证系统 | 900732e | ✅ 通过 |
| TC-002 | 管理员登录失败 | 认证系统 | 900732e | ✅ 通过 |
| TC-003 | 文章创建与发布 | 内容管理 | a94c800 | ✅ 通过 |
| TC-004 | 文章编辑 | 内容管理 | a94c800 | ✅ 通过 |
| TC-005 | 标签筛选浏览 | 标签系统 | a94c800 | ✅ 通过 |
| TC-006 | 会员评论功能 | 评论系统 | a94c800 | ✅ 通过 |
| TC-007 | 关键词搜索命中 | 搜索增强 | a94c800 | ✅ 通过 |
| TC-008 | 搜索无结果提示 | 搜索增强 | a94c800 | ✅ 通过 |
| TC-009 | 匿名访问公开文章 | 权限控制 | 900732e | ✅ 通过 |
| TC-010 | 匿名无法访问后台 | 权限控制 | 900732e | ✅ 通过 |
| TC-011 | 会员无法访问后台 | 权限控制 | 900732e | ✅ 通过 |
| TC-012 | 评论权限控制 | 权限控制 | a94c800 | ✅ 通过 |
| TC-013 | 桌面端布局正常 | 自定义主题 | 8103140 | ✅ 通过 |
| TC-014 | 移动端响应式布局 | 自定义主题 | 8103140 | ✅ 通过 |
| TC-015 | 键盘可访问性 | 搜索增强 | a94c800 | ✅ 通过 |
| TC-016 | 自定义主题可辨识性 | 自定义主题 | 8103140 | ✅ 通过 |
| TC-017 | 重启后数据保留 | 数据持久化 | 900732e | ✅ 通过 |
| TC-018 | 内容导出与恢复 | 数据备份 | a94c800 | ✅ 通过 |
| TC-019 | 相关文章推荐功能 | 自主功能1 | a94c800 | ✅ 通过 |
| TC-020 | 搜索增强功能 | 自主功能2 | a94c800 | ✅ 通过 |

---

## 个人贡献与上游贡献区分

| 类别 | 上游 Ghost/Source | 本人开发 | 占比 |
|------|-------------------|----------|------|
| 核心功能(认证/内容/会员/评论) | ✅ 全部 | ❌ 未修改 | 上游100% |
| 默认主题基础结构 | ✅ 全部 | ❌ 未修改核心结构 | 上游100% |
| 主题样式(基础) | ✅ screen.css | ❌ 未修改 | 上游100% |
| 主题样式(自定义增强) | ❌ | ✅ oss-custom.css (373行) | 本人100% |
| 导航组件 | ✅ 基础结构 | ✅ 中文化+类名+无障碍 | 上游70% / 本人30% |
| 文章卡片组件 | ✅ 基础结构 | ✅ 阅读时间+中文日期+样式 | 上游60% / 本人40% |
| 相关文章推荐 | ✅ 简单最新文章 | ✅ 标签相似度+回退逻辑 | 上游20% / 本人80% |
| 搜索功能 | ✅ 原生搜索入口 | ✅ 完全重写为增强搜索 | 上游10% / 本人90% |
| 项目文档 | ❌ | ✅ 全部文档 | 本人100% |
| 测试用例 | ❌ | ✅ 20项验收测试 | 本人100% |
| 启动脚本/工具 | ❌ | ✅ 全部脚本 | 本人100% |
| 演示数据 | ❌ | ✅ 9篇文章+4标签+2会员 | 本人100% |

---

## Git 命令证据

### 仓库初始化
```bash
git init
git branch -M main
# 提交哈希: 900732e
```

### 功能分支
```bash
git switch -c feature/theme-customization
# 提交哈希: 8103140

git switch -c feature/blog-enhancement
# 提交哈希: a94c800, 86e693c, e55126a, e77a7cf
```

### 合并
```bash
git switch main
git merge feature/blog-enhancement --no-ff
# 合并提交: 882cd7b
```

### 标签
```bash
git tag -a v1.0-lab -m "实验01完成版本"
# 标签: v1.0-lab (annotated tag)
```

### 完整提交图
```
*   882cd7b (HEAD -> main, tag: v1.0-lab) merge
|\
| * e77a7cf docs: PR与Code Review记录
| * e55126a docs: README/NOTICE/备份恢复
| * 86e693c test: 20项验收测试
| * a94c800 feat(enhancement): 自主扩展功能
| * 8103140 (feature/theme-customization) feat(theme): 自定义主题
|/
* 900732e chore: 项目初始化
```

---

## 验证方法

教师可通过以下命令验证 Git 证据：

```bash
# 查看提交历史
git log --oneline --graph --all --decorate

# 查看每个提交的文件变更
git show --stat 900732e
git show --stat 8103140
git show --stat a94c800
git show --stat 86e693c
git show --stat e55126a
git show --stat e77a7cf

# 查看分支
git branch -a

# 查看标签
git tag -l -n

# 查看具体文件的修改历史
git log --oneline -- theme/oss-blog-theme/post.hbs
git log --oneline -- theme/oss-blog-theme/assets/js/oss-search.js

# 查看差异
git diff 900732e 8103140 --stat
git diff 8103140 a94c800 --stat
```

---

**对照表生成日期**：2026年9月7日
**总提交数**：7个（6个非合并 + 1个合并）
**总文件数**：107个跟踪文件
**版本标签**：v1.0-lab
