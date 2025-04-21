async function scrapeTelegramMessagesWithScroll() {
  const messages = new Set();
  const maxScrolls = 40;
  let scrollCount = 0;

  const scrollContainer =
    document.querySelector(".message-list__wrapper") ||
    document.querySelector('[class*="Scroll"][class*="scroll"]') || // fallback class
    document.querySelector('[role="presentation"]'); // Telegram is obfuscated

  if (!scrollContainer) {
    return [];
  }

  while (scrollCount < maxScrolls) {
    const visibleMessages = document.querySelectorAll("[data-timestamp]");
    visibleMessages.forEach((node) => {
      const text = node.innerText || "";
      const ts = node.getAttribute("data-timestamp");

      if (text && ts) {
        const timestamp = new Date(parseInt(ts) * 1000).toISOString();
        messages.add(JSON.stringify({ text, timestamp }));
      }
    });

    scrollContainer.scrollTop = 0; // scroll to top
    await new Promise((resolve) => setTimeout(resolve, 1000));
    scrollCount++;
  }

  return Array.from(messages).map((m) => JSON.parse(m));
}

scrapeTelegramMessagesWithScroll().then((msgs) => {
  window.postMessage({ type: "TELEGRAM_MESSAGES", payload: msgs }, "*");
});
