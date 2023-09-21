// content.js
console.log("content.js");
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.command === "SCRAPE") {
    try {
      sendResponse({ price: getAllTextEndingWithPCM(document.body) });
    } catch (error) {
      console.log("error: ", error);
      sendResponse({ data: " ERROR " });
    }
  }
});

function getAllTextEndingWithPCM(element) {
  console.log("getAllTextEndingWithPCM!");
  let textContent = "";

  // Helper function to recursively traverse and collect text
  function traverse(node) {
    // Exclude script and style tags
    if (node.nodeName === "SCRIPT" || node.nodeName === "STYLE") {
      return;
    }
    // If the node is a text node and it ends with "pcm", add its content to the textContent
    if (
      node.nodeType === Node.TEXT_NODE &&
      /pcm$/i.test(node.textContent?.trim())
    ) {
      textContent += node.textContent?.trim() + " ";
    }

    // Recursively traverse child nodes
    for (const childNode of node.childNodes) {
      traverse(childNode);
    }
  }
  traverse(element || document.body);

  return textContent.trim();
}
