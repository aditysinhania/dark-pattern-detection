// Prevent multiple injections
if (window.__DP_CONTENT_LOADED__) {
  console.log("Content script already loaded");
} else {
  window.__DP_CONTENT_LOADED__ = true;

  class DarkPatternDetector {
    constructor() {
      this.running = false;
      this.highlights = [];
    }

    analyzePage() {
      if (this.running) return;
      this.running = true;

      try {
        const text = document.body.innerText;
        if (!text) {
          this.running = false;
          return;
        }

        console.log("Sending text to background...");

        chrome.runtime.sendMessage(
          { action: "analyze", text: text },
          (response) => {
            if (!response || response.error) {
              console.error("API Error");
              this.running = false;
              return;
            }

            console.log("Received result:", response);
            this.displayResults(response);
            this.running = false;
          }
        );
      } catch (e) {
        console.error(e);
        this.running = false;
      }
    }

    displayResults(result) {
      this.clearHighlights();

      if (!result.dark_patterns || result.dark_patterns.length === 0) {
        this.showNotification("No dark patterns detected");
        return;
      }

      result.dark_patterns.forEach(pattern => {
        pattern.matched_phrases.forEach(phrase => {
          this.highlightText(phrase, pattern.name);
        });
      });

      this.showNotification(
        `Detected ${result.dark_patterns.length} dark pattern(s)`
      );
    }

    highlightText(text, label) {
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT
      );

      let node;
      const regex = new RegExp(text, "gi");

      while ((node = walker.nextNode())) {
        if (!node.nodeValue.trim()) continue;

        if (regex.test(node.nodeValue)) {
          const span = document.createElement("span");
          span.style.background = "yellow";
          span.title = label;

          const parts = node.nodeValue.split(regex);
          const matches = node.nodeValue.match(regex);

          const fragment = document.createDocumentFragment();

          parts.forEach((part, i) => {
            fragment.appendChild(document.createTextNode(part));
            if (matches && matches[i]) {
              const mark = span.cloneNode();
              mark.textContent = matches[i];
              fragment.appendChild(mark);
              this.highlights.push(mark);
            }
          });

          node.parentNode.replaceChild(fragment, node);
        }
      }
    }

    clearHighlights() {
      this.highlights.forEach(el => {
        if (el.parentNode) {
          el.replaceWith(document.createTextNode(el.textContent));
        }
      });
      this.highlights = [];
    }

    showNotification(message) {
      const existing = document.getElementById("dp-notify");
      if (existing) existing.remove();

      const div = document.createElement("div");
      div.id = "dp-notify";
      div.textContent = message;

      div.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: black;
        color: white;
        padding: 10px;
        z-index: 999999;
      `;

      document.body.appendChild(div);
      setTimeout(() => div.remove(), 3000);
    }
  }

  const detector = new DarkPatternDetector();

  chrome.runtime.onMessage.addListener((req) => {
    if (req.action === "analyze") {
      detector.analyzePage();
    }
  });
}