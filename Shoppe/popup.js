const API_URL = 'http://127.0.0.1:5000/api';

const emotionMap = {
    'Enjoyment': { name: 'Thích', emoji: '😍', polarity: 'pos', bg: 'bg-green-100', text: 'text-green-700' },
    'Surprise':  { name: 'Ngạc nhiên', emoji: '😲', polarity: 'pos', bg: 'bg-green-50', text: 'text-green-600' },
    'Other':     { name: 'Khác', emoji: '🤔', polarity: 'neu', bg: 'bg-slate-100', text: 'text-slate-700' },
    'Sadness':   { name: 'Buồn', emoji: '😢', polarity: 'neg', bg: 'bg-blue-100', text: 'text-blue-700' },
    'Anger':     { name: 'Giận', emoji: '😡', polarity: 'neg', bg: 'bg-red-100', text: 'text-red-700' },
    'Disgust':   { name: 'Chê', emoji: '🤢', polarity: 'neg', bg: 'bg-orange-100', text: 'text-orange-700' },
    'Fear':      { name: 'Sợ', emoji: '😨', polarity: 'neg', bg: 'bg-purple-100', text: 'text-purple-700' }
};

let scrapedData = []; 
let currentStats = { total: 0, emoCount: {}, polarity: { pos:0, neu:0, neg:0 } };
let currentEmotionFilter = null;

document.getElementById('btn-scan').addEventListener('click', scanShopeeComments);
document.getElementById('btn-reset-filter').addEventListener('click', resetFilter);
document.getElementById('btn-clear').addEventListener('click', clearAllData);

// Khôi phục dữ liệu nếu tắt/mở lại Panel
document.addEventListener('DOMContentLoaded', () => {
    chrome.storage.local.get(['savedShopeeData'], function(result) {
        if (result.savedShopeeData && result.savedShopeeData.length > 0) {
            scrapedData = result.savedShopeeData;
            calculateStats();
            updateChart();
            renderFilters();
            renderComments();
            document.getElementById('status-text').innerText = `Khôi phục ${scrapedData.length} bình luận`;
        }
    });
});

// Hàm xử lý xóa dữ liệu
function clearAllData() {
    if (confirm("Bạn có chắc chắn muốn xóa toàn bộ dữ liệu đã phân tích để quét sản phẩm mới?")) {
        scrapedData = [];
        currentEmotionFilter = null; // Bỏ lọc nếu đang có
        
        // Xóa trong bộ nhớ tạm của Chrome
        chrome.storage.local.remove(['savedShopeeData'], () => {
            calculateStats();
            updateChart();
            renderFilters();
            renderComments();
            
            // Reset giao diện
            document.getElementById('metrics-panel').style.display = 'none';
            document.getElementById('status-text').innerText = "Đã xóa dữ liệu. Sẵn sàng quét mới.";
            document.getElementById('current-filter-label').innerHTML = `Tất cả đánh giá`;
            document.getElementById('current-filter-label').style.color = '#334155';
            document.getElementById('btn-reset-filter').style.display = 'none';
            document.getElementById('btn-scan').innerHTML = `<svg style="width: 14px; height: 14px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg> Bắt đầu Quét`;
        });
    }
}

function scanShopeeComments() {
    const btn = document.getElementById('btn-scan');
    const status = document.getElementById('status-text');
    const metricsPanel = document.getElementById('metrics-panel');
    
    let maxPagesInput = document.getElementById('input-pages').value;
    const MAX_PAGES = parseInt(maxPagesInput) || 3;

    metricsPanel.style.display = 'none';
    btn.innerHTML = `<span style="font-size: 12px;">⏳</span> Đang quét...`;
    btn.disabled = true;
    
    status.innerText = `Đang tự động cuộn và lật tối đa ${MAX_PAGES} trang...`;

    // Dùng lastFocusedWindow thay vì currentWindow
    chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs) {
        if (!tabs || tabs.length === 0) {
            status.innerHTML = `<span style="color: red;">Lỗi: Không tìm thấy tab trình duyệt.</span>`;
            btn.innerHTML = `Quét Lại`;
            btn.disabled = false;
            return;
        }

        let activeTab = tabs[0];
        
        // Tránh lỗi undefined nếu activeTab không có url
        if (!activeTab.url || !activeTab.url.includes("shopee.vn")) {
            status.innerHTML = `<span style="color: red;">Lỗi: Bạn đang không ở trang Shopee.vn</span>`;
            btn.innerHTML = `Quét Lại`;
            btn.disabled = false;
            return;
        }

        let startCrawlTime = performance.now();

        // Biến MAX_PAGES bây giờ đã mang giá trị từ ô input và truyền sang content.js
        chrome.tabs.sendMessage(activeTab.id, {action: "extract_all_comments", maxPages: MAX_PAGES}, async function(response) {
            
            if (chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError);
                status.innerHTML = `<span style="color: red; font-weight: bold;">LỖI KẾT NỐI: Vui lòng nhấn F5 tải lại trang Shopee này rồi thử lại!</span>`;
                btn.innerHTML = `Quét Lại`;
                btn.disabled = false;
                return;
            }

            let endCrawlTime = performance.now();
            let crawlDuration = ((endCrawlTime - startCrawlTime) / 1000).toFixed(2);

            if (response && response.success && response.data.length > 0) {
                document.getElementById('time-crawl').innerText = crawlDuration + 's';
                status.innerText = `Đã cào ${response.data.length} comments. Đang AI dự đoán...`;
                metricsPanel.style.display = 'flex';

                let startPredictTime = performance.now();
                await analyzeBatchComments(response.data);
                let endPredictTime = performance.now();
                
                let predictDuration = ((endPredictTime - startPredictTime) / 1000).toFixed(2);
                document.getElementById('time-predict').innerText = predictDuration + 's';
                
            } else {
                status.innerHTML = `<span style="color: #ee4d2d;">Không tìm thấy bình luận. Hãy kiểm tra xem sản phẩm có đánh giá không.</span>`;
            }
            
            btn.innerHTML = `Quét (Cộng dồn)`;
            btn.disabled = false;
        });
    });
}

