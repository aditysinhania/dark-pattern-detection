document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  try {
    // Inject content script every time
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ["content.js"]
    });

    // Small delay before sending message
    setTimeout(() => {
      chrome.tabs.sendMessage(tab.id, { action: "analyze" });
    }, 200);

  } catch (err) {
    console.error("Error:", err);
  }
});