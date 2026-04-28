// content.js

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extract_all_comments") {
        scrapeAllPages(request.maxPages || 10).then(allComments => {
            sendResponse({ success: true, data: allComments });
        }).catch(err => {
            sendResponse({ success: false, error: err.toString() });
        });
        return true; 
    }
});

async function scrapeAllPages(maxPages) {
    let allComments = new Set(); 
    let currentPage = 1;

    // TỰ ĐỘNG CUỘN TRANG (AUTO-SCROLL)
    // Cuộn từ từ xuống để Shopee kích hoạt API Lazy-load phần bình luận
    for(let i = 1; i <= 3; i++) {
        window.scrollTo(0, (document.body.scrollHeight / 3) * i);
        await sleep(800);
    }
    // Chờ thêm 2 giây để mạng tải DOM bình luận về
    await sleep(2000);

    while (currentPage <= maxPages) {
        // Quét bình luận - Thêm class shopee-product-rating__main dự phòng
        let commentNodes = document.querySelectorAll('.YNedDV, .shopee-product-rating__main');
        commentNodes.forEach(node => {
            let text = node.textContent.trim();
            if (text) allComments.add(text);
        });

        // Tìm nút Next
        let nextButton = document.querySelector('button.shopee-icon-button.shopee-icon-button--right');

        // Dừng nếu hết trang hoặc nút bị disable
        if (!nextButton || 
            nextButton.disabled || 
            nextButton.classList.contains('shopee-icon-button--disabled') || 
            nextButton.classList.contains('shopee-button-no-outline--non-click')) {
            break; 
        }

        // Chuyển trang và chờ 2.5s cho mỗi trang
        nextButton.click();
        currentPage++;
        await sleep(2500); 
    }

    return Array.from(allComments);
}