async function analyzeBatchComments(commentsArray) {
    try {
        const res = await fetch(`${API_URL}/predict_batch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comments: commentsArray })
        });
        
        if(!res.ok) throw new Error("Server Python trả về lỗi");
        
        const data = await res.json();
        
        scrapedData = scrapedData.concat(data); // Cộng dồn
        chrome.storage.local.set({ savedShopeeData: scrapedData }); // Lưu lại
        
        calculateStats();
        updateChart();
        renderFilters();
        renderComments();
        document.getElementById('status-text').innerText = `Đã phân tích xong ${scrapedData.length} bình luận`;

    } catch (error) {
        console.error(error);
        document.getElementById('status-text').innerText = "Lỗi mạng: App.py (Flask) chưa bật!";
    }
}

// ... (Giữ nguyên các hàm calculateStats, updateChart, renderFilters, filterByEmotion, resetFilter, renderComments của bạn ở dưới) ...
function calculateStats() {
    currentStats = { total: 0, emoCount: { Enjoyment:0, Surprise:0, Other:0, Sadness:0, Anger:0, Disgust:0, Fear:0 }, polarity: { pos:0, neu:0, neg:0 } };
    scrapedData.forEach(item => {
        if(emotionMap[item.emotion]) {
            currentStats.total++;
            currentStats.emoCount[item.emotion] = (currentStats.emoCount[item.emotion] || 0) + 1;
            currentStats.polarity[emotionMap[item.emotion].polarity]++;
        }
    });
    document.getElementById('total-count').innerText = currentStats.total;
}

function updateChart() {
    if(currentStats.total === 0) return;

    let pctPos = Math.round((currentStats.polarity.pos / currentStats.total) * 100) || 0;
    let pctNeu = Math.round((currentStats.polarity.neu / currentStats.total) * 100) || 0;
    let pctNeg = 100 - pctPos - pctNeu;

    document.getElementById('pct-pos').innerText = pctPos + '%';
    document.getElementById('pct-neu').innerText = pctNeu + '%';
    document.getElementById('pct-neg').innerText = pctNeg + '%';

    let posEnd = pctPos;
    let neuEnd = posEnd + pctNeu;
    const donut = document.getElementById('main-donut');
    donut.style.background = `conic-gradient(#22c55e 0% ${posEnd}%, #94a3b8 ${posEnd}% ${neuEnd}%, #ef4444 ${neuEnd}% 100%)`;
}

function renderFilters() {
    const container = document.getElementById('filter-buttons');
    container.innerHTML = '';
    
    let sortedEmos = Object.keys(emotionMap).map(key => {
        return { id: key, ...emotionMap[key], count: currentStats.emoCount[key] || 0 }
    }).filter(emo => emo.count > 0).sort((a,b) => b.count - a.count);

    sortedEmos.forEach(emo => {
        const btn = document.createElement('button');
        btn.className = `filter-btn ${emo.bg} ${emo.text}`;
        btn.innerHTML = `<span>${emo.emoji} ${emo.name}</span> <span style="font-weight:900;">${emo.count}</span>`;
        btn.onclick = () => filterByEmotion(emo.id, emo.name, emo.emoji);
        container.appendChild(btn);
    });
}

function filterByEmotion(id, name, emoji) {
    currentEmotionFilter = id;
    document.getElementById('current-filter-label').innerHTML = `Lọc: ${emoji} ${name}`;
    document.getElementById('current-filter-label').style.color = '#ee4d2d';
    document.getElementById('btn-reset-filter').style.display = 'block';
    renderComments();
}

function resetFilter() {
    currentEmotionFilter = null;
    document.getElementById('current-filter-label').innerHTML = `Tất cả đánh giá`;
    document.getElementById('current-filter-label').style.color = '#334155';
    document.getElementById('btn-reset-filter').style.display = 'none';
    renderComments();
}

function renderComments() {
    const container = document.getElementById('dynamic-comments');
    container.innerHTML = '';
    
    let filteredData = currentEmotionFilter ? scrapedData.filter(c => c.emotion === currentEmotionFilter) : scrapedData;

    if (filteredData.length === 0) {
        container.innerHTML = `
        <div class="empty-state">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            <span style="font-size: 11px; font-weight: 500;">Không có bình luận phù hợp</span>
        </div>`;
        return;
    }

    filteredData.forEach(comment => {
        let pol = emotionMap[comment.emotion].polarity;
        let starsCount = pol === 'pos' ? 5 : (pol === 'neu' ? 3 : 1);
        let starsHtml = '⭐'.repeat(starsCount) + '<span style="color:#e2e8f0;">' + '★'.repeat(5 - starsCount) + '</span>';
        
        let html = `
        <div class="cmt-item">
            <div class="cmt-header">
                <div class="shopee-star">${starsHtml}</div>
                <div class="cmt-badge ${emotionMap[comment.emotion].bg}">
                    ${emotionMap[comment.emotion].emoji} ${emotionMap[comment.emotion].name}
                </div>
            </div>
            <div class="cmt-text">
                ${comment.text}
            </div>
        </div>`;
        container.innerHTML += html;
    });
}