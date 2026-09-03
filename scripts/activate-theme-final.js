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
    const login = await makeRequest('POST', '/ghost/api/admin/session/', { username: 'admin@ossblog.local', password: 'Admin@2026Lab!' });
    const cookies = login.cookies;
    console.log('Logged in');

    // List themes
    const themesResult = await makeRequest('GET', '/ghost/api/admin/themes/', null, cookies);
    console.log('\nAvailable themes:');
    themesResult.data.themes.forEach(t => console.log(`  - ${t.name} (active: ${t.active})`));

    // Activate custom theme using the correct endpoint
    console.log('\nActivating oss-blog-theme...');
    const activateResult = await makeRequest('PUT', '/ghost/api/admin/themes/oss-blog-theme/activate', {}, cookies);
    console.log('Status:', activateResult.statusCode);
    
    if (activateResult.statusCode === 200) {
        console.log('Theme activated successfully!');
        const active = activateResult.data.themes.find(t => t.active);
        console.log('Active theme:', active.name);
    } else {
        console.log('Response:', JSON.stringify(activateResult.data, null, 2));
    }
}

main().catch(console.error);
