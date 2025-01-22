// chrome.runtime.onInstalled.addListener(() => {
//     console.log("Site Blocker extension installed");

//     // 동적으로 규칙 추가 예시
//     const newRule = {
//         id: 3,
//         priority: 1,
//         action: { type: "block" },
//         condition: { urlFilter: "blockedsite.com", resourceTypes: ["main_frame"] }
//     };

//     chrome.declarativeNetRequest.updateDynamicRules({
//         addRules: [newRule],
//         removeRuleIds: [3] // 기존 규칙 제거 (예: 규칙 ID 3)
//     });
// });

// 차단된 사이트 목록
let blockedSites = [];

// FastAPI로부터 차단된 사이트 목록 가져오기
async function fetchBlockedSites(userId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/blocked-site/${userId}`);
        const data = await response.json();
        /*
        JSON 형식으로 응답
        {
            "user_id": 1,
            "blocked_sites": [
                { "url": "https://www.youtube.com" },
                { "url": "https://www.facebook.com" }
            ]
        }
        */
        blockedSites = data.blocked_sites.map(site => new URL(site.url).hostname); 
        // url에서 도메인(예: youtube.com, facebook.com)만 추출하여 blockedSites 배열에 저장.
        console.log("Blocked sites updated:", blockedSites);
    } catch (error) {
        console.error("Failed to fetch blocked sites:", error);
    }
}

// WebRequest API로 요청 차단
chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        const url = new URL(details.url).hostname; // 요청된 URL의 도메인만 추출해서 가져옴
        if (blockedSites.includes(url)) { // blockedSites 배열에 도메인이 포함되어 있는지 확인
            console.log(`Blocked: ${url}`);
            return { cancel: true }; // 요청 취소
        }
        return { cancel: false };
    },
    { urls: ["<all_urls>"] }, // 모든 URL에 대해 작동
    ["blocking"]
);

// 사용자 ID 설정 및 차단 목록 갱신

const userId = 1; // FastAPI에서 사용할 사용자 ID -> 추후 로그인 기능 추가 시 사용자 ID 동적으로 설정(이걸 구글 로그인할때 받아오면 될듯)

fetchBlockedSites(userId); // 확장 프로그램 시작 시 차단 목록 불러오기

// 차단 목록을 일정 시간마다 업데이트 (예: 3분 간격)
setInterval(() => fetchBlockedSites(userId), 180000);
