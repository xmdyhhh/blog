const http = require('http');
const fs = require('fs');

function makeRequest(method, path, body, cookies = null) {
    return new Promise((resolve, reject) => {
        const postData = body ? JSON.stringify(body) : null;
        const options = {
            hostname: 'localhost',
            port: 2368,
            path: path,
            method: method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (postData) options.headers['Content-Length'] = Buffer.byteLength(postData);
        if (cookies) options.headers['Cookie'] = cookies;

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                const setCookie = res.headers['set-cookie'];
                let parsedData = null;
                if (data) { try { parsedData = JSON.parse(data); } catch (e) { parsedData = { raw: data }; } }
                resolve({ statusCode: res.statusCode, data: parsedData, cookies: setCookie ? setCookie.map(c => c.split(';')[0]).join('; ') : cookies });
            });
        });
        req.on('error', reject);
        if (postData) req.write(postData);
        req.end();
    });
}

async function main() {
    const login = await makeRequest('POST', '/ghost/api/admin/session/', { username: 'admin@ossblog.local', password: 'Admin@2026Lab!' });
    const cookies = login.cookies;
    console.log('Logged in');

    // Export all posts
    const postsResult = await makeRequest('GET', '/ghost/api/admin/posts/?limit=all&include=tags,authors', null, cookies);
    console.log('Posts exported:', postsResult.data.posts ? postsResult.data.posts.length : 0);

    // Export tags
    const tagsResult = await makeRequest('GET', '/ghost/api/admin/tags/?limit=all', null, cookies);
    console.log('Tags exported:', tagsResult.data.tags ? tagsResult.data.tags.length : 0);

    // Export members
    const membersResult = await makeRequest('GET', '/ghost/api/admin/members/?limit=all', null, cookies);
    console.log('Members exported:', membersResult.data.members ? membersResult.data.members.length : 0);

    // Combine into export file
    const exportData = {
        exportDate: new Date().toISOString(),
        ghostVersion: '6.59.0',
        posts: postsResult.data.posts || [],
        tags: tagsResult.data.tags || [],
        members: membersResult.data.members || []
    };

    const exportPath = 'D:/Desktop/开源软件作业/oss-blog/backups/ghost-content-export.json';
    fs.writeFileSync(exportPath, JSON.stringify(exportData, null, 2));
    console.log('\nContent exported to:', exportPath);
    console.log('Export file size:', (fs.statSync(exportPath).size / 1024).toFixed(2), 'KB');
}

main().catch(console.error);
