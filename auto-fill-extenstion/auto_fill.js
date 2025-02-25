chrome.webNavigation.onCompleted.addListener((details) => {
    chrome.scripting.executeScript({
        target: { tabId: details.tabId },
        files: ["content.js"]
    });
}, { url: [{ hostContains: "greenhouse.io" }] });
