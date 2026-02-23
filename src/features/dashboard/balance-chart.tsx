import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { toNumber, formatCurrency } from "@/lib/format";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { format, parseISO } from "date-fns";

interface SnapshotEdge {
  node: {
    id: string;
    amount: string;
    currency: string;
    date: string;
  };
}

interface BalanceChartProps {
  title: string;
  data: ReadonlyArray<SnapshotEdge>;
  loading: boolean;
  currency: string;
}

export function BalanceChart({ title, data, loading, currency }: BalanceChartProps) {
  const chartData = data.map((edge) => ({
    date: edge.node.date,
    amount: toNumber(edge.node.amount),
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <Skeleton className="h-[250px] w-full" />
        ) : chartData.length === 0 ? (
          <div className="flex h-[250px] items-center justify-center text-muted-foreground">
            No snapshot data available
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id={`gradient-${currency}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="date"
                tickFormatter={(v: string) => {
                  try {
                    return format(parseISO(v), "MM/dd");
                  } catch {
                    return v;
                  }
                }}
                className="text-xs"
              />
              <YAxis
                tickFormatter={(v: number) =>
                  currency === "KRW"
                    ? `${(v / 1000000).toFixed(0)}M`
                    : `$${(v / 1000).toFixed(0)}K`
                }
                className="text-xs"
                width={60}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (!active || !payload?.length) return null;
                  const item = payload[0];
                  return (
                    <div className="rounded-lg border bg-background p-2 shadow-sm">
                      <p className="text-xs text-muted-foreground">{item.payload.date}</p>
                      <p className="text-sm font-bold">
                        {formatCurrency(item.value as number, currency)}
                      </p>
                    </div>
                  );
                }}
              />
              <Area
                type="monotone"
                dataKey="amount"
                stroke="hsl(var(--chart-1))"
                fill={`url(#gradient-${currency})`}
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
