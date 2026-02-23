import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { formatCurrency } from "@/lib/format";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { format, parseISO } from "date-fns";

interface SalaryBarChartProps {
  data: ReadonlyArray<{ date: string; grossPay: number; netPay: number }>;
  loading: boolean;
}

export function SalaryBarChart({ data, loading }: SalaryBarChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">Salary Over Time</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <Skeleton className="h-[300px] w-full" />
        ) : data.length === 0 ? (
          <div className="flex h-[300px] items-center justify-center text-muted-foreground">
            No salary data available
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={[...data]}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="date"
                tickFormatter={(v: string) => {
                  try {
                    return format(parseISO(v), "yy/MM");
                  } catch {
                    return v;
                  }
                }}
                className="text-xs"
              />
              <YAxis
                tickFormatter={(v: number) => `$${(v / 1000).toFixed(0)}K`}
                className="text-xs"
                width={60}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (!active || !payload?.length) return null;
                  return (
                    <div className="rounded-lg border bg-background p-3 shadow-sm">
                      <p className="text-xs text-muted-foreground mb-1">{payload[0]?.payload?.date}</p>
                      {payload.map((p) => (
                        <p key={p.dataKey as string} className="text-sm">
                          <span className="font-medium">{p.dataKey === "grossPay" ? "Gross" : "Net"}: </span>
                          {formatCurrency(p.value as number, "USD")}
                        </p>
                      ))}
                    </div>
                  );
                }}
              />
              <Legend />
              <Bar dataKey="grossPay" name="Gross Pay" fill="hsl(var(--chart-1))" radius={[2, 2, 0, 0]} />
              <Bar dataKey="netPay" name="Net Pay" fill="hsl(var(--chart-2))" radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
