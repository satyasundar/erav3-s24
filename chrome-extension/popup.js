document.getElementById("run-btn").onclick = async () => {
  const prompt = document.getElementById("prompt").value;
  const spinner = document.getElementById("spinner");
  const resultBox = document.getElementById("result");

  resultBox.textContent = "";
  spinner.classList.remove("hidden");

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

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
        resultBox.textContent = "✅ " + data.result;
      }
    );
  } catch (error) {
    console.error("Error:", error);
    resultBox.textContent = "❌ Something went wrong!";
  } finally {
    spinner.classList.add("hidden");
  }
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
