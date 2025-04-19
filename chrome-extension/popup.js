document.getElementById("run-btn").onclick = async () => {
  const prompt = document.getElementById("prompt").value;
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript(
    {
      target: { tabId: tab.id },
      func: scrapeTelegramMessages,
    },
    async (results) => {
      const messages = results[0].result;
      const res = await fetch("http://localhost:8000/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, messages }),
      });
      const data = await res.json();
      document.getElementById("result").textContent = data.result;
    }
  );
};

function scrapeTelegramMessages() {
  const messageNodes = document.querySelectorAll("[data-timestamp]");
  const messages = [];

  messageNodes.forEach((node) => {
    const text = node.innerText || "";
    const ts = node.getAttribute("data-timestamp");

    if (text && ts) {
      const timestamp = new Date(parseInt(ts) * 1000).toISOString();
      messages.push({ text, timestamp });
    }
  });

  return messages;
}
