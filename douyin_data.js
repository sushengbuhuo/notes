// ==UserScript==
// @name         dy
// @namespace    http://tampermonkey.net/
// @version      0.0.1
// @description  抖音用户主页数据
// @author       
// @match        https://www.douyin.com/user/*
// @icon         
// @grant        none
// @license MIT
// ==/UserScript==

(function () {
    'use strict';
    let table;

    function initGbkTable() {
        // https://en.wikipedia.org/wiki/GBK_(character_encoding)#Encoding
        const ranges = [
            [0xA1, 0xA9, 0xA1, 0xFE],
            [0xB0, 0xF7, 0xA1, 0xFE],
            [0x81, 0xA0, 0x40, 0xFE],
            [0xAA, 0xFE, 0x40, 0xA0],
            [0xA8, 0xA9, 0x40, 0xA0],
            [0xAA, 0xAF, 0xA1, 0xFE],
            [0xF8, 0xFE, 0xA1, 0xFE],
            [0xA1, 0xA7, 0x40, 0xA0],
        ];
        const codes = new Uint16Array(23940);
        let i = 0;

        for (const [b1Begin, b1End, b2Begin, b2End] of ranges) {
            for (let b2 = b2Begin; b2 <= b2End; b2++) {
                if (b2 !== 0x7F) {
                    for (let b1 = b1Begin; b1 <= b1End; b1++) {
                        codes[i++] = b2 << 8 | b1
                    }
                }
            }
        }
        table = new Uint16Array(65536);
        table.fill(0xFFFF);
        const str = new TextDecoder('gbk').decode(codes);
        for (let i = 0; i < str.length; i++) {
            table[str.charCodeAt(i)] = codes[i]
        }
    }

    function str2gbk(str, opt = {}) {
        if (!table) {
            initGbkTable()
        }
        const NodeJsBufAlloc = typeof Buffer === 'function' && Buffer.allocUnsafe;
        const defaultOnAlloc = NodeJsBufAlloc
            ? (len) => NodeJsBufAlloc(len)
            : (len) => new Uint8Array(len);
        const defaultOnError = () => 63;
        const onAlloc = opt.onAlloc || defaultOnAlloc;
        const onError = opt.onError || defaultOnError;

        const buf = onAlloc(str.length * 2);
        let n = 0;

        for (let i = 0; i < str.length; i++) {
            const code = str.charCodeAt(i);
            if (code < 0x80) {
                buf[n++] = code;
                continue
            }
            const gbk = table[code];

            if (gbk !== 0xFFFF) {
                buf[n++] = gbk;
                buf[n++] = gbk >> 8
            } else if (code === 8364) {
                buf[n++] = 0x80
            } else {
                const ret = onError(i, str);
                if (ret === -1) {
                    break
                }
                if (ret > 0xFF) {
                    buf[n++] = ret;
                    buf[n++] = ret >> 8
                } else {
                    buf[n++] = ret
                }
            }
        }
        return buf.subarray(0, n)
    }

    let aweme_list = [];
    let userKey = [
        "昵称", "关注", "粉丝",
        "获赞", "抖音号", "IP属地",
        "年龄", "签名", "作品数", "主页"
    ];
    let userData = [];
    let timer;

    function extractDataFromScript() {
        const scriptTag = document.getElementById('RENDER_DATA');
        if (!scriptTag) return;
        let data = JSON.parse(decodeURIComponent(scriptTag.innerHTML));

        for (const prop in data) {
            if (prop !== "_location" && prop !== "app") {
                let userInfo = data[prop].user.user;
                userData.push(
                    userInfo.nickname, userInfo.followingCount, userInfo.mplatformFollowersCount,
                    userInfo.totalFavorited, '\t' + (userInfo.uniqueId === "" ? userInfo.uniqueId : userInfo.shortId), userInfo.ipLocation,
                    userInfo.age, '"' + (userInfo.desc === undefined ? '' : userInfo.desc) + '"', userInfo.awemeCount, "https://www.douyin.com/user/" + userInfo.secUid
                );
            }
        }
        timer = setTimeout(() => createDownloadButton(), 1000);
    }

    function copyToClipboard(text) {
        try {
            const textarea = document.createElement("textarea");
            textarea.setAttribute('readonly', 'readonly');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            let flag = document.execCommand("copy");
            document.body.removeChild(textarea);
            return flag;
        } catch (e) {
            console.log(e);
            return false;
        }
    }

    function openLink(url) {
        const link = document.createElement('a');
        link.href = url;
        link.target = "_blank";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function createVideoButton(text, top, func) {
        const button = document.createElement("button");
        button.textContent = text;
        button.style.position = "absolute";
        button.style.right = "0px";
        button.style.top = top;
        button.style.opacity = "0.5";
        button.addEventListener("click", func);
        return button;
    }

    function createDownloadButton() {
        let targetNodes = document.querySelectorAll("ul.EZC0YBrG > li.Eie04v01 > div > a");
        for (let i = 0; i < targetNodes.length; i++) {
            let targetNode = targetNodes[i];
            if (targetNode.dataset.added)
                continue;
            const button2 = createVideoButton("复制链接", "0px", (event) => {
                event.preventDefault();
                event.stopPropagation();
                if (copyToClipboard(aweme_list[i].url))
                    button2.textContent = "复制成功";
                else
                    button2.textContent = "复制失败";
                setTimeout(() => {
                    button2.textContent = '复制链接';
                }, 2000);
            });
            targetNode.appendChild(button2);
            const button3 = createVideoButton("打开链接", "21px", (event) => {
                event.preventDefault();
                event.stopPropagation();
                openLink(aweme_list[i].url);
            });
            targetNode.appendChild(button3);
            const button = createVideoButton("下载", "42px", (event) => {
                event.preventDefault();
                event.stopPropagation();
                let xhr = new XMLHttpRequest();
                xhr.open('GET', aweme_list[i].url.replace("http://", "https://"), true);
                xhr.responseType = 'blob';
                xhr.onload = (e) => {
                    let a = document.createElement('a');
                    a.href = window.URL.createObjectURL(xhr.response);
                    a.download = (aweme_list[i].desc ? aweme_list[i].desc.replace(/[\/:*?"<>|]/g, "") : aweme_list[i].awemeId) + ".mp4";
                    a.click()
                };
                xhr.onprogress = (event) => {
                    if (event.lengthComputable) {
                        button.textContent = "下载" + (event.loaded * 100 / event.total).toFixed(1) + '%';
                    }
                };
                xhr.send();
            });
            targetNode.appendChild(button);
            targetNode.dataset.added = true;
        }
    }

    function createButton(title, top) {
        top = top === undefined ? "60px" : top;
        const button = document.createElement('button');
        button.textContent = title;
        button.style.position = 'fixed';
        button.style.right = '5px';
        button.style.top = top;
        button.style.zIndex = '90000';
        document.body.appendChild(button);
        return button
    }

    function txt2file(txt, filename) {
        const blob = new Blob([txt], {type: 'text/plain'});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename.replace(/[\/:*?"<>|]/g, "");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    function downloadData(encoding) {
        let text = userKey.join(",") + "\n" + userData.join(",") + "\n\n";
        text += "作品描述,作品链接,点赞数,评论数,收藏数,分享数,发布时间,下载链接\n";
        aweme_list.forEach(item => {
            text += ['"' + item.desc + '"', "https://www.douyin.com/video/"+item.awemeId, item.diggCount, item.commentCount,
                item.collectCount, item.shareCount, item.date, item.url].join(",") + "\n"
        });
        if (encoding === "gbk")
            text = str2gbk(text);
        txt2file(text, userData[0] + ".csv");
    }

    function interceptResponse() {
        const originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function () {
            const self = this;
            this.onreadystatechange = function () {
                if (self.readyState === 4) {
                    if (self._url.indexOf("/aweme/v1/web/aweme/post") > -1) {
                        var json = JSON.parse(self.response);
                        let post_data = json.aweme_list.map(item => Object.assign(
                            {"awemeId": item.aweme_id, "desc": item.desc},
                            {
                                "diggCount": item.statistics.digg_count,
                                "commentCount": item.statistics.comment_count,
                                "collectCount": item.statistics.collect_count,
                                "shareCount": item.statistics.share_count
                            },
                            {
                                "date": new Date(item.create_time * 1000).toLocaleString(),
                                "url": item.video.play_addr.url_list[0]
                            }));
                        aweme_list = aweme_list.concat(post_data);
                        if (timer !== undefined)
                            clearTimeout(timer);
                        timer = setTimeout(() => createDownloadButton(), 1000);
                    }
                }
            };
            originalSend.apply(this, arguments);
        };
    }

    function scrollPageToBottom() {
        const SCROLL_DELAY = 1000; // Adjust the delay between each scroll action (in milliseconds)
        let scrollInterval;

        function getScrollPosition() {
            return scrollY || pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;
        }

        function scrollToBottom() {
            scrollTo(0, document.body.scrollHeight);
        }

        function hasReachedBottom() {
            return getScrollPosition() >= (document.body.scrollHeight - innerHeight);
        }

        function scrollLoop() {
            if (!hasReachedBottom()) {
                scrollToBottom();
            } else {
                console.log("Reached the bottom of the page!");
                clearInterval(scrollInterval);
            }
        }

        function startScrolling() {
            scrollInterval = setInterval(scrollLoop, SCROLL_DELAY);
        }

        let button = createButton('开启自动下拉到底', '60px');
        button.addEventListener('click', startScrolling);
    }

    // To start scrolling, call the function:
    scrollPageToBottom();
    interceptResponse();
    window.onload = () => {
        extractDataFromScript();
        createButton("下载已加载数据", "81px").addEventListener('click', (e) => downloadData("gbk"));
    };
})();
