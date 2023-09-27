export const setGroupCode = (code: string) => {
  chrome.storage.local.set({ groupCode: code }, function () {
    if (chrome.runtime.lastError) {
      console.error(chrome.runtime.lastError);
    }
  });
};

export const getGroupCode = async () => {
  return new Promise<string | undefined>((resolve) => {
    chrome.storage.local.get("groupCode", function (result) {
      console.log("result");
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
        resolve(undefined);
      } else {
        const groupCode = result.groupCode;
        resolve(groupCode);
      }
    });
  });
};
