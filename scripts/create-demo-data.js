// Ghost Demo Data Creation Script
const https = require('http');

const BASE_URL = 'http://localhost:2368';
const ADMIN_EMAIL = 'admin@ossblog.local';
const ADMIN_PASSWORD = 'Admin@2026Lab!';

function makeRequest(method, path, body, cookies = null) {
    return new Promise((resolve, reject) => {
        const postData = body ? JSON.stringify(body) : null;
        const options = {
            hostname: 'localhost',
            port: 2368,
            path: path,
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        if (postData) {
            options.headers['Content-Length'] = Buffer.byteLength(postData);
        }
        if (cookies) {
            options.headers['Cookie'] = cookies;
        }

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                const setCookie = res.headers['set-cookie'];
                let parsedData = null;
                if (data) {
                    try {
                        parsedData = JSON.parse(data);
                    } catch (e) {
                        parsedData = { raw: data };
                    }
                }
                resolve({
                    statusCode: res.statusCode,
                    data: parsedData,
                    cookies: setCookie ? setCookie.map(c => c.split(';')[0]).join('; ') : cookies
                });
            });
        });

        req.on('error', reject);
        if (postData) req.write(postData);
        req.end();
    });
}

async function main() {
    console.log('=== Ghost Demo Data Creation ===\n');

    // 1. Login
    console.log('1. Logging in as admin...');
    const loginResult = await makeRequest('POST', '/ghost/api/admin/session/', {
        username: ADMIN_EMAIL,
        password: ADMIN_PASSWORD
    });
    console.log(`   Login status: ${loginResult.statusCode}`);
    const sessionCookies = loginResult.cookies;

    // 2. Create integration
    console.log('\n2. Creating API integration...');
    const intResult = await makeRequest('POST', '/ghost/api/admin/integrations/', {
        integrations: [{
            name: 'OSS Blog Lab Integration',
            description: 'Integration for open source software lab'
        }]
    }, sessionCookies);
    const integration = intResult.data.integrations[0];
    const contentApiKey = integration.api_keys[0].secret;
    const adminApiKey = integration.api_keys[1].secret;
    console.log(`   Integration created. Content Key: ${contentApiKey}`);
    
    // Save API keys
    const fs = require('fs');
    fs.writeFileSync('D:/Desktop/开源软件作业/oss-blog/scripts/api-keys.json', JSON.stringify({
        contentApiKey,
        adminApiKey,
        integrationId: integration.id
    }, null, 2));

    // 3. Create tags
    console.log('\n3. Creating tags...');
    const tags = [
        { name: '开源软件', slug: 'open-source', description: '开源软件相关文章' },
        { name: '技术教程', slug: 'tutorial', description: '技术教程和指南' },
        { name: '实验记录', slug: 'lab-notes', description: '课程实验记录' }
    ];
    for (const tag of tags) {
        const result = await makeRequest('POST', '/ghost/api/admin/tags/', { tags: [tag] }, sessionCookies);
        console.log(`   Tag created: ${result.data.tags[0].name}`);
    }

    // 4. Create members
    console.log('\n4. Creating members...');
    const members = [
        { name: '张三', email: 'zhangsan@example.com', note: '演示会员账号1' },
        { name: '李四', email: 'lisi@example.com', note: '演示会员账号2' }
    ];
    for (const member of members) {
        const result = await makeRequest('POST', '/ghost/api/admin/members/', { members: [member] }, sessionCookies);
        console.log(`   Member created: ${result.data.members[0].name} (${result.data.members[0].email})`);
    }

    // 5. Create posts
    console.log('\n5. Creating posts...');
    const posts = [
        {
            title: 'Ghost 开源博客系统入门指南',
            slug: 'ghost-getting-started',
            status: 'published',
            tags: [{ name: '开源软件' }, { name: '技术教程' }],
            html: `<h2>什么是 Ghost？</h2><p>Ghost 是一个强大的开源博客平台，使用 Node.js 构建，专为内容创作者设计。它提供了丰富的编辑器、会员系统、评论功能和主题机制。</p><h2>为什么选择 Ghost？</h2><ul><li>开源免费，MIT 许可证</li><li>现代化的编辑器体验</li><li>内置会员和订阅功能</li><li>强大的主题定制能力</li><li>丰富的 API 接口</li></ul><h2>快速开始</h2><p>使用 Ghost CLI 可以快速在本地搭建 Ghost 实例：</p><pre><code>npm install -g ghost-cli@latest
mkdir my-blog && cd my-blog
ghost install local</code></pre><p>安装完成后，访问 http://localhost:2368/ghost 完成初始化设置。</p>`
        },
        {
            title: '开源软件许可证详解：MIT、Apache、GPL 的区别',
            slug: 'open-source-licenses-explained',
            status: 'published',
            tags: [{ name: '开源软件' }],
            html: `<h2>为什么许可证很重要？</h2><p>开源软件许可证决定了他人可以如何使用、修改和分发你的代码。选择合适的许可证是开源项目的重要决策。</p><h2>MIT 许可证</h2><p>MIT 是最宽松的开源许可证之一。它允许他人自由使用、修改、合并、发布、分发、再授权和销售软件副本，只需保留版权声明和许可声明。</p><h2>Apache 2.0 许可证</h2><p>Apache 2.0 与 MIT 类似，但额外提供了专利授权和商标保护。它要求声明修改内容，并保留 NOTICE 文件。</p><h2>GPL 许可证</h2><p>GPL（GNU General Public License）是一种 copyleft 许可证，要求基于 GPL 代码的衍生作品也必须以 GPL 开源。这确保了代码的持续开放性。</p><h2>如何选择？</h2><ul><li>想要最大程度的自由传播：MIT</li><li>需要专利保护：Apache 2.0</li><li>希望衍生作品保持开源：GPL</li></ul>`
        },
        {
            title: 'Node.js 项目最佳实践：从结构到部署',
            slug: 'nodejs-best-practices',
            status: 'published',
            tags: [{ name: '技术教程' }],
            html: `<h2>项目结构</h2><p>一个良好的 Node.js 项目结构应该清晰分离关注点。推荐使用以下结构：</p><pre><code>project/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── tests/
├── config/
├── docs/
└── package.json</code></pre><h2>依赖管理</h2><p>使用 package-lock.json 或 pnpm-lock.yaml 锁定依赖版本，确保团队成员和部署环境使用相同的依赖版本。</p><h2>错误处理</h2><p>使用统一的错误处理中间件，避免在每个路由中重复错误处理逻辑。自定义错误类可以提供更丰富的错误信息。</p><h2>安全实践</h2><ul><li>永远不要将密码、密钥提交到版本控制</li><li>使用环境变量管理敏感配置</li><li>对用户输入进行验证和清理</li><li>使用 helmet 等中间件设置安全头</li></ul><h2>测试</h2><p>编写单元测试和集成测试，使用 Jest 或 Mocha 等测试框架。设置 CI/CD 流水线，在每次提交时自动运行测试。</p>`
        },
        {
            title: '实验记录：开源个人博客系统二次开发',
            slug: 'lab-blog-customization',
            status: 'published',
            tags: [{ name: '实验记录' }, { name: '开源软件' }],
            html: `<h2>实验目标</h2><p>本次实验的目标是基于 Ghost 开源博客系统进行二次开发，完成一个可注册、可写作、可评论、可搜索的个人博客系统。</p><h2>技术选型</h2><p>我们选择 Ghost 作为基线项目，原因如下：</p><ul><li>Ghost 具备成熟的编辑器、标签、会员和评论机制</li><li>使用 Node.js 开发，与课程技术栈一致</li><li>主题定制能力强，适合二次开发</li><li>MIT 许可证，允许自由修改和分发</li></ul><h2>开发环境</h2><ul><li>操作系统：Windows 11</li><li>Node.js：22.23.1 LTS</li><li>Ghost CLI：1.32.3</li><li>Ghost：6.59.0</li><li>数据库：SQLite（本地开发）</li></ul><h2>二次开发内容</h2><h3>1. 自定义主题</h3><p>基于 Ghost 默认主题进行修改，包括自定义导航栏、文章列表卡片样式、文章详情页元数据展示和响应式布局优化。</p><h3>2. 自主扩展功能</h3><p>实现相关文章推荐功能，基于标签相似度为读者推荐相关内容。</p><h3>3. 搜索增强</h3><p>在 Ghost 原生搜索基础上，增加搜索结果高亮和无结果提示。</p><h2>遇到的问题</h2><p>在开发过程中，我们遇到了 Node.js 版本兼容性问题。Ghost 6.x 要求 Node.js 22 LTS，而系统默认安装的是 Node.js 24。解决方案是下载 Node.js 22 便携版，并在运行 Ghost 时指定使用该版本。</p>`
        },
        {
            title: 'Git 版本管理实战：从分支到 Pull Request',
            slug: 'git-version-control-practice',
            status: 'published',
            tags: [{ name: '技术教程' }, { name: '实验记录' }],
            html: `<h2>为什么需要版本控制？</h2><p>版本控制是软件开发的基础实践。它允许我们追踪代码变更、协作开发、回滚错误修改，并维护多个开发分支。</p><h2>基本工作流</h2><h3>1. 初始化仓库</h3><pre><code>git init
git add .
git commit -m "Initial commit"</code></pre><h3>2. 创建功能分支</h3><pre><code>git switch -c feature/my-feature</code></pre><h3>3. 提交变更</h3><pre><code>git add modified-file.js
git commit -m "feat: add my feature"</code></pre><h3>4. 推送并创建 PR</h3><pre><code>git push -u origin feature/my-feature</code></pre><h2>提交信息规范</h2><p>使用 Conventional Commits 规范：feat 新功能、fix 修复 bug、docs 文档更新、style 代码格式、refactor 重构、test 测试相关、chore 构建工具相关。</p><h2>Code Review 清单</h2><ul><li>代码是否符合项目规范？</li><li>是否有足够的测试覆盖？</li><li>是否有安全隐患？</li><li>命名是否清晰？</li><li>是否有重复代码？</li><li>错误处理是否完善？</li></ul><h2>实验中的 Git 实践</h2><p>在本次博客系统二次开发实验中，我们使用 main 主分支保持稳定，feature/theme-customization 主题定制分支，feature/blog-enhancement 自主功能开发分支。每个功能分支开发完成后，创建 Pull Request 并进行自我 Code Review，然后合并到 main 分支。</p>`
        },
        {
            title: 'SQLite 数据库入门：轻量级数据存储方案',
            slug: 'sqlite-getting-started',
            status: 'published',
            tags: [{ name: '技术教程' }],
            html: `<h2>什么是 SQLite？</h2><p>SQLite 是一个轻量级的关系型数据库管理系统，它以单个文件的形式存储数据，不需要独立的服务器进程。这使得它非常适合嵌入式设备、移动应用和小型 Web 应用。</p><h2>SQLite 的优势</h2><ul><li>零配置：无需安装和配置数据库服务器</li><li>单文件：整个数据库存储在一个文件中，便于备份和迁移</li><li>跨平台：支持所有主流操作系统</li><li>ACID 兼容：支持事务，保证数据一致性</li><li>标准 SQL：支持大部分 SQL92 标准</li></ul><h2>基本操作</h2><h3>创建数据库和表</h3><pre><code>sqlite3 mydatabase.db
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);</code></pre><h3>插入和查询数据</h3><pre><code>INSERT INTO users (name, email) VALUES ('张三', 'zhangsan@example.com');
SELECT * FROM users WHERE name LIKE '张%';
UPDATE users SET email = 'new@example.com' WHERE id = 1;
DELETE FROM users WHERE id = 1;</code></pre><h2>在 Node.js 中使用 SQLite</h2><p>使用 better-sqlite3 库可以在 Node.js 中高效地操作 SQLite 数据库。在本地开发环境中，Ghost 默认使用 SQLite 存储数据。数据库文件位于 content/data/ghost-local.db。</p>`
        },
        {
            title: 'Handlebars 模板引擎教程：构建动态网页',
            slug: 'handlebars-template-tutorial',
            status: 'published',
            tags: [{ name: '技术教程' }, { name: '开源软件' }],
            html: `<h2>什么是 Handlebars？</h2><p>Handlebars 是一个简单的模板引擎，它使用模板和输入数据生成 HTML 页面。它是 Mustache 的超集，添加了一些额外的功能，如助手函数和块表达式。</p><h2>基本语法</h2><h3>变量输出</h3><p>使用双大括号输出变量内容。</p><h3>条件判断</h3><p>使用 if/else 块进行条件渲染。</p><h3>循环遍历</h3><p>使用 each 块遍历数组或集合。</p><h2>Ghost 主题中的 Handlebars</h2><p>Ghost 主题使用 Handlebars 作为模板引擎。主题文件位于 content/themes/ 目录下，主要文件包括 default.hbs 主布局模板、index.hbs 首页模板、post.hbs 文章详情模板、tag.hbs 标签页模板、author.hbs 作者页模板和 partials/ 可复用组件模板。</p><h2>常用 Ghost 助手</h2><ul><li>get：获取内容数据</li><li>foreach：遍历内容集合</li><li>img_url：生成图片 URL</li><li>asset：引用主题资源</li><li>body_class：生成 body CSS 类</li><li>pagination：生成分页</li></ul><h2>自定义助手</h2><p>在 Ghost 主题中，可以通过 app.js 注册自定义助手函数，扩展模板的功能。这是二次开发的重要手段。</p>`
        },
        {
            title: '实验总结：开源软件二次开发的经验与反思',
            slug: 'lab-summary-and-reflection',
            status: 'published',
            tags: [{ name: '实验记录' }],
            html: `<h2>实验完成情况</h2><p>本次实验成功完成了基于 Ghost 的开源个人博客系统二次开发。系统具备用户注册和登录、文章创建编辑和发布、标签分类和浏览、会员评论系统、关键词搜索功能、自定义主题和相关文章推荐等功能。</p><h2>学到的知识</h2><h3>1. 开源项目评估</h3><p>学会了如何评估开源项目的适用性，包括查看许可证、社区活跃度、文档质量和技术栈匹配度。</p><h3>2. 源码阅读能力</h3><p>通过阅读 Ghost 的主题代码和 API 文档，提升了理解大型开源项目结构的能力。</p><h3>3. 二次开发实践</h3><p>掌握了在不修改核心代码的前提下，通过主题和 API 进行二次开发的方法。这种方式保证了上游项目的可升级性。</p><h3>4. 版本管理规范</h3><p>实践了使用 Feature Branch、Pull Request 和 Code Review 的开发流程，养成了规范的提交习惯。</p><h2>遇到的挑战</h2><h3>1. 环境配置</h3><p>Node.js 版本兼容性是第一个挑战。通过使用便携版 Node.js 22 解决了这个问题，这也让我认识到锁定开发环境版本的重要性。</p><h3>2. 主题开发</h3><p>Ghost 主题使用 Handlebars 模板引擎，需要学习其特定的助手函数和数据结构。通过阅读官方文档和默认主题源码，逐步掌握了主题开发方法。</p><h3>3. API 集成</h3><p>在实现自主扩展功能时，需要使用 Ghost Content API 获取相关文章。需要注意 API 密钥的安全使用，不能将 Admin API Key 暴露到前端。</p><h2>改进方向</h2><ul><li>增加更多的自主扩展功能，如文章收藏、阅读统计等</li><li>优化主题的无障碍访问性</li><li>增加自动化测试覆盖</li><li>尝试使用 MySQL 替代 SQLite，模拟生产环境</li><li>学习 Ghost 核心代码，深入理解其架构设计</li></ul><h2>结语</h2><p>通过本次实验，我深刻体会到了开源软件的力量。站在成熟开源项目的肩膀上，可以快速构建功能完善的应用，同时通过二次开发学习优秀的代码设计和工程实践。这为今后参与更大规模的开源项目打下了基础。</p>`
        }
    ];

    for (const post of posts) {
        const result = await makeRequest('POST', '/ghost/api/admin/posts/?source=html', { posts: [post] }, sessionCookies);
        if (result.statusCode === 201) {
            console.log(`   Post created: ${result.data.posts[0].title}`);
        } else {
            console.log(`   Failed to create post: ${post.title}, status: ${result.statusCode}`);
            console.log(`   Response: ${JSON.stringify(result.data)}`);
        }
    }

    console.log('\n=== All demo data created successfully ===');
    console.log(`Tags: ${tags.length}`);
    console.log(`Members: ${members.length}`);
    console.log(`Posts: ${posts.length}`);
}

main().catch(console.error);
