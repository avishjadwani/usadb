function readCSVFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = () => {
      const data = Papa.parse(reader.result, { header: true });
      if (data.errors.length) {
        reject(data.errors);
      } else {
        resolve(data.data);
      }
    };
    reader.onerror = () => {
      reject(reader.error);
    };
  });
}

function generateDataDescription(data) {
  // TODO: Write code to analyze the data and generate a description.
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "CSV_FILE_SELECTED") {
    readCSVFile(message.file)
      .then(generateDataDescription)
      .then((description) => {
        sendResponse({ type: "DATA_DESCRIPTION_GENERATED", description });
      })
      .catch((error) => {
        sendResponse({ type: "ERROR", error });
      });
    return true;
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "SELECT_CSV_FILE") {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".csv";
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      chrome.runtime.sendMessage({ type: "CSV_FILE_SELECTED", file }, (response) => {
        if (response.type === "DATA_DESCRIPTION_GENERATED") {
          console.log(response.description);
        } else {
          console.error(response.error);
        }
      });
    });
    fileInput.click();
  }
});

