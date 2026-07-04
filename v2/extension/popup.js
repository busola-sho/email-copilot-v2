const API_URL = "https://email-copilotv2.onrender.com/";

const emailBodyInput = document.getElementById("emailBody");
const draftReplyInput = document.getElementById("draftReply");
const generateButton = document.getElementById("generateButton");
const copyButton = document.getElementById("copyButton");
const statusText = document.getElementById("status");
const metadata = document.getElementById("metadata");

async function loadSelectedText() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => window.getSelection().toString()
    });

    const selectedText = results[0].result.trim();

    if (selectedText) {
      emailBodyInput.value = selectedText;
      emailBodyInput.classList.add("prefilled");
      statusText.textContent = "Selected text loaded. Edit if needed.";
    }
  } catch (error) {
    statusText.textContent = "";
  }
}

emailBodyInput.addEventListener("focus", () => {
  emailBodyInput.classList.remove("prefilled");
});

generateButton.addEventListener("click", async () => {
  const emailBody = emailBodyInput.value.trim();

  if (!emailBody) {
    statusText.textContent = "Please paste or select an email first.";
    return;
  }

  statusText.textContent = "Generating reply...";
  draftReplyInput.value = "";
  metadata.textContent = "";
  generateButton.disabled = true;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email_body: emailBody })
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();

    draftReplyInput.value = data.draft;
    metadata.textContent = `Intent: ${data.intent} | Confidence: ${data.confidence} | Needs review: ${data.needs_review}`;
    statusText.textContent = "Draft generated.";
  } catch (error) {
    statusText.textContent = `Error: ${error.message}`;
  } finally {
    generateButton.disabled = false;
  }
});

copyButton.addEventListener("click", async () => {
  const draft = draftReplyInput.value.trim();

  if (!draft) {
    statusText.textContent = "No draft to copy yet.";
    return;
  }

  await navigator.clipboard.writeText(draft);
  statusText.textContent = "Draft copied.";
});

loadSelectedText();