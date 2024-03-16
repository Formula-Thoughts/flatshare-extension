export function extractNumber(input: string): number {
  return parseFloat(input.replace(/[^0-9.]/g, ""));
}

export function getObjectByKeyPart(keyPart: string, obj: any): any {
  for (const [key, value] of Object.entries(obj)) {
    if (key.includes(keyPart)) {
      return value;
    }
  }

  return null;
}

export function extractNumberFromString(str: string): number {
  // Remove currency symbol and comma
  const numberStr = str.replace(/[^0-9.-]+/g, "");
  // Parse the string as a number
  const number = parseFloat(numberStr);
  return number;
}
