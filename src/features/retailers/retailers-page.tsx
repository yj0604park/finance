import { useMemo, useState } from "react";
import { format, subMonths } from "date-fns";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { useGetAllTransactionsQuery } from "@/graphql/generated/graphql";
import { formatCurrency, toNumber } from "@/lib/format";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Decimal } from "decimal.js";

export function RetailersPage() {
  const defaultEndDate = format(new Date(), "yyyy-MM-dd");
  const defaultStartDate = format(subMonths(new Date(), 3), "yyyy-MM-dd");

  const [startDate, setStartDate] = useState<string>(defaultStartDate);
  const [endDate, setEndDate] = useState<string>(defaultEndDate);
  const [currency, setCurrency] = useState<string>("USD");

  const { data, loading, error } = useGetAllTransactionsQuery({
    variables: {
      first: 1000,
      after: "",
      accountId: null,
      dateGte: startDate || null,
      dateLte: endDate || null,
    },
  });

  const transactions = data?.transactionRelay?.edges ?? [];

  const retailerSummary = useMemo(() => {
    const map: Record<string, { name: string; spending: Decimal; income: Decimal; count: number }> = {};

    for (const edge of transactions) {
      const tx = edge.node;
      if (tx.account.currency !== currency || tx.isInternal) continue;
      const name = tx.retailer?.name ?? "(No Retailer)";
      const key = tx.retailer?.id ?? "__none__";

      if (!map[key]) {
        map[key] = { name, spending: new Decimal(0), income: new Decimal(0), count: 0 };
      }
      const amount = new Decimal(tx.amount);
      if (amount.isNegative()) {
        map[key].spending = map[key].spending.plus(amount.abs());
      } else {
        map[key].income = map[key].income.plus(amount);
      }
      map[key].count += 1;
    }

    return Object.values(map)
      .sort((a, b) => b.spending.comparedTo(a.spending));
  }, [transactions, currency]);

  const top10 = retailerSummary.slice(0, 10);
  const chartData = top10.map((r) => ({
    name: r.name.length > 15 ? `${r.name.slice(0, 15)}…` : r.name,
    spending: toNumber(r.spending.toString()),
  }));

  const totalSpending = retailerSummary.reduce(
    (acc, r) => acc.plus(r.spending),
    new Decimal(0),
  );

  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-6 text-destructive">
        Failed to load data: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Retailers</h1>
        <Badge variant="outline">{retailerSummary.length} retailers</Badge>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="flex flex-wrap gap-4 pt-6">
          <div className="w-32">
            <Select value={currency} onValueChange={setCurrency}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="USD">USD</SelectItem>
                <SelectItem value="KRW">KRW</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center gap-2">
            <Input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-40"
            />
            <span className="text-muted-foreground text-sm">~</span>
            <Input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-40"
            />
          </div>
        </CardContent>
      </Card>

      {loading ? (
        <div className="space-y-4">
          <Skeleton className="h-64 w-full" />
          <Skeleton className="h-96 w-full" />
        </div>
      ) : (
        <>
          {/* Bar chart - top 10 */}
          {chartData.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Top 10 Retailers by Spending</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={chartData} layout="vertical" margin={{ left: 16 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <XAxis
                      type="number"
                      tickFormatter={(v: number) =>
                        currency === "USD" ? `$${(v / 1000).toFixed(0)}k` : `₩${(v / 10000).toFixed(0)}만`
                      }
                    />
                    <YAxis type="category" dataKey="name" width={120} tick={{ fontSize: 12 }} />
                    <Tooltip
                      formatter={(value: number) =>
                        [formatCurrency(value.toString(), currency), "Spending"]
                      }
                    />
                    <Bar dataKey="spending" fill="#6366f1" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          )}

          {/* Full table */}
          <Card>
            <CardHeader>
              <CardTitle>
                All Retailers
                <Badge variant="outline" className="ml-2 font-normal">
                  Total {formatCurrency(totalSpending.toString(), currency)}
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Retailer</TableHead>
                    <TableHead className="text-right">Spending</TableHead>
                    <TableHead className="text-right">Income</TableHead>
                    <TableHead className="text-right">Txn Count</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {retailerSummary.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
                        No data
                      </TableCell>
                    </TableRow>
                  ) : (
                    retailerSummary.map((r) => (
                      <TableRow key={r.name}>
                        <TableCell className="font-medium">{r.name}</TableCell>
                        <TableCell className="text-right font-mono text-sm text-red-600">
                          {r.spending.isZero() ? "—" : formatCurrency(r.spending.toString(), currency)}
                        </TableCell>
                        <TableCell className="text-right font-mono text-sm text-foreground">
                          {r.income.isZero() ? "—" : formatCurrency(r.income.toString(), currency)}
                        </TableCell>
                        <TableCell className="text-right text-muted-foreground text-sm">
                          {r.count}
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
