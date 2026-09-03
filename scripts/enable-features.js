const http = require('http');

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
    // Login
    const login = await makeRequest('POST', '/ghost/api/admin/session/', { username: 'admin@ossblog.local', password: 'Admin@2026Lab!' });
    const cookies = login.cookies;
    console.log('Logged in');

    // Get current settings
    const settingsResult = await makeRequest('GET', '/ghost/api/admin/settings/', null, cookies);
    console.log('Current settings fetched');

    // Update settings to enable members and comments
    const updates = {
        settings: [
            { key: 'members_signup_access', value: 'all' },
            { key: 'comments_enabled', value: 'all' },
            { key: 'title', value: '开源软件实验博客' },
            { key: 'description', value: '基于 Ghost 的开源个人博客系统二次开发实验' }
        ]
    };
    const updateResult = await makeRequest('PUT', '/ghost/api/admin/settings/', updates, cookies);
    console.log('Settings updated:', updateResult.statusCode);

    // List themes
    const themesResult = await makeRequest('GET', '/ghost/api/admin/themes/', null, cookies);
    if (themesResult.data && themesResult.data.themes) {
        console.log('\nInstalled themes:');
        themesResult.data.themes.forEach(t => console.log(`  - ${t.name} (active: ${t.active})`));
    }
}

main().catch(console.error);
