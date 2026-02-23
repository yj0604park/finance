import { Decimal } from "decimal.js";

/**
 * Format a numeric value as a currency string.
 */
export function formatCurrency(amount: string | number | null | undefined, currency: string): string {
  const sign = currency === "USD" ? "$" : "₩";
  const digits = currency === "USD" ? 2 : 0;

  if (amount == null || amount === "") {
    return `${sign} 0${digits > 0 ? `.${  "0".repeat(digits)}` : ""}`;
  }

  const decimal = new Decimal(amount);

  const formatted = decimal
    .abs()
    .toNumber()
    .toLocaleString("ko-KR", { minimumFractionDigits: digits });

  if (decimal.isNegative()) {
    return `-${sign} ${formatted}`;
  }
  return `${sign} ${formatted}`;
}

/**
 * Format as accounting style: negatives in parentheses, zero as em dash.
 */
export function formatAccounting(amount: string | number | null | undefined, currency: string): string {
  const decimal = new Decimal(amount ?? 0);
  if (decimal.isZero()) return "—";

  const formatted = formatCurrency(decimal.abs().toString(), currency);
  return decimal.isNegative() ? `(${formatted})` : formatted;
}

/**
 * Format as accounting style in USD.
 */
export function formatAccountingUSD(amount: string | number | null | undefined): string {
  return formatAccounting(amount, "USD");
}

/**
 * Get a Tailwind color class based on value sign.
 */
export function getDisplayColor(value: string | number | null | undefined): string {
  const decimal = new Decimal(value ?? 0);
  if (decimal.isNegative()) return "text-red-600";
  if (decimal.isZero()) return "text-muted-foreground";
  return "text-foreground";
}

/**
 * Sum bank balances for a specific currency.
 */
export function getTotalBalance(
  bankList: ReadonlyArray<{
    node: { balance: ReadonlyArray<{ currency: string; value: string }> };
  }>,
  currency: string,
): string {
  let sum = new Decimal(0);
  for (const bank of bankList) {
    for (const b of bank.node.balance) {
      if (b.currency === currency) {
        sum = sum.plus(new Decimal(b.value));
      }
    }
  }
  return sum.toString();
}

/**
 * Safely convert a value to a number.
 */
export function toNumber(value: string | number | null | undefined): number {
  try {
    return new Decimal(value ?? 0).toNumber();
  } catch {
    return 0;
  }
}

/**
 * Split an array into chunks.
 */
export function chunk<T>(array: T[], size: number): T[][] {
  const result: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}
