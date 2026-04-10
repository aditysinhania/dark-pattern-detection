// Prevent duplicate processing per tab
const activeRequests = new Set();

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyze") {
    const tabId = sender.tab.id;

    // 🔥 Prevent multiple calls from same tab
    if (activeRequests.has(tabId)) {
      console.log("Already processing for this tab, skipping...");
      return;
    }

    activeRequests.add(tabId);

    console.log("Processing request from tab:", tabId);

    fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: request.text })
    })
      .then((res) => res.json())
      .then((data) => {
        sendResponse(data);
      })
      .catch((err) => {
        console.error("API Error:", err);
        sendResponse({ error: "API failed" });
      })
      .finally(() => {
        // ✅ allow future requests after completion
        activeRequests.delete(tabId);
      });

    return true; // keep async alive
  }
});