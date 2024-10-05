import * as cheerio from "cheerio";

export const getDomElementsFromActiveTab = async (
  tabId: number,
  targetClasses: { target: string; eq: number }[]
) => {
  let domRes = await chrome.scripting
    .executeScript({
      target: { tabId },
      func: () => {
        const elements = document.getElementsByTagName("div");
        const htmlContents = Array.from(elements, (el) => el.innerHTML);
        return htmlContents.join("");
      },
    })
    .catch(console.error);

  if (!domRes) return;

  const $ = cheerio.load(domRes[0].result as any);

  function filterBreakingLines(inputString: string) {
    // Split the input string by newline characters and trim each element
    const values = inputString
      .split("\n")
      .map((value) => value.trim())
      .filter((value) => value.length > 0); // Filter out empty strings

    return values;
  }

  const result = targetClasses.map((targetClass) => {
    const elementText = $(targetClass.target).eq(targetClass.eq).text().trim();
    return {
      class: targetClass,
      data: elementText.includes("\n")
        ? filterBreakingLines(elementText)
        : elementText,
    };
  });

  return result;
};

// Will return string that matches a price format like "£x,xxx pcm" / "£x,xxx pw"
export const getDomElementContainingPriceFormat = async (
  tabId: number,
  searchText: string
): Promise<string> => {
  const domRes = await chrome.scripting
    .executeScript({
      target: { tabId },
      func: (partialText: string): string | null => {
        const allElements = Array.from(document.querySelectorAll("span"));
        const regex = new RegExp(`\\£\\s*\\d+[,.\\d]*\\s+${partialText}`, "i");

        for (let i = 0; i < allElements.length; i++) {
          const element = allElements[i];
          if (regex.test(element.textContent ?? "")) {
            return element.textContent?.match(regex)?.[0].trim() ?? null;
          }
        }
        return null;
      },
      args: [searchText],
    })
    .catch(console.error);

  if (!domRes || !domRes[0] || !domRes[0].result) {
    return "";
  }

  return domRes[0].result;
};

export const getFlatDataFromRightmove = (
  tabId: number,
  tabUrl: string,
  onClickAction: (title: string, url: string, price: string) => void
) => {
  const saveData = async () => {
    const flatData = await getDomElementsFromActiveTab(tabId, [
      { target: `[itemprop="streetAddress"]`, eq: 0 },
    ]);

    const title = flatData && flatData[0].data;

    return onClickAction(
      title as string,
      tabUrl,
      await getDomElementContainingPriceFormat(tabId, "pcm")
    );
  };
  return saveData();
};

export const getFlatDataFromOpenRent = (
  tabId: number,
  tabUrl: string,
  onClickAction: (title: string, url: string, price: string) => void
) => {
  const saveData = async () => {
    const flatData = await getDomElementsFromActiveTab(tabId, [
      { target: ".price-title", eq: 0 },
      { target: ".property-title", eq: 0 },
    ]);
    const price = flatData && flatData[0].data;
    const title = flatData && flatData[1].data;
    console.log("flatdata", flatData);
    return onClickAction(title as string, tabUrl, price as string);
  };
  return saveData();
};

export const getFlatDataFromSpareroom = (
  tabId: number,
  tabUrl: string,
  onClickAction: (title: string, url: string, price: string) => void
) => {
  const saveData = async () => {
    const flatData = await getDomElementsFromActiveTab(tabId, [
      { target: ".feature-list__key", eq: 0 },
      { target: "h1", eq: 0 },
    ]);
    const price = flatData && flatData[0].data;
    const title = flatData && flatData[1].data;
    console.log("flatdata", flatData);
    return onClickAction(title as string, tabUrl, price as string);
  };
  return saveData();
};

export const getFlatDataFromZoopla = (
  tabId: number,
  tabUrl: string,
  onClickAction: (title: string, url: string, price: string) => void
) => {
  const saveData = async () => {
    const flatData = await getDomElementsFromActiveTab(tabId, [
      { target: `[data-testid="price"]`, eq: 0 },
      { target: `[data-testid="address-label"]`, eq: 0 },
    ]);
    const price = flatData && flatData[0].data;
    const title = flatData && flatData[1].data;
    console.log("flatdata", flatData);
    return onClickAction(title as string, tabUrl, price as string);
  };
  return saveData();
};

/**
 *
 * When saving flats to the api, we need to filter parameters. We cannot do this for spareroom though, as the flat id is included as a parameter.
 */
export const propertyUrlToSend = (
  type: "spareroom" | "any" = "any",
  url: string
) => {
  if (type === "spareroom") {
    return url?.split("&search_id")[0];
  } else {
    return url?.split("?")[0];
  }
};
