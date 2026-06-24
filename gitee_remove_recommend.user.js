// ==UserScript==
// @name         Gitee移除多余推荐菜单
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  移除 Gitee 工作台的“推荐关注”、“推荐仓库”板块，以及“智能客服”浮标、“模力方舟”和“AI队友”导航菜单，并禁用 favicon 动态红点提醒
// @author       SodaCris
// @match        https://gitee.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gitee.com
// @license      MIT
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    const DEFAULT_FAVICON = 'https://gitee.com/favicon.ico';

    // 1. 注入 CSS 隐藏样式以避免界面闪烁 (Flicker)
    const style = document.createElement('style');
    style.textContent = '.gitee-cleanup-hidden { display: none !important; }';
    document.documentElement.appendChild(style);

    // 锁定 Favicon 为默认图标，阻止动态红点提醒
    function lockFavicon() {
        const favicon = document.querySelector('link[rel*="icon"]');
        if (favicon) {
            if (favicon.getAttribute('href') !== DEFAULT_FAVICON) {
                favicon.setAttribute('href', DEFAULT_FAVICON);
            }
        } else {
            // 如果 favicon 标签不存在，重新生成一个默认的
            if (document.head) {
                const link = document.createElement('link');
                link.rel = 'shortcut icon';
                link.href = DEFAULT_FAVICON;
                document.head.appendChild(link);
            }
        }

        // 清理任何多余的 favicon 标签
        const allFavicons = document.querySelectorAll('link[rel*="icon"]');
        if (allFavicons.length > 1) {
            for (let i = 1; i < allFavicons.length; i++) {
                allFavicons[i].remove();
            }
        }
    }

    function cleanGiteeUI() {
        // 1. 扫描 span 和 a 标签以匹配并移除菜单项：“模力方舟” & “AI队友 / AI 队友”
        const menuElements = document.querySelectorAll('span, a');
        for (const el of menuElements) {
            const textNormalized = el.textContent.trim().replace(/\s+/g, '');

            if (textNormalized === '模力方舟' || textNormalized === 'AI队友') {
                const li = el.closest('li');
                if (li) {
                    li.classList.add('gitee-cleanup-hidden');
                } else {
                    el.classList.add('gitee-cleanup-hidden'); // 如果没有包裹在 li 中，直接隐藏自身
                }
            }
        }

        // 2. 扫描 span 移除“推荐关注”
        const spans = document.querySelectorAll('span');
        for (const span of spans) {
            const textNormalized = span.textContent.trim().replace(/\s+/g, '');
            if (textNormalized === '推荐关注') {
                const container = span.closest('.mb-4');
                if (container) {
                    container.classList.add('gitee-cleanup-hidden');
                }
            }
        }

        // 3. 移除“推荐仓库”及其关联列表 (解决异步加载不同步问题)
        const strongs = document.querySelectorAll('strong');
        for (const strong of strongs) {
            const textNormalized = strong.textContent.trim().replace(/\s+/g, '');
            if (textNormalized === '推荐仓库') {
                const headerContainer = strong.closest('.mb-2');
                if (headerContainer) {
                    headerContainer.classList.add('gitee-cleanup-hidden');
                    
                    // 推荐仓库的列表 ul 是标题的下一个兄弟节点
                    const listContainer = headerContainer.nextElementSibling;
                    if (listContainer && listContainer.tagName.toLowerCase() === 'ul') {
                        listContainer.classList.add('gitee-cleanup-hidden');
                    }
                }
            }
        }

        // 4. 移除“智能客服”悬浮图标
        const customerServiceImg = document.querySelector('img[alt="智能客服"]');
        if (customerServiceImg) {
            const container = customerServiceImg.closest('.fixed') || customerServiceImg.closest('.z-40');
            if (container) {
                container.classList.add('gitee-cleanup-hidden');
            }
        }

        // 5. 执行 Favicon 锁定
        lockFavicon();
    }

    // 立即执行一次
    cleanGiteeUI();

    // 使用 MutationObserver 监控 DOM 树和 head link 属性的变化
    const observer = new MutationObserver(() => {
        cleanGiteeUI();
    });

    observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['href']
    });
})();
