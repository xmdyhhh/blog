/* ============================================
   OSS Blog Theme - Search Enhancement
   开源软件实验博客搜索增强功能
   Features: 搜索弹窗、结果高亮、无结果建议、键盘导航
   ============================================ */

(function() {
    'use strict';

    // 配置 - Content API Key 会在主题激活时通过 data 属性注入
    const CONFIG = {
        apiUrl: window.location.origin + '/ghost/api/content/posts/',
        apiKey: document.documentElement.getAttribute('data-content-api-key') || '',
        searchDebounce: 300,
        maxResults: 10
    };

    // 搜索状态
    let searchState = {
        isOpen: false,
        currentQuery: '',
        results: [],
        selectedIndex: -1,
        debounceTimer: null
    };

    // DOM 元素引用
    let elements = {};

    /**
     * 初始化搜索增强功能
     */
    function init() {
        createSearchUI();
        bindEvents();
        console.log('[OSS Search] 搜索增强功能已初始化');
    }

    /**
     * 创建搜索弹窗 UI
     */
    function createSearchUI() {
        // 创建遮罩层
        elements.overlay = document.createElement('div');
        elements.overlay.className = 'oss-search-overlay';
        elements.overlay.setAttribute('role', 'dialog');
        elements.overlay.setAttribute('aria-modal', 'true');
        elements.overlay.setAttribute('aria-label', '搜索文章');

        // 创建弹窗
        elements.modal = document.createElement('div');
        elements.modal.className = 'oss-search-modal';

        // 创建头部
        elements.header = document.createElement('div');
        elements.header.className = 'oss-search-header';

        // 搜索图标
        const searchIcon = document.createElement('span');
        searchIcon.innerHTML = '🔍';
        searchIcon.style.fontSize = '1.2rem';

        // 搜索输入框
        elements.input = document.createElement('input');
        elements.input.type = 'text';
        elements.input.className = 'oss-search-input';
        elements.input.placeholder = '搜索文章标题、内容或标签...';
        elements.input.setAttribute('aria-label', '搜索关键词');
        elements.input.setAttribute('autocomplete', 'off');

        // 关闭按钮
        elements.closeBtn = document.createElement('button');
        elements.closeBtn.className = 'oss-search-close';
        elements.closeBtn.innerHTML = '×';
        elements.closeBtn.setAttribute('aria-label', '关闭搜索');

        elements.header.appendChild(searchIcon);
        elements.header.appendChild(elements.input);
        elements.header.appendChild(elements.closeBtn);

        // 搜索结果区域
        elements.results = document.createElement('div');
        elements.results.className = 'oss-search-results';
        elements.results.setAttribute('role', 'listbox');

        elements.modal.appendChild(elements.header);
        elements.modal.appendChild(elements.results);
        elements.overlay.appendChild(elements.modal);

        document.body.appendChild(elements.overlay);
    }

    /**
     * 绑定事件
     */
    function bindEvents() {
        // 点击搜索按钮打开搜索
        document.querySelectorAll('[data-ghost-search], .gh-search-button, button[aria-label*="搜索"]').forEach(function(btn) {
            btn.addEventListener('click', openSearch);
        });

        // 如果没有找到搜索按钮，监听键盘快捷键 Ctrl+K 或 Cmd+K
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                toggleSearch();
            }
        });

        // 关闭按钮
        elements.closeBtn.addEventListener('click', closeSearch);

        // 点击遮罩层关闭
        elements.overlay.addEventListener('click', function(e) {
            if (e.target === elements.overlay) {
                closeSearch();
            }
        });

        // 搜索输入
        elements.input.addEventListener('input', handleSearchInput);

        // 键盘导航
        elements.input.addEventListener('keydown', handleKeyboardNavigation);

        // ESC 关闭
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && searchState.isOpen) {
                closeSearch();
            }
        });
    }

    /**
     * 打开搜索
     */
    function openSearch() {
        searchState.isOpen = true;
        searchState.selectedIndex = -1;
        elements.overlay.classList.add('active');
        elements.input.value = '';
        elements.results.innerHTML = getInitialHint();
        
        // 延迟聚焦以确保动画完成
        setTimeout(function() {
            elements.input.focus();
        }, 100);

        document.body.style.overflow = 'hidden';
    }

    /**
     * 关闭搜索
     */
    function closeSearch() {
        searchState.isOpen = false;
        elements.overlay.classList.remove('active');
        document.body.style.overflow = '';
        clearTimeout(searchState.debounceTimer);
    }

    /**
     * 切换搜索状态
     */
    function toggleSearch() {
        if (searchState.isOpen) {
            closeSearch();
        } else {
            openSearch();
        }
    }

    /**
     * 处理搜索输入
     */
    function handleSearchInput() {
        const query = elements.input.value.trim();
        searchState.currentQuery = query;

        if (query.length === 0) {
            elements.results.innerHTML = getInitialHint();
            searchState.results = [];
            return;
        }

        if (query.length < 2) {
            elements.results.innerHTML = '<div class="oss-search-loading">请输入至少2个字符...</div>';
            return;
        }

        // 显示加载状态
        elements.results.innerHTML = '<div class="oss-search-loading"><div class="oss-search-spinner"></div><p style="margin-top:12px;">正在搜索...</p></div>';

        // 防抖搜索
        clearTimeout(searchState.debounceTimer);
        searchState.debounceTimer = setTimeout(function() {
            performSearch(query);
        }, CONFIG.searchDebounce);
    }

    /**
     * 执行搜索
     */
    async function performSearch(query) {
        if (!CONFIG.apiKey) {
            elements.results.innerHTML = getNoApiKeyMessage();
            return;
        }

        try {
            // 使用 Ghost Content API 搜索
            const url = CONFIG.apiUrl + 
                '?key=' + encodeURIComponent(CONFIG.apiKey) +
                '&limit=' + CONFIG.maxResults +
                '&include=authors,tags' +
                '&fields=id,title,slug,url,excerpt,custom_excerpt,feature_image' +
                '&filter=' + encodeURIComponent('(title:~' + query + ',excerpt:~' + query + ')');

            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error('API 请求失败: ' + response.status);
            }

            const data = await response.json();
            searchState.results = data.posts || [];
            searchState.selectedIndex = -1;

            if (searchState.results.length === 0) {
                elements.results.innerHTML = getNoResultsHTML(query);
            } else {
                renderResults(searchState.results, query);
            }

        } catch (error) {
            console.error('[OSS Search] 搜索错误:', error);
            elements.results.innerHTML = '<div class="oss-search-no-results"><p>搜索服务暂时不可用，请稍后重试。</p><p style="font-size:0.85rem;color:#bbb;">错误: ' + error.message + '</p></div>';
        }
    }

    /**
     * 渲染搜索结果
     */
    function renderResults(results, query) {
        let html = '<div style="padding:8px 16px;color:#888;font-size:0.85rem;">找到 ' + results.length + ' 篇相关文章</div>';
        
        results.forEach(function(post, index) {
            const title = highlightText(post.title, query);
            const excerpt = highlightText(post.custom_excerpt || post.excerpt || '', query);
            const tagNames = post.tags ? post.tags.map(function(t) { return t.name; }).join(', ') : '';
            
            html += '<a href="' + post.url + '" class="oss-search-result-item" role="option" data-index="' + index + '" tabindex="-1">' +
                '<div class="oss-search-result-title">' + title + '</div>' +
                '<div class="oss-search-result-excerpt">' + excerpt + '</div>' +
                (tagNames ? '<div style="margin-top:6px;font-size:0.8rem;color:#3eb0ef;">#' + tagNames + '</div>' : '') +
                '</a>';
        });

        elements.results.innerHTML = html;

        // 绑定结果项点击
        elements.results.querySelectorAll('.oss-search-result-item').forEach(function(item) {
            item.addEventListener('mouseenter', function() {
                searchState.selectedIndex = parseInt(this.getAttribute('data-index'));
                updateSelection();
            });
        });
    }

    /**
     * 高亮搜索关键词
     */
    function highlightText(text, query) {
        if (!text || !query) return text || '';
        
        // 转义正则特殊字符
        const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp('(' + escapedQuery + ')', 'gi');
        
        return text.replace(regex, '<mark class="oss-search-highlight">$1</mark>');
    }

    /**
     * 处理键盘导航
     */
    function handleKeyboardNavigation(e) {
        const items = elements.results.querySelectorAll('.oss-search-result-item');
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                if (searchState.selectedIndex < items.length - 1) {
                    searchState.selectedIndex++;
                    updateSelection();
                }
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                if (searchState.selectedIndex > 0) {
                    searchState.selectedIndex--;
                    updateSelection();
                }
                break;
                
            case 'Enter':
                e.preventDefault();
                if (searchState.selectedIndex >= 0 && items[searchState.selectedIndex]) {
                    window.location.href = items[searchState.selectedIndex].href;
                } else if (searchState.results.length > 0) {
                    window.location.href = searchState.results[0].url;
                }
                break;
        }
    }

    /**
     * 更新选中状态
     */
    function updateSelection() {
        const items = elements.results.querySelectorAll('.oss-search-result-item');
        items.forEach(function(item, index) {
            if (index === searchState.selectedIndex) {
                item.style.background = '#f0f7ff';
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.style.background = '';
            }
        });
    }

    /**
     * 获取初始提示 HTML
     */
    function getInitialHint() {
        return '<div style="padding:30px;text-align:center;color:#999;">' +
            '<p style="font-size:1.1rem;margin-bottom:8px;">🔍 开始搜索</p>' +
            '<p style="font-size:0.9rem;">输入关键词搜索文章标题和内容</p>' +
            '<p style="font-size:0.8rem;margin-top:16px;color:#bbb;">快捷键: Ctrl/Cmd + K · ESC 关闭</p>' +
            '</div>';
    }

    /**
     * 获取无结果 HTML
     */
    function getNoResultsHTML(query) {
        // 获取热门标签作为建议
        const popularTags = ['开源软件', '技术教程', '实验记录', 'Node.js', 'Ghost', 'Git'];
        const tagSuggestions = popularTags.map(function(tag) {
            return '<span class="oss-search-suggestion-tag" data-tag="' + tag + '">#' + tag + '</span>';
        }).join('');

        return '<div class="oss-search-no-results">' +
            '<div class="oss-search-no-results-icon">📭</div>' +
            '<p style="font-size:1.1rem;font-weight:600;margin-bottom:8px;">未找到相关文章</p>' +
            '<p style="color:#888;margin-bottom:16px;">没有找到与 "<strong>' + escapeHtml(query) + '</strong>" 匹配的内容</p>' +
            '<div class="oss-search-suggestions">' +
            '<p style="margin-bottom:8px;">试试搜索这些热门标签：</p>' +
            tagSuggestions +
            '</div>' +
            '</div>';
    }

    /**
     * 获取无 API Key 提示
     */
    function getNoApiKeyMessage() {
        return '<div class="oss-search-no-results">' +
            '<div class="oss-search-no-results-icon">⚙️</div>' +
            '<p style="font-weight:600;margin-bottom:8px;">搜索功能未配置</p>' +
            '<p style="color:#888;font-size:0.9rem;">请在主题设置中配置 Ghost Content API Key</p>' +
            '<p style="color:#bbb;font-size:0.8rem;margin-top:12px;">管理员可在 Ghost 后台 → 集成 → 添加自定义集成</p>' +
            '</div>';
    }

    /**
     * HTML 转义
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // 绑定标签建议点击事件（事件委托）
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('oss-search-suggestion-tag')) {
            const tag = e.target.getAttribute('data-tag');
            elements.input.value = tag;
            handleSearchInput();
        }
    });

    // DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
