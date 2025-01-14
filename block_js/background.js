chrome.runtime.onInstalled.addListener(() => {
    console.log("Site Blocker extension installed");

    // 동적으로 규칙 추가 예시
    const newRule = {
        id: 3,
        priority: 1,
        action: { type: "block" },
        condition: { urlFilter: "blockedsite.com", resourceTypes: ["main_frame"] }
    };

    chrome.declarativeNetRequest.updateDynamicRules({
        addRules: [newRule],
        removeRuleIds: [3] // 기존 규칙 제거 (예: 규칙 ID 3)
    });
});
