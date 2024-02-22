export function extractNumber(input: string): number {
  return parseFloat(input.replace(/[^0-9.]/g, ""));
}
