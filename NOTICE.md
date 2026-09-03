# 第三方资源与许可证声明 (NOTICE)

本项目基于以下开源项目和资源进行二次开发，特此声明并保留原始许可证。

## 上游项目

### Ghost
- **项目名称**: Ghost
- **仓库地址**: https://github.com/TryGhost/Ghost
- **版本**: v6.59.0
- **许可证**: MIT License
- **用途**: 作为博客系统的核心运行平台，提供认证、内容管理、会员、评论等基础功能
- **修改范围**: 未修改 Ghost 核心代码，所有二次开发在主题层完成

### Ghost Source Theme
- **项目名称**: Source (Ghost 默认主题)
- **仓库地址**: https://github.com/TryGhost/Source
- **版本**: 1.7.2
- **许可证**: MIT License
- **用途**: 作为自定义主题的基础模板
- **修改范围**: 
  - 修改导航栏组件 (partials/components/navigation.hbs)
  - 修改文章卡片组件 (partials/post-card.hbs)
  - 修改文章详情页 (post.hbs)，增强相关文章推荐
  - 修改主布局 (default.hbs)，添加自定义 CSS/JS 引用
  - 新增自定义样式文件 (assets/css/oss-custom.css)
  - 新增搜索增强脚本 (assets/js/oss-search.js)
  - 修改 package.json 主题名称和版本

## 开发工具与依赖

### Node.js
- **版本**: v22.23.1 LTS
- **许可证**: MIT License
- **用途**: Ghost 运行环境

### Ghost CLI
- **版本**: 1.32.3
- **许可证**: MIT License
- **用途**: Ghost 本地安装和进程管理

### 其他 npm 依赖
所有 npm 依赖的许可证信息可在各包的 package.json 或 LICENSE 文件中查看。项目使用 pnpm 进行包管理，依赖锁定文件为 pnpm-lock.yaml。

## 字体资源

主题使用以下字体（通过 Google Fonts CDN 加载，未包含在项目文件中）：
- Inter (sans-serif) - SIL Open Font License
- EB Garamond (serif) - SIL Open Font License
- JetBrains Mono (monospace) - SIL Open Font License

## 图片资源

本项目未包含第三方图片资源。演示文章使用纯文本内容，未使用封面图片。Ghost 默认封面图片来自 Ghost 官方 CDN (static.ghost.org)。

## 本项目新增代码许可证

本项目新增的自定义主题代码、脚本和文档采用 **MIT License**，与上游项目保持兼容。

## 致谢

感谢 Ghost Foundation 和开源社区提供的优秀开源项目，使本实验得以在成熟平台基础上进行二次开发学习。

---

**声明日期**: 2026-09-03
**项目作者**: 学生本人（软件工程专业）
**课程**: 《开源软件与新技术》实验01
