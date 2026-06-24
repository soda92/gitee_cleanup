// ==UserScript==
// @name         Gitee移除多余推荐菜单
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  移除 Gitee 工作台的“推荐关注”、“推荐仓库”板块，以及“智能客服”浮标、“模力方舟”和“AI队友”导航菜单
// @author       You
// @match        https://gitee.com/
// @match        https://gitee.com/dashboard
// @match        https://gitee.com/dashboard/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gitee.com
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    function cleanGiteeUI() {
        const spans = document.querySelectorAll('span');

        for (const span of spans) {
            const textNormalized = span.textContent.trim().replace(/\s+/g, '');

            // 1. 移除“推荐关注”
            if (textNormalized === '推荐关注') {
                const container = span.closest('.mb-4');
                if (container) container.remove();
            }

            // 2. 移除导航菜单项：“模力方舟”
            if (textNormalized === '模力方舟') {
                const li = span.closest('li');
                if (li) li.remove();
            }

            // 3. 移除导航菜单项：“AI队友”
            if (textNormalized === 'AI队友') {
                const li = span.closest('li');
                if (li) li.remove();
            }
        }

        // 4. 移除“推荐仓库”
        const strongs = document.querySelectorAll('strong');
        for (const strong of strongs) {
            const textNormalized = strong.textContent.trim().replace(/\s+/g, '');
            if (textNormalized === '推荐仓库') {
                const headerContainer = strong.closest('.mb-2');
                if (headerContainer) {
                    const listContainer = headerContainer.nextElementSibling;
                    if (listContainer && listContainer.tagName.toLowerCase() === 'ul') {
                        listContainer.remove();
                    }
                    headerContainer.remove();
                }
            }
        }

        // 5. 移除“智能客服”悬浮图标
        const customerServiceImg = document.querySelector('img[alt="智能客服"]');
        if (customerServiceImg) {
            const container = customerServiceImg.closest('.fixed') || customerServiceImg.closest('.z-40');
            if (container) {
                container.remove();
            }
        }
    }

    // 立即执行一次
    cleanGiteeUI();

    // 使用 MutationObserver 监控 DOM 树变化，实时清除动态加载渲染的元素
    const observer = new MutationObserver(() => {
        cleanGiteeUI();
    });

    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });
})();
