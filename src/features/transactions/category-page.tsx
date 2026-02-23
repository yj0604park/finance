import { useMemo, useState } from "react";
import { format, subMonths } from "date-fns";
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
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

const CATEGORY_LABELS: Record<string, string> = {
  ETC: "기타",
  FOOD: "식비",
  TRANSPORT: "교통",
  SHOPPING: "쇼핑",
  HEALTH: "건강",
  CULTURE: "문화",
  TRAVEL: "여행",
  EDUCATION: "교육",
  COMMUNICATION: "통신",
  UTILITY: "공과금",
  INCOME: "수입",
  TRANSFER: "이체",
};

const CHART_COLORS = [
  "#6366f1", "#f59e0b", "#10b981", "#ef4444", "#3b82f6",
  "#8b5cf6", "#ec4899", "#14b8a6", "#f97316", "#84cc16",
  "#06b6d4", "#a855f7",
];

export function CategoryPage() {
  const defaultEndDate = format(new Date(), "yyyy-MM-dd");
  const defaultStartDate = format(subMonths(new Date(), 1), "yyyy-MM-dd");

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

  const { spendingByCategory, incomeByCategory } = useMemo(() => {
    const spending: Record<string, Decimal> = {};
    const income: Record<string, Decimal> = {};

    for (const edge of transactions) {
      const tx = edge.node;
      if (tx.account.currency !== currency || tx.isInternal) continue;
      const amount = new Decimal(tx.amount);
      const category = tx.type;

      if (amount.isNegative()) {
        spending[category] = (spending[category] ?? new Decimal(0)).plus(amount.abs());
      } else {
        income[category] = (income[category] ?? new Decimal(0)).plus(amount);
      }
    }

    const spendingByCategory = Object.entries(spending)
      .map(([type, total]) => ({ type, total, label: CATEGORY_LABELS[type] ?? type }))
      .sort((a, b) => b.total.comparedTo(a.total));

    const incomeByCategory = Object.entries(income)
      .map(([type, total]) => ({ type, total, label: CATEGORY_LABELS[type] ?? type }))
      .sort((a, b) => b.total.comparedTo(a.total));

    return { spendingByCategory, incomeByCategory };
  }, [transactions, currency]);

  const totalSpending = spendingByCategory.reduce(
    (acc, item) => acc.plus(item.total),
    new Decimal(0),
  );

  const chartData = spendingByCategory.map((item) => ({
    name: item.label,
    value: toNumber(item.total.toString()),
  }));

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
        <h1 className="text-3xl font-bold tracking-tight">Categories</h1>
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Skeleton className="h-80 w-full" />
          <Skeleton className="h-80 w-full" />
        </div>
      ) : (
        <>
          {/* Chart + Spending Table */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Spending by Category</CardTitle>
              </CardHeader>
              <CardContent>
                {chartData.length === 0 ? (
                  <div className="flex h-64 items-center justify-center text-muted-foreground">
                    No spending data
                  </div>
                ) : (
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={110}
                        paddingAngle={2}
                        dataKey="value"
                      >
                        {chartData.map((_, index) => (
                          <Cell
                            key={`cell-${index.toString()}`}
                            fill={CHART_COLORS[index % CHART_COLORS.length]}
                          />
                        ))}
                      </Pie>
                      <Tooltip
                        formatter={(value: number) =>
                          formatCurrency(value.toString(), currency)
                        }
                      />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>
                  Spending Detail
                  <Badge variant="outline" className="ml-2 font-normal">
                    Total {formatCurrency(totalSpending.toString(), currency)}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Category</TableHead>
                      <TableHead className="text-right">Amount</TableHead>
                      <TableHead className="text-right">%</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {spendingByCategory.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={3} className="text-center text-muted-foreground py-6">
                          No data
                        </TableCell>
                      </TableRow>
                    ) : (
                      spendingByCategory.map((item, idx) => {
                        const pct = totalSpending.isZero()
                          ? 0
                          : item.total.div(totalSpending).times(100).toNumber();
                        return (
                          <TableRow key={item.type}>
                            <TableCell className="flex items-center gap-2">
                              <span
                                className="inline-block h-3 w-3 rounded-full"
                                style={{ backgroundColor: CHART_COLORS[idx % CHART_COLORS.length] }}
                              />
                              {item.label}
                            </TableCell>
                            <TableCell className="text-right font-mono text-sm">
                              {formatCurrency(item.total.toString(), currency)}
                            </TableCell>
                            <TableCell className="text-right text-muted-foreground text-sm">
                              {pct.toFixed(1)}%
                            </TableCell>
                          </TableRow>
                        );
                      })
                    )}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>

          {/* Income Table */}
          {incomeByCategory.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Income by Category</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Category</TableHead>
                      <TableHead className="text-right">Amount</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {incomeByCategory.map((item) => (
                      <TableRow key={item.type}>
                        <TableCell>{item.label}</TableCell>
                        <TableCell className="text-right font-mono text-sm text-foreground">
                          {formatCurrency(item.total.toString(), currency)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